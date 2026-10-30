# Google Play – teksty i odpowiedzi do formularzy

Limity Google Play: nazwa 30 znaków, krótki opis 80 znaków, pełny opis 4000 znaków.

---

## 🇵🇱 Polski (pl-PL) – język domyślny

**Nazwa aplikacji** (23 znaki)
```
Tankvia: koszty auta
```

**Krótki opis** (78 znaków)
```
Tankowania, spalanie, ładowanie EV, serwisy i przypomnienia – wszystko o aucie
```

**Pełny opis**
```
Tankvia to prosty i czytelny dziennik Twojego samochodu. Zapisuj tankowania, sprawdzaj realne spalanie, pilnuj terminów serwisów i miej pełną kontrolę nad kosztami auta – bez zakładania konta.

⛽ TANKOWANIA I SPALANIE
• Data, godzina, stacja, rodzaj paliwa, ilość, cena i koszt – wpisz dowolne dwie wartości, trzecia wyliczy się sama
• Dokładne spalanie metodą „do pełna” – po każdym tankowaniu i średnio
• Ile kilometrów przejechałeś od poprzedniego tankowania
• Stacje w pobliżu jednym przyciskiem (GPS)
• Zdjęcia paragonów i faktur – także w formacie HEIC

⚡ AUTA ELEKTRYCZNE I HYBRYDY PLUG-IN
• Ładowanie w domu, w pracy, AC i szybkie DC
• Zużycie energii w kWh/100 km, poziom baterii przed i po, moc ładowania
• Ile oszczędzasz w porównaniu z autem spalinowym

🔧 SERWIS I KOSZTY
• Serwisy, naprawy, opony, przeglądy, ubezpieczenie, podatki, leasing, parking, autostrady, myjnia i inne
• Pole „Ważne do” – np. koniec polisy OC – aplikacja sama doda przypomnienie

🔔 PRZYPOMNIENIA
• Terminy według daty lub przebiegu
• Powiadomienia 7 dni przed terminem i w dniu terminu

📈 TRENDY I RAPORTY
• Wykresy spalania, cen paliwa i miesięcznych wydatków
• Koszt na 1 km i na 100 km, porównanie cen na stacjach
• Raport historii pojazdu do PDF – przyda się przy sprzedaży auta

👓 WYGODA
• Lupa: powiększenie całej aplikacji do 200%
• Wiele samochodów, wiele walut, jednostki km/L lub mile/galony
• Jasny i ciemny motyw (zgodnie z ustawieniami telefonu)
• Kopia zapasowa i eksport do CSV (Excel)

🔒 PRYWATNOŚĆ
Twoje dane są zapisywane wyłącznie na Twoim telefonie. Bez kont, bez reklam, bez śledzenia.
```

---

## 🇬🇧 English (en-US / en-GB)

**App name** (21 chars)
```
Tankvia: car costs
```

**Short description** (79 chars)
```
Fill-ups, fuel economy, EV charging, service and reminders – all about your car
```

**Full description**
```
Tankvia is a simple, clear logbook for your car. Record fill-ups, see your real fuel economy, keep track of service dates and stay on top of every car cost – no account needed.

⛽ FILL-UPS AND FUEL ECONOMY
• Date, time, station, fuel grade, amount, price and cost – enter any two, the third is calculated
• Accurate full-to-full consumption – per fill-up and on average
• Distance driven since the previous fill-up
• Nearby stations with one tap (GPS)
• Photos of receipts and invoices – including HEIC

⚡ ELECTRIC CARS AND PLUG-IN HYBRIDS
• Home, workplace, public AC and DC fast charging
• Energy use in kWh/100 km (or mi/kWh), battery level before and after, charging power
• How much you save compared with a combustion car

🔧 SERVICE AND COSTS
• Service, repairs, tyres, inspections, insurance, tax, lease, parking, tolls, car wash and more
• “Valid until” field – e.g. insurance expiry – adds a reminder automatically

🔔 REMINDERS
• Due by date or by odometer
• Notifications 7 days before and on the due date

📈 TRENDS AND REPORTS
• Charts of consumption, fuel prices and monthly spending
• Cost per km and per 100 km, fuel prices by station
• Vehicle history report as PDF – handy when selling your car

👓 COMFORT
• Magnifier: enlarge the whole app up to 200%
• Multiple cars, 20 currencies, km/L or miles/gallons
• Light and dark theme (follows your phone)
• Backup and CSV export (Excel)

🔒 PRIVACY
Your data is stored only on your phone. No accounts, no ads, no tracking.
```

---

## Pliki do wgrania (folder `store/`)

| Pole w konsoli | Plik |
|---|---|
| Ikona aplikacji (512×512) | `store/icon-512.png` |
| Grafika (1024×500) | `store/feature-graphic-pl.png` / `store/feature-graphic-en.png` |
| Zrzuty ekranu telefonu (2–8 szt.) | `store/screenshots/pl/*.png` / `store/screenshots/en/*.png` |
| Pakiet aplikacji (AAB) | `dist/Tankvia-<wersja>.aab` |
| Polityka prywatności (URL) | `https://hofi9014.github.io/refuelling/privacy.html` |

---

## Podpowiedzi do formularzy w konsoli

**Kategoria:** Auto i pojazdy (Auto & Vehicles). **Tagi:** np. „Spalanie”, „Koszty samochodu”.

**Reklamy:** Nie, aplikacja nie zawiera reklam.

**Dostęp do aplikacji:** Wszystkie funkcje są dostępne bez logowania.

**Grupa docelowa:** 18+ (aplikacja dla kierowców). Nie jest skierowana do dzieci.

**Klasyfikacja treści (kwestionariusz IARC):** kategoria „Narzędzia / Użyteczność”. Na wszystkie pytania o przemoc, seks, wulgaryzmy, hazard, substancje itp. – „Nie”. Użytkownicy nie komunikują się ze sobą i nie udostępniają treści.

**Bezpieczeństwo danych (Data safety):**
- *Czy aplikacja zbiera lub udostępnia dane użytkownika?* → **Nie.** Dane wpisane w aplikacji pozostają na urządzeniu i nie są wysyłane do dewelopera.
- Uwaga: lokalizacja jest wysyłana jednorazowo do OpenStreetMap tylko po naciśnięciu „Stacje w pobliżu”, wyłącznie by wyszukać stacje, i nie jest zapisywana. Google traktuje przetwarzanie „efemeryczne” na żądanie użytkownika łagodniej, ale **ostrożniej jest zadeklarować**: *Lokalizacja → Przybliżona i dokładna lokalizacja → Zbierane: tak, Udostępniane: nie, Przetwarzane efemerycznie: tak, Wymagane: nie (opcjonalne), Cel: Funkcje aplikacji*.
- *Czy dane są szyfrowane podczas przesyłania?* → Tak (HTTPS).
- *Czy użytkownik może poprosić o usunięcie danych?* → Dane są tylko na urządzeniu; użytkownik usuwa je sam w aplikacji lub odinstalowując ją.

**Aplikacje dotyczące finansów / zdrowia / rządowe:** Nie dotyczy.
