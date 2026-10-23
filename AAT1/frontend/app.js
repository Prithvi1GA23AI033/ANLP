// AAT1 frontend. All requests go to the local Flask app on port 5001.
const API = "http://localhost:5001";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

async function loadSample() {
  const r = await fetch(API + "/api/sample");
  if (!r.ok) throw new Error("HTTP " + r.status);
  const d = await r.json();
  $("q1-text").value = d.paragraph;
}

async function runQ1() {
  const text = $("q1-text").value;
  $("q1-out").innerHTML = "<p class='status'>Working…</p>";
  try {
    const r = await fetch(API + "/api/pos-ner", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({paragraph: text})
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    let html = "", last = 0;
    d.entities.forEach(e => {
      html += esc(text.slice(last, e.start)) + `<mark class="${e.label}">${esc(e.text)}<b>${e.label}</b></mark>`;
      last = e.end;
    });
    html += esc(text.slice(last));
    const counts = Object.entries(d.pos_counts).sort((a, b) => b[1] - a[1]).map(([k, v]) => `<span class="tag">${k}: ${v}</span>`).join("");
    $("q1-out").innerHTML = `
     <h3>Named entities in context</h3><div class="ent-view">${html}</div>
     <div class="grid2" style="margin-top:6px">
      <div><h3>Words and POS tags (${d.tokens.length} tokens)</h3><table><tr><th>#</th><th>Word</th><th>POS</th><th>Tag</th><th>Lemma</th><th>Meaning</th></tr>
       ${d.tokens.map((t, i) => `<tr><td>${i + 1}</td><td>${esc(t.text)}</td><td><span class="pos">${t.pos}</span></td><td>${t.tag}</td><td>${esc(t.lemma)}</td><td>${esc(t.pos_meaning)}</td></tr>`).join("")}</table></div>
      <div><h3>Entities (${d.entities.length})</h3><table><tr><th>Entity</th><th>Label</th><th>Meaning</th></tr>
       ${d.entities.map(e => `<tr><td>${esc(e.text)}</td><td><span class="pos">${e.label}</span></td><td>${esc(e.meaning)}</td></tr>`).join("")}</table>
       <h3>POS distribution</h3>${counts}<p class="status">Model: ${esc(d.model)}</p></div>
     </div>`;
  } catch (e) {
    $("q1-out").innerHTML = `<p class="err">Backend error: ${esc(e.message)}. Is app.py running on port 5001?</p>`;
  }
}

loadSample().catch(e => {
  $("q1-out").innerHTML = `<p class="err">Could not load data/paragraph.txt from port 5001 (${esc(e.message)}).</p>`;
});
