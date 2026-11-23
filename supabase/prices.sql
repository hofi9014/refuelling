-- Tankvia: shared fuel prices ("Where to fill up?").
-- Run once in Supabase: SQL Editor → New query → paste this whole file → Run. Running it again is safe.
--
-- Nothing about the person is stored: only the station (name and position), the fuel, the price per litre, the currency and the day.
-- The app can't read or write the tables directly; it only calls the two functions below, which check every price.

create table if not exists public.prices (
  id           bigint generated always as identity primary key,
  station_key  text not null,                       -- the station's position rounded to ~100 m, so reports from different phones meet
  station_name text not null check (char_length(station_name) between 2 and 200),
  lat          double precision not null check (lat between -90 and 90),
  lon          double precision not null check (lon between -180 and 180),
  grade        text not null check (grade in ('pb95','pb98','on','onp','lpg','cng','e85')),
  price        numeric(10,3) not null check (price > 0),   -- per litre (the app converts gallons)
  currency     text not null check (currency ~ '^[A-Z]{3}$'),
  day          date not null,
  source       text not null check (source in ('receipt','pump')),
  created_at   timestamptz not null default now()
);
create index if not exists prices_station on public.prices (station_key, grade, day desc);
create index if not exists prices_area on public.prices (currency, grade, lat, lon);

-- daily counters for the usage check (GitHub Actions warns before the free plan runs out)
create table if not exists public.usage_daily (
  day      date primary key,
  writes   integer not null default 0,
  reads    integer not null default 0,
  rows_out bigint  not null default 0
);

alter table public.prices enable row level security;
alter table public.usage_daily enable row level security;
revoke all on public.prices, public.usage_daily from public, anon, authenticated;

-- A price from the app. Returns 'ok', 'duplicate', 'outlier' (too far from what others paid) or 'invalid'.
create or replace function public.report_price(
  p_lat double precision, p_lon double precision, p_name text, p_grade text,
  p_price numeric, p_currency text, p_day date, p_source text)
returns text language plpgsql security definer set search_path = public as $$
declare k text; med double precision; n bigint;
begin
  if p_grade is null or p_grade not in ('pb95','pb98','on','onp','lpg','cng','e85')
     or p_source is null or p_source not in ('receipt','pump')
     or p_currency is null or p_currency !~ '^[A-Z]{3}$'
     or p_price is null or p_price <= 0 or p_price > 100000
     or p_lat is null or p_lat not between -90 and 90 or p_lon is null or p_lon not between -180 and 180
     or p_day is null or p_day > current_date + 1 or p_day < current_date - 60
     or p_name is null or char_length(p_name) not between 2 and 200 then
    return 'invalid';
  end if;
  k := round(p_lat::numeric, 3)::text || ',' || round(p_lon::numeric, 3)::text;
  if exists (select 1 from prices where station_key = k and grade = p_grade and day = p_day and price = round(p_price, 3)) then
    return 'duplicate';
  end if;
  -- far from what was paid at this station lately: most likely a misread number
  select percentile_cont(0.5) within group (order by price), count(*) into med, n
    from prices where station_key = k and grade = p_grade and currency = p_currency and day >= current_date - 30;
  if n >= 3 and abs(p_price - med) > med * 0.25 then return 'outlier'; end if;
  -- far from the area's prices (about 50 km around)
  select percentile_cont(0.5) within group (order by price), count(*) into med, n
    from prices where grade = p_grade and currency = p_currency and day >= current_date - 14
      and lat between p_lat - 0.5 and p_lat + 0.5 and lon between p_lon - 0.8 and p_lon + 0.8;
  if n >= 5 and abs(p_price - med) > med * 0.4 then return 'outlier'; end if;
  insert into prices (station_key, station_name, lat, lon, grade, price, currency, day, source)
    values (k, left(p_name, 200), round(p_lat::numeric, 5), round(p_lon::numeric, 5), p_grade, round(p_price, 3), p_currency, p_day, p_source);
  insert into usage_daily (day, writes) values (current_date, 1)
    on conflict (day) do update set writes = usage_daily.writes + 1;
  return 'ok';
end $$;

-- The newest price of every fuel at every station around a point (radius in km, at most 50), last 60 days.
create or replace function public.nearby_prices(p_lat double precision, p_lon double precision, p_km double precision, p_currency text)
returns table (station_key text, station_name text, lat double precision, lon double precision, grade text, price numeric, day date, reports bigint)
language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare dl double precision := least(greatest(coalesce(p_km, 15), 1), 50) / 111.0; dn double precision; c bigint;
begin
  dn := dl / greatest(cos(radians(p_lat)), 0.2);
  return query
    select distinct on (p.station_key, p.grade) p.station_key, p.station_name, p.lat, p.lon, p.grade, p.price, p.day,
           count(*) over (partition by p.station_key, p.grade)
      from prices p
     where p.currency = p_currency and p.day >= current_date - 60
       and p.lat between p_lat - dl and p_lat + dl and p.lon between p_lon - dn and p_lon + dn
     order by p.station_key, p.grade, p.day desc, p.created_at desc
     limit 400;
  get diagnostics c = row_count;
  insert into usage_daily (day, reads, rows_out) values (current_date, 1, c)
    on conflict (day) do update set reads = usage_daily.reads + 1, rows_out = usage_daily.rows_out + c;
end $$;

-- For the daily usage check only (needs the secret key; the app can't call it).
create or replace function public.usage_stats()
returns json language sql security definer set search_path = public as $$
  select json_build_object(
    'db_bytes',     pg_database_size(current_database()),
    'rows',         (select count(*) from prices),
    'writes_30d',   coalesce((select sum(writes)   from usage_daily where day >= current_date - 30), 0),
    'reads_30d',    coalesce((select sum(reads)    from usage_daily where day >= current_date - 30), 0),
    'rows_out_30d', coalesce((select sum(rows_out) from usage_daily where day >= current_date - 30), 0))
$$;

revoke all on function public.report_price(double precision, double precision, text, text, numeric, text, date, text) from public;
revoke all on function public.nearby_prices(double precision, double precision, double precision, text) from public;
revoke all on function public.usage_stats() from public, anon, authenticated;
grant execute on function public.report_price(double precision, double precision, text, text, numeric, text, date, text) to anon, authenticated;
grant execute on function public.nearby_prices(double precision, double precision, double precision, text) to anon, authenticated;
grant execute on function public.usage_stats() to service_role;
