// AAT2 frontend. All requests go to the local Flask app on port 5002.
const API = "http://localhost:5002";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const lines = id => $(id).value.split("\n").map(s => s.trim()).filter(Boolean);

document.addEventListener("click", event => {
  if (event.target.matches(".chips span")) {
    $(event.target.parentElement.dataset.target).value = event.target.textContent;
  }
});

async function loadSample() {
  const r = await fetch(API + "/api/sample");
  if (!r.ok) throw new Error("HTTP " + r.status);
  const d = await r.json();
  $("q2-docs").value = d.documents.join("\n");
  $("q2-q").value = d.question;
  $("q2-chips").innerHTML = d.suggestions.map(q => `<span>${esc(q)}</span>`).join("");
}

async function runQ2() {
  $("q2-out").innerHTML = "<p class='status'>Working…</p>";
  try {
    const r = await fetch(API + "/api/qa", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: $("q2-q").value, documents: lines("q2-docs")})
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    const max = Math.max(...d.ranked.map(row => row.score), 0.0001);
    $("q2-out").innerHTML = `<h3>Answer</h3><div class="answer"><small>Most relevant sentence</small>${esc(d.answer)}</div>
     <h3>Top ranked sentences (out of ${d.num_sentences})</h3><table><tr><th>Rank</th><th>Sentence</th><th>Doc</th><th>Cosine score</th></tr>
     ${d.ranked.map((row, i) => `<tr><td>${i + 1}</td><td>${esc(row.sentence)}</td><td>D${row.doc}</td><td><span class="bar" style="width:${Math.round(90 * row.score / max)}px"></span> ${row.score.toFixed(3)}</td></tr>`).join("")}</table>`;
  } catch (e) {
    $("q2-out").innerHTML = `<p class="err">Backend error: ${esc(e.message)}. Is app.py running on port 5002?</p>`;
  }
}

loadSample().catch(e => {
  $("q2-out").innerHTML = `<p class="err">Could not load sample documents from port 5002 (${esc(e.message)}).</p>`;
});
