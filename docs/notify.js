// Shared by the page and the service worker, which has no access to the app's I18N: [soon, overdue, due today, in days, days ago, in distance].
const NOTIFY_TEXT = {
  pl: ["Zbliża się termin", "Termin minął", "Dziś mija termin", "za {n} dni", "{n} dni temu", "za {n} {u}"],
  en: ["Coming up", "Overdue", "Due today", "in {n} days", "{n} days ago", "in {n} {u}"],
  de: ["Termin steht bevor", "Überfällig", "Heute fällig", "in {n} Tagen", "vor {n} Tagen", "in {n} {u}"],
  fr: ["Échéance proche", "En retard", "Échéance aujourd'hui", "dans {n} jours", "il y a {n} jours", "dans {n} {u}"],
  es: ["Próximo vencimiento", "Vencido", "Vence hoy", "en {n} días", "hace {n} días", "en {n} {u}"],
  it: ["In scadenza", "Scaduto", "Scade oggi", "tra {n} giorni", "{n} giorni fa", "tra {n} {u}"],
  pt: ["Prazo a aproximar-se", "Em atraso", "Termina hoje", "daqui a {n} dias", "há {n} dias", "daqui a {n} {u}"],
  nl: ["Binnenkort", "Verlopen", "Vandaag", "over {n} dagen", "{n} dagen geleden", "over {n} {u}"],
  da: ["Snart", "Overskredet", "I dag", "om {n} dage", "for {n} dage siden", "om {n} {u}"],
  sv: ["Snart", "Försenad", "Idag", "om {n} dagar", "för {n} dagar sedan", "om {n} {u}"],
  nb: ["Snart", "Forfalt", "I dag", "om {n} dager", "for {n} dager siden", "om {n} {u}"],
  fi: ["Pian", "Myöhässä", "Tänään", "{n} päivän päästä", "{n} päivää sitten", "{n} {u} päästä"],
  is: ["Styttist í", "Fallið á tíma", "Í dag", "eftir {n} daga", "fyrir {n} dögum", "eftir {n} {u}"],
  cs: ["Blíží se termín", "Po termínu", "Termín je dnes", "za {n} dní", "před {n} dny", "za {n} {u}"],
  sk: ["Blíži sa termín", "Po termíne", "Termín je dnes", "o {n} dní", "pred {n} dňami", "o {n} {u}"],
  hu: ["Közelgő határidő", "Lejárt", "Ma esedékes", "{n} nap múlva", "{n} napja", "{n} {u} múlva"],
  ro: ["Termen apropiat", "Termen depășit", "Termen azi", "în {n} zile", "acum {n} zile", "în {n} {u}"],
  bg: ["Наближава срок", "Просрочено", "Срокът е днес", "след {n} дни", "преди {n} дни", "след {n} {u}"],
  uk: ["Наближається термін", "Прострочено", "Термін сьогодні", "за {n} дн.", "{n} дн. тому", "за {n} {u}"],
  tr: ["Yaklaşıyor", "Gecikti", "Bugün", "{n} gün sonra", "{n} gün önce", "{n} {u} sonra"],
  hi: ["जल्द देय", "समय बीत गया", "आज देय", "{n} दिन में", "{n} दिन पहले", "{n} {u} में"],
  ja: ["期限が近づいています", "期限切れ", "今日が期限です", "あと{n}日", "{n}日前", "あと{n}{u}"]
};
const notifyText = S => NOTIFY_TEXT[S.settings.lang] || NOTIFY_TEXT.en;
// Which reminders deserve a notification now.
// A reminder notifies once when it gets close (7 days / 500 km) and once more when it is overdue.
function dueNotifications(S, notified, todayStr) {
  const out = [], tx = notifyText(S), fill = (s, n, u) => s.replace("{n}", n).replace("{u}", u), du = /^(us|uk)$/.test(S.settings.units) ? "mi" : "km";
  for (const r of S.reminders || []) {
    if (r.done) continue;
    const V = (S.vehicles || []).find(v => v.id === r.vid);
    if (!V) continue;
    const odo = Math.max(0, ...["fuel", "charges", "services"].flatMap(k => (S[k] || []).filter(x => x.vid === r.vid).map(x => +x.odo || 0)));
    const dd = r.date ? Math.round((new Date(r.date + "T12:00") - new Date(todayStr + "T12:00")) / 864e5) : null;
    const dk = r.odo ? r.odo - odo : null;
    const over = (dd != null && dd < 0) || (dk != null && dk <= 0), soon = (dd != null && dd <= 7) || (dk != null && dk <= 500);
    if (!over && !soon) continue;
    const key = `${r.id}:${over ? "over" : "soon"}:${r.date || ""}:${r.odo || ""}`;
    if (notified[key]) continue;
    const when = [
      dd != null && (dd >= 0 ? fill(tx[3], dd) : fill(tx[4], -dd)),
      dk != null && dk > 0 && fill(tx[5], dk, du)
    ].filter(Boolean).join(", ");
    out.push({
      key, tag: r.id,
      title: over ? tx[1] : tx[0],
      body: `${V.name}: ${r.title}${when ? ` (${when})` : ""}`
    });
  }
  return out;
}
