// AAT5 frontend. All requests go to the local Flask app on port 5005.
const API = "http://localhost:5005";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const lines = id => $(id).value.split("\n").map(s => s.trim()).filter(Boolean);

async function loadSample() {
  const r = await fetch(API + "/api/sample");
  if (!r.ok) throw new Error("HTTP " + r.status);
  const d = await r.json();
  $("q5-w").value = d.word;
  $("q5-ctx").value = d.contexts.join("\n");
}

async function runQ5() {
  $("q5-out").innerHTML = "<p class='status'>Working…</p>";
  try {
    const r = await fetch(API + "/api/wordnet", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({word: $("q5-w").value, contexts: lines("q5-ctx")})
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    $("q5-out").innerHTML = `<h3>Meaning in context (Lesk)</h3><table><tr><th>Sentence</th><th>Chosen synset</th><th>Definition</th></tr>
     ${d.contexts.map(row => `<tr><td>${esc(row.sentence)}</td><td><span class="pos">${esc(row.synset)}</span></td><td>${esc(row.definition)}</td></tr>`).join("")}</table>
     <h3>All synonyms of “${esc(d.word)}”</h3>${d.all_synonyms.map(syn => `<span class="tag">${esc(syn)}</span>`).join("")}
     <h3>WordNet senses (${d.num_senses})</h3><table><tr><th>#</th><th>Synset</th><th>POS</th><th>Definition</th><th>Synonyms</th></tr>
     ${d.senses.map((sense, i) => `<tr><td>${i + 1}</td><td>${esc(sense.synset)}</td><td>${sense.pos}</td><td>${esc(sense.definition)}${sense.examples.length ? `<br><i style="color:#6b6458">e.g. ${esc(sense.examples[0])}</i>` : ""}</td><td>${esc(sense.synonyms.join(", "))}</td></tr>`).join("")}</table>`;
  } catch (e) {
    $("q5-out").innerHTML = `<p class="err">Backend error: ${esc(e.message)}. Is app.py running on port 5005?</p>`;
  }
}

loadSample().catch(e => {
  $("q5-out").innerHTML = `<p class="err">Could not load data/word.txt from port 5005 (${esc(e.message)}).</p>`;
});
