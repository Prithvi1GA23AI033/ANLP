// AAT4 frontend. All requests go to the local Flask app on port 5004.
const API = "http://localhost:5004";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const lines = id => $(id).value.split("\n").map(s => s.trim()).filter(Boolean);

async function loadSample() {
  const r = await fetch(API + "/api/sample");
  if (!r.ok) throw new Error("HTTP " + r.status);
  const d = await r.json();
  $("q4-docs").value = d.documents.join("\n");
  $("q4-k").value = d.n_topics;
  $("q4-seed").value = d.seed;
}

async function runQ4() {
  $("q4-out").innerHTML = "<p class='status'>Working…</p>";
  try {
    const r = await fetch(API + "/api/lda", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({documents: lines("q4-docs"), n_topics: $("q4-k").value, seed: $("q4-seed").value})
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    $("q4-out").innerHTML = `<h3>Top five words per topic</h3><div class="topics">${d.topics.map(topic => `<div class="topic"><h4>Topic ${topic.topic}</h4>
      ${topic.words.map((word, i) => `<div><span>${i + 1}. ${esc(word)}</span><span><span class="bar" style="width:${Math.round(400 * topic.weights[i])}px"></span> ${topic.weights[i]}</span></div>`).join("")}</div>`).join("")}</div>
     <h3>Dominant topic per document (vocabulary: ${d.vocab_size} words, seed ${d.seed})</h3><table><tr><th>Doc</th><th>Text</th><th>Topic</th><th>Probability</th></tr>
     ${d.documents.map(row => `<tr><td>D${row.doc}</td><td>${esc(row.text)}</td><td><span class="pos">T${row.topic}</span></td><td>${row.prob}</td></tr>`).join("")}</table>`;
  } catch (e) {
    $("q4-out").innerHTML = `<p class="err">Backend error: ${esc(e.message)}. Is app.py running on port 5004?</p>`;
  }
}

loadSample().catch(e => {
  $("q4-out").innerHTML = `<p class="err">Could not load data/documents.txt from port 5004 (${esc(e.message)}).</p>`;
});
