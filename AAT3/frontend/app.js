// AAT3 frontend. All requests go to the local Flask app on port 5003.
const API = "http://localhost:5003";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

document.addEventListener("click", event => {
  if (event.target.matches(".chips span")) {
    $(event.target.parentElement.dataset.target).value = event.target.textContent;
  }
});

async function loadSample() {
  const r = await fetch(API + "/api/sample");
  if (!r.ok) throw new Error("HTTP " + r.status);
  const d = await r.json();
  $("q3-q").value = d.question;
  $("q3-chips").innerHTML = d.suggestions.map(q => `<span>${esc(q)}</span>`).join("");
  const status = await fetch(API + "/api/status");
  if (status.ok) {
    const s = await status.json();
    $("q3-status").innerHTML = `Knowledge source: <b>${esc(s.knowledge_source)}</b> · LLM: ${esc(s.llm)}`;
  }
}

async function runQ3() {
  $("q3-out").innerHTML = "<p class='status'>Working…</p>";
  try {
    const r = await fetch(API + "/api/rag", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: $("q3-q").value})
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    const fallback = d.generator.startsWith("Template");
    $("q3-status").innerHTML = `Knowledge source: <b>${esc(d.knowledge_source)}</b> · Generator: <span class="tag ${fallback ? "fb" : ""}">${esc(d.generator)}</span>`;
    $("q3-out").innerHTML = `<h3>Generated answer</h3><div class="answer"><small>${esc(d.generator)}</small>${esc(d.answer)}</div>
     <h3>Retrieved entities</h3>${d.retrieved_entities.map(hit => `<span class="tag">${esc(hit)}</span>`).join("") || "<p class='status'>none</p>"}
     <h3>Retrieved context passed to the generator (${d.context.length} facts)</h3><table><tr><th>#</th><th>Fact from the graph</th></tr>
     ${d.context.map((fact, i) => `<tr><td>${i + 1}</td><td>${esc(fact)}</td></tr>`).join("")}</table>`;
  } catch (e) {
    $("q3-out").innerHTML = `<p class="err">Backend error: ${esc(e.message)}. Is app.py running on port 5003?</p>`;
  }
}

loadSample().catch(e => {
  $("q3-out").innerHTML = `<p class="err">Could not reach the AAT3 backend on port 5003 (${esc(e.message)}).</p>`;
});
