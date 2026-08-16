(() => {
  const depthMeta = {
    part_a: { label: "OD-0 / Surface decision", short: "OD-0" },
    part_b: { label: "OD-1 / First-order impact", short: "OD-1" },
    part_c: { label: "OD-2 / Multi-agent interaction", short: "OD-2" },
    part_d: { label: "OD-n / Equilibrium reasoning", short: "OD-n" }
  };

  const coverageText = {
    "OD-0": "Surface decision only. No causal effect of the output has been marked.",
    "OD-1": "The analysis includes a first-order effect on the target or affected actors.",
    "OD-2": "The analysis also includes feedback through other systems, incentives or future data.",
    "OD-n": "The analysis asks whether the policy remains stable under mutual adaptation."
  };

  const state = {
    scenarios: [],
    scenario: null,
    part: "part_a"
  };

  const elements = {
    select: document.querySelector("#scenarioSelect"),
    random: document.querySelector("#randomScenario"),
    meta: document.querySelector("#scenarioMeta"),
    title: document.querySelector("#scenario-heading"),
    description: document.querySelector("#scenarioDescription"),
    promptLevel: document.querySelector("#promptLevel"),
    promptText: document.querySelector("#promptText"),
    promptRubric: document.querySelector("#promptRubric"),
    checklist: document.querySelector("#lensChecklist"),
    coverage: document.querySelector("#coverageOutput"),
    receipt: document.querySelector("#receiptJson"),
    copy: document.querySelector("#copyReceipt"),
    download: document.querySelector("#downloadReceipt"),
    share: document.querySelector("#shareScenario"),
    status: document.querySelector("#actionStatus")
  };

  function selectedLenses() {
    return [...elements.checklist.querySelectorAll("input:checked")].map((input) => input.value);
  }

  function observerCoverage(lenses) {
    const hasImpact = lenses.includes("target_change") || lenses.includes("actor_adaptation");
    const hasSystem = lenses.includes("system_feedback");
    const hasEquilibrium = lenses.includes("equilibrium");
    if (hasImpact && hasSystem && hasEquilibrium) return "OD-n";
    if (hasImpact && hasSystem) return "OD-2";
    if (hasImpact) return "OD-1";
    return "OD-0";
  }

  function receiptObject() {
    const lenses = selectedLenses();
    return {
      schema: "reflexbench_orientation_receipt_v1",
      scenario_id: state.scenario?.id ?? null,
      scenario_title: state.scenario?.title ?? null,
      domain: state.scenario?.domain ?? null,
      inspected_prompt_level: depthMeta[state.part].short,
      observer_coverage: observerCoverage(lenses),
      selected_lenses: lenses,
      source: `https://mianzhang.org/demos/reflexbench-observer-depth/?scenario=${encodeURIComponent(state.scenario?.id ?? "")}`,
      generated_at: new Date().toISOString(),
      boundary: "Orientation only. This receipt is not a ReflexBench model score, safety certification, or deployment authorization."
    };
  }

  function updateReceipt() {
    const receipt = receiptObject();
    elements.receipt.textContent = JSON.stringify(receipt, null, 2);
    elements.coverage.innerHTML = `<span>Current coverage</span><strong>${receipt.observer_coverage}</strong><p>${coverageText[receipt.observer_coverage]}</p>`;
  }

  function updateScenario() {
    const scenario = state.scenario;
    if (!scenario) return;
    const part = scenario[state.part];
    elements.meta.textContent = `${scenario.id} / ${scenario.domain}`;
    elements.title.textContent = scenario.title;
    elements.description.textContent = scenario.description;
    elements.promptLevel.textContent = depthMeta[state.part].label;
    elements.promptText.textContent = part.prompt;
    elements.promptRubric.textContent = part.rubric;
    document.querySelectorAll(".depth-button").forEach((button) => {
      const active = button.dataset.level === state.part;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    });
    const url = new URL(window.location.href);
    url.searchParams.set("scenario", scenario.id);
    window.history.replaceState({}, "", url);
    updateReceipt();
  }

  function setScenario(id) {
    state.scenario = state.scenarios.find((scenario) => scenario.id === id) ?? state.scenarios[0];
    elements.select.value = state.scenario.id;
    updateScenario();
  }

  async function copyText(text, successMessage) {
    await navigator.clipboard.writeText(text);
    elements.status.textContent = successMessage;
  }

  async function loadScenarios() {
    try {
      const response = await fetch("reflexbench.jsonl", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const body = await response.text();
      state.scenarios = body.trim().split(/\r?\n/).map((line) => JSON.parse(line));
      elements.select.innerHTML = state.scenarios.map((scenario) => `<option value="${scenario.id}">${scenario.id} · ${scenario.title}</option>`).join("");
      elements.select.disabled = false;
      const requested = new URLSearchParams(window.location.search).get("scenario");
      setScenario(requested);
    } catch (error) {
      elements.title.textContent = "Scenario data unavailable";
      elements.description.textContent = "The public scenario file could not be loaded. Open the GitHub artifact or retry after the page deployment is complete.";
      elements.status.textContent = error.message;
    }
  }

  elements.select.addEventListener("change", () => setScenario(elements.select.value));
  elements.random.addEventListener("click", () => {
    if (!state.scenarios.length) return;
    const index = Math.floor(Math.random() * state.scenarios.length);
    setScenario(state.scenarios[index].id);
  });
  document.querySelectorAll(".depth-button").forEach((button) => button.addEventListener("click", () => {
    state.part = button.dataset.level;
    updateScenario();
  }));
  elements.checklist.addEventListener("change", updateReceipt);
  elements.copy.addEventListener("click", async () => {
    try { await copyText(elements.receipt.textContent, "Receipt copied."); }
    catch { elements.status.textContent = "Clipboard access was blocked by the browser."; }
  });
  elements.download.addEventListener("click", () => {
    const blob = new Blob([elements.receipt.textContent], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `reflexbench-${state.scenario?.id ?? "scenario"}-orientation.json`;
    link.click();
    URL.revokeObjectURL(link.href);
    elements.status.textContent = "Receipt downloaded.";
  });
  elements.share.addEventListener("click", async () => {
    const url = new URL(window.location.href).toString();
    const data = { title: `ReflexBench ${state.scenario?.id}`, text: `${state.scenario?.title}: inspect what changes after the model speaks.`, url };
    try {
      if (navigator.share) await navigator.share(data);
      else await copyText(url, "Scenario link copied.");
    } catch (error) {
      if (error.name !== "AbortError") elements.status.textContent = "Share action was not completed.";
    }
  });

  loadScenarios();
})();
