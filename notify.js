// Shared by the page and the service worker: which reminders deserve a notification now.
// A reminder notifies once when it gets close (7 days / 500 km) and once more when it is overdue.
function dueNotifications(S, notified, todayStr) {
  const out = [], pl = S.settings.lang === "pl", du = /^(us|uk)$/.test(S.settings.units) ? "mi" : "km";
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
      dd != null && (dd >= 0 ? (pl ? `za ${dd} dni` : `in ${dd} days`) : (pl ? `${-dd} dni temu` : `${-dd} days ago`)),
      dk != null && dk > 0 && (pl ? `za ${dk} ${du}` : `in ${dk} ${du}`)
    ].filter(Boolean).join(", ");
    out.push({
      key, tag: r.id,
      title: over ? (pl ? "Termin minął" : "Overdue") : (pl ? "Zbliża się termin" : "Coming up"),
      body: `${V.name}: ${r.title}${when ? ` (${when})` : ""}`
    });
  }
  return out;
}
