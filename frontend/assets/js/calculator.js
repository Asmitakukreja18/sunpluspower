/**
 * SunPlus Power Advanced Solar ROI & Financial Sizing Engine
 */

let currentStep = 1;
let currentTab = "overview";
let systemData = {}; // Stores calculated variables globally for sensitivity recalculations

const STATE_IRRADIANCE = {
  "uttar pradesh": 120.0,
  "maharashtra": 125.0,
  "gujarat": 128.0,
  "rajasthan": 132.0,
  "karnataka": 120.0
};

const BASE_TARIFF = 7.5; // Rs. per kWh

document.addEventListener("DOMContentLoaded", () => {
  // Bind input listeners for Live Preview
  const previewInputs = [
    "input-bill", "input-units", "calc-state", "input-grid", "input-roof", "input-storage", "calc-finance-mode"
  ];
  
  previewInputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updateLivePreview);
      el.addEventListener("change", updateLivePreview);
    }
  });

  // Radios input listeners
  const panelRadios = document.querySelectorAll('input[name="panel-tier"]');
  panelRadios.forEach(radio => {
    radio.addEventListener("change", () => {
      highlightTierCard(radio.value);
      updateLivePreview();
    });
  });

  // Sync bill <-> units bidirectionally
  const inputBill = document.getElementById("input-bill");
  const inputUnits = document.getElementById("input-units");
  if (inputBill && inputUnits) {
    inputBill.addEventListener("input", () => {
      inputUnits.value = Math.round(parseFloat(inputBill.value) / BASE_TARIFF);
      document.getElementById("val-units").textContent = `${parseFloat(inputUnits.value).toLocaleString("en-IN")} units`;
    });
    inputUnits.addEventListener("input", () => {
      inputBill.value = Math.round(parseFloat(inputUnits.value) * BASE_TARIFF);
      document.getElementById("val-bill").textContent = `Rs.${parseFloat(inputBill.value).toLocaleString("en-IN")}`;
    });
  }

  // Show/hide battery storage battery capacity slider
  const inputGrid = document.getElementById("input-grid");
  if (inputGrid) {
    inputGrid.addEventListener("change", () => {
      const val = inputGrid.value;
      const storageContainer = document.getElementById("storage-container");
      if (storageContainer) {
        if (val === "hybrid" || val === "off-grid") {
          storageContainer.classList.remove("hidden");
        } else {
          storageContainer.classList.add("hidden");
        }
      }
    });
  }

  // Show/hide loan configurations
  const inputFinance = document.getElementById("calc-finance-mode");
  if (inputFinance) {
    inputFinance.addEventListener("change", () => {
      const loanFields = document.querySelectorAll(".loan-field");
      loanFields.forEach(el => {
        if (inputFinance.value === "loan") {
          el.classList.remove("hidden");
        } else {
          el.classList.add("hidden");
        }
      });
    });
  }

  // Bind Sensitivity Sliders
  const sliderCapex = document.getElementById("sens-slider-capex");
  const sliderTariff = document.getElementById("sens-slider-tariff");
  if (sliderCapex && sliderTariff) {
    sliderCapex.addEventListener("input", runSensitivityRecalculations);
    sliderTariff.addEventListener("input", runSensitivityRecalculations);
  }

  // Load local draft on startup if available
  loadCalculatorDraft();

  // Detect routing clean path
  handleCleanRouting();

  // Listen to browser Back/Forward navigation
  window.addEventListener("popstate", (e) => {
    handleCleanRouting();
  });
});

/** Form stepper navigation */
function updateWizardSidebar() {
  for (let i = 1; i <= 6; i++) {
    const node = document.querySelector(`#step-nav-${i} .step-node`);
    const label = document.querySelector(`#step-nav-${i} span`);
    if (!node) continue;
    
    if (i === currentStep) {
      node.className = "step-node active w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold text-sm";
      label.className = "text-sm font-bold text-on-surface";
    } else if (i < currentStep) {
      node.className = "step-node completed w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold text-sm";
      label.className = "text-sm font-semibold text-primary";
    } else {
      node.className = "step-node w-8 h-8 rounded-full border-2 border-outline flex items-center justify-center font-bold text-sm text-secondary";
      label.className = "text-sm font-semibold text-secondary";
    }
  }
}

function showStep(stepNum) {
  const cards = document.querySelectorAll(".step-card");
  cards.forEach((card, idx) => {
    if (idx + 1 === stepNum) {
      card.classList.remove("hidden");
    } else {
      card.classList.add("hidden");
    }
  });

  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");
  const btnRun = document.getElementById("btn-run");

  if (stepNum === 1) {
    btnPrev.classList.add("hidden");
  } else {
    btnPrev.classList.remove("hidden");
  }

  if (stepNum === 6) {
    btnNext.classList.add("hidden");
    btnRun.classList.remove("hidden");
    populateWizardReviewSummary();
  } else {
    btnNext.classList.remove("hidden");
    btnRun.classList.add("hidden");
  }

  currentStep = stepNum;
  updateWizardSidebar();
}

function wizardNext() {
  const form = document.getElementById("wizard-form");
  // Simple validations per step
  const inputs = document.querySelectorAll(`#step-card-${currentStep} input, #step-card-${currentStep} select`);
  let valid = true;
  inputs.forEach(el => {
    if (!el.checkValidity()) {
      el.reportValidity();
      valid = false;
    }
  });

  if (!valid) return;
  
  if (currentStep < 6) {
    showStep(currentStep + 1);
    saveCalculatorDraft();
  }
}

function wizardPrev() {
  if (currentStep > 1) {
    showStep(currentStep - 1);
  }
}

function highlightTierCard(selectedValue) {
  const labelMap = {
    "standard":  "tier-label-std",
    "high":       "tier-label-high",
    "bifacial":   "tier-label-bifacial"
  };
  Object.entries(labelMap).forEach(([val, id]) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (val === selectedValue) {
      el.classList.add("border-primary", "bg-primary-container/10", "ring-1", "ring-primary/10");
      el.classList.remove("border-outline");
    } else {
      el.classList.remove("border-primary", "bg-primary-container/10", "ring-1", "ring-primary/10");
      el.classList.add("border-outline");
    }
  });
}

function populateWizardReviewSummary() {
  document.getElementById("review-name").textContent = document.getElementById("calc-name").value || "N/A";
  document.getElementById("review-location").textContent = (document.getElementById("calc-state").value || "N/A").toUpperCase();
  document.getElementById("review-units").textContent = `${document.getElementById("input-units").value} units / month`;
  document.getElementById("review-area").textContent = `${document.getElementById("input-roof").value} Sq. Ft.`;
  
  const tier = document.querySelector('input[name="panel-tier"]:checked')?.value || "standard";
  document.getElementById("review-tier").textContent = tier.toUpperCase();
  
  const finance = document.getElementById("calc-finance-mode").value;
  document.getElementById("review-finance").textContent = finance.toUpperCase();
}

/** Local Draft Persistence */
function saveCalculatorDraft() {
  const draft = {
    name: document.getElementById("calc-name").value,
    customer_type: document.getElementById("calc-customer-type").value,
    email: document.getElementById("calc-email").value,
    phone: document.getElementById("calc-phone").value,
    location: document.getElementById("calc-state").value,
    zipcode: document.getElementById("calc-zip").value,
    monthly_bill: document.getElementById("input-bill").value,
    monthly_units: document.getElementById("input-units").value,
    sanctioned_load: document.getElementById("calc-load").value,
    daytime_pct: document.getElementById("calc-daytime").value,
    available_area: document.getElementById("input-roof").value,
    roof_type: document.getElementById("input-roof-type").value,
    orientation: document.getElementById("input-orientation").value,
    shading_level: document.getElementById("input-shading").value,
    grid_mode: document.getElementById("input-grid").value,
    panel_tier: document.querySelector('input[name="panel-tier"]:checked')?.value || "standard",
    storage_kwh: document.getElementById("input-storage").value,
    finance_mode: document.getElementById("calc-finance-mode").value,
    interest_rate: document.getElementById("calc-interest").value,
    loan_tenure: document.getElementById("calc-loan-tenure").value,
    tariff_escalation: document.getElementById("calc-tariff-escalation").value,
    om_escalation: document.getElementById("calc-om-escalation").value,
    discount_rate: document.getElementById("calc-discount-rate").value,
    currentStep
  };
  localStorage.setItem("sunplus_calculator_draft", JSON.stringify(draft));
  
  const status = document.getElementById("draft-status");
  if (status) {
    status.classList.remove("hidden");
    setTimeout(() => status.classList.add("hidden"), 3000);
  }
}

function loadCalculatorDraft() {
  const raw = localStorage.getItem("sunplus_calculator_draft");
  if (!raw) return;
  try {
    const draft = JSON.parse(raw);
    document.getElementById("calc-name").value = draft.name || "";
    document.getElementById("calc-customer-type").value = draft.customer_type || "residential";
    document.getElementById("calc-email").value = draft.email || "";
    document.getElementById("calc-phone").value = draft.phone || "";
    document.getElementById("calc-state").value = draft.location || "uttar pradesh";
    document.getElementById("calc-zip").value = draft.zipcode || "";
    document.getElementById("input-bill").value = draft.monthly_bill || 15000;
    document.getElementById("input-units").value = draft.monthly_units || 2143;
    document.getElementById("calc-load").value = draft.sanctioned_load || 15;
    document.getElementById("calc-daytime").value = draft.daytime_pct || 70;
    document.getElementById("input-roof").value = draft.available_area || 2000;
    document.getElementById("input-roof-type").value = draft.roof_type || "flat";
    document.getElementById("input-orientation").value = draft.orientation || "south";
    document.getElementById("input-shading").value = draft.shading_level || "none";
    document.getElementById("input-grid").value = draft.grid_mode || "rooftop";
    document.getElementById("input-storage").value = draft.storage_kwh || 10;
    document.getElementById("calc-finance-mode").value = draft.finance_mode || "cash";
    document.getElementById("calc-interest").value = draft.interest_rate || 8.5;
    document.getElementById("calc-loan-tenure").value = draft.loan_tenure || 7;
    document.getElementById("calc-tariff-escalation").value = draft.tariff_escalation || 4.0;
    document.getElementById("calc-om-escalation").value = draft.om_escalation || 3.5;
    document.getElementById("calc-discount-rate").value = draft.discount_rate || 8.0;
    
    // Sync slider labels
    document.getElementById("val-units").textContent = `${parseInt(draft.monthly_units || 2143).toLocaleString("en-IN")} units`;
    document.getElementById("val-bill").textContent = `Rs.${parseInt(draft.monthly_bill || 15000).toLocaleString("en-IN")}`;
    document.getElementById("val-storage").textContent = `${draft.storage_kwh || 10} kWh`;

    if (draft.panel_tier) {
      const radio = document.querySelector(`input[name="panel-tier"][value="${draft.panel_tier}"]`);
      if (radio) radio.checked = true;
      highlightTierCard(draft.panel_tier);
    }
    
    currentStep = draft.currentStep || 1;
    showStep(currentStep);
    updateLivePreview();
  } catch (err) {
    console.error("Failed to load draft", err);
  }
}

/** Sizing Sizer Calculations (Live updates) */
function updateLivePreview() {
  const units = parseFloat(document.getElementById("input-units").value) || 0;
  const state = document.getElementById("calc-state").value;
  const grid = document.getElementById("input-grid").value;
  const storage = parseFloat(document.getElementById("input-storage").value) || 0;
  const panelTier = document.querySelector('input[name="panel-tier"]:checked')?.value || "standard";
  const property = document.getElementById("calc-customer-type").value;

  const irradiance = STATE_IRRADIANCE[state] || 120.0;
  let size = units / irradiance;
  if (size < 1.0) size = 1.0;
  size = Math.round(size * 10) / 10;

  // Cost estimates
  let baseCostPerKw = 55000;
  if (grid === "off-grid") baseCostPerKw = 75000;
  if (grid === "hybrid") baseCostPerKw = 85000;

  let premium = 0;
  if (panelTier === "high") premium = 5000;
  if (panelTier === "bifacial") premium = 12000;

  let gross = size * (baseCostPerKw + premium);
  if (grid === "hybrid" || grid === "off-grid") {
    gross += storage * 12000;
  }
  gross = Math.round(gross);

  // Subsidy computations
  let subsidy = 0;
  if (property === "residential" && (grid === "rooftop" || grid === "hybrid")) {
    if (size >= 3.0) subsidy = 78000;
    else if (size >= 2.0) subsidy = 60000;
    else subsidy = Math.round(size * 30000);
  }

  const net = Math.max(0, gross - subsidy);

  document.getElementById("preview-system-size").textContent = `${size} kW`;
  document.getElementById("preview-gross-cost").textContent = `Rs.${gross.toLocaleString("en-IN")}`;
  document.getElementById("preview-subsidy").textContent = `Rs.${subsidy.toLocaleString("en-IN")}`;
  document.getElementById("preview-net-cost").textContent = `Rs.${net.toLocaleString("en-IN")}`;
}

/** Cinematic processing sequence */
function runAnalysisWorkflow() {
  switchView("processing");

  const terminal = document.getElementById("terminal-logs");
  terminal.innerHTML = `<div class="text-white/40">&gt;&gt; SunPlus Power Simulation engine initialized.</div>`;

  const steps = [
    { text: "VALIDATING FORM INPUT PARAMETERS...", duration: 500 },
    { text: "FETCHING LOCAL STATE SOLAR IRRADIANCE DATA...", duration: 800 },
    { text: "SIZING MODULE MATRIX ARRAYS AND BALANCE-OF-SYSTEM (BOS)...", duration: 800 },
    { text: "SIMULATING 25-YEAR CUMULATIVE INVERTER DEGRADATION...", duration: 600 },
    { text: "ESTIMATING UTILITY TARIFF SAVINGS ESCALATIONS...", duration: 500 },
    { text: "NORMALIZING CAPITAL EXPENDITURES AND PAYBACK LIMITS...", duration: 600 }
  ];

  let currentLogIdx = 0;

  function runNextLog() {
    if (currentLogIdx < steps.length) {
      const step = steps[currentLogIdx];
      const timeStr = new Date().toLocaleTimeString();
      
      const logDiv = document.createElement("div");
      logDiv.innerHTML = `[${timeStr}] <span class="text-white">${step.text}</span> <span class="text-green-500 font-bold">DONE</span>`;
      terminal.appendChild(logDiv);
      terminal.scrollTop = terminal.scrollHeight;

      document.getElementById("processing-title").textContent = step.text.replace("...", "");
      document.getElementById("processing-sub").textContent = `TASK ${currentLogIdx + 1} OF ${steps.length}`;

      currentLogIdx++;
      setTimeout(runNextLog, step.duration);
    } else {
      // Completed, redirect to Analysis overview
      setTimeout(() => {
        history.pushState({ view: "analysis", tab: "overview" }, "", "/analysis/overview");
        handleCleanRouting();
      }, 500);
    }
  }

  setTimeout(runNextLog, 300);
}

/** Sizing Engine and Financial Amortization */
function runCalculatorEngine() {
  const name = document.getElementById("calc-name").value || "Valued Customer";
  const state = document.getElementById("calc-state").value;
  const bill = parseFloat(document.getElementById("input-bill").value) || 0;
  const units = parseFloat(document.getElementById("input-units").value) || 0;
  const roof = parseFloat(document.getElementById("input-roof").value) || 0;
  const grid = document.getElementById("input-grid").value;
  const panelTier = document.querySelector('input[name="panel-tier"]:checked')?.value || "standard";
  const storage = parseFloat(document.getElementById("input-storage").value) || 0;
  const property = document.getElementById("calc-customer-type").value;
  
  const financeMode = document.getElementById("calc-finance-mode").value;
  const tariffEsc = (parseFloat(document.getElementById("calc-tariff-escalation").value) || 4.0) / 100;
  const omEsc = (parseFloat(document.getElementById("calc-om-escalation").value) || 3.5) / 100;
  const discRate = (parseFloat(document.getElementById("calc-discount-rate").value) || 8.0) / 100;

  // Sizing Size
  const irradiance = STATE_IRRADIANCE[state] || 120.0;
  let size = units / irradiance;
  if (size < 1.0) size = 1.0;
  size = Math.round(size * 10) / 10;

  // Space required (100 Sq Ft per kW standard)
  const spaceNeeded = Math.round(size * 100);

  // Capital Costs
  let baseCostPerKw = 55000;
  if (grid === "off-grid") baseCostPerKw = 75000;
  if (grid === "hybrid") baseCostPerKw = 85000;

  let premium = 0;
  if (panelTier === "high") premium = 5000;
  if (panelTier === "bifacial") premium = 12000;

  let gross = size * (baseCostPerKw + premium);
  if (grid === "hybrid" || grid === "off-grid") {
    gross += storage * 12000;
  }
  gross = Math.round(gross);

  let subsidy = 0;
  if (property === "residential" && (grid === "rooftop" || grid === "hybrid")) {
    if (size >= 3.0) subsidy = 78000;
    else if (size >= 2.0) subsidy = 60000;
    else subsidy = Math.round(size * 30000);
  }

  const net = Math.max(0, gross - subsidy);
  const annualGen = size * irradiance * 12;
  const firstYearSavings = annualGen * BASE_TARIFF;

  // 25-Year Amortization calculations
  let cumSavings = 0;
  let tableRowsHtml = "";
  const yearsData = [];

  for (let yr = 1; yr <= 25; yr++) {
    const deg = Math.pow(0.995, yr - 1); // 0.5% module degradation per year
    const hike = Math.pow(1 + tariffEsc, yr - 1);
    const omHike = Math.pow(1 + omEsc, yr - 1);

    const yrGen = annualGen * deg;
    const costWithoutSolar = bill * 12 * hike;
    const costWithSolar = Math.max(0, costWithoutSolar - (yrGen * BASE_TARIFF));
    const yrSavings = costWithoutSolar - costWithSolar;
    const yrOm = (size * 1000) * omHike; // Base O&M standard Rs.1000/kW
    const netYrSavings = yrSavings - yrOm;

    cumSavings += netYrSavings;

    yearsData.push({
      year: yr,
      gen: yrGen,
      costWithout: costWithoutSolar,
      costWith: costWithSolar,
      savings: netYrSavings,
      cumulative: cumSavings
    });

    tableRowsHtml += `
      <tr>
        <td class="p-4 font-bold text-on-surface">Year ${yr}</td>
        <td class="p-4">${Math.round(yrGen).toLocaleString("en-IN")} kWh</td>
        <td class="p-4 text-secondary line-through">Rs.${Math.round(costWithoutSolar).toLocaleString("en-IN")}</td>
        <td class="p-4 font-semibold text-primary">Rs.${Math.round(costWithSolar).toLocaleString("en-IN")}</td>
        <td class="p-4 text-green-600 font-bold">Rs.${Math.round(netYrSavings).toLocaleString("en-IN")}</td>
        <td class="p-4 font-bold text-on-surface">Rs.${Math.round(cumSavings).toLocaleString("en-IN")}</td>
      </tr>
    `;
  }

  // Populate Financial Table
  const tbody = document.getElementById("cashflow-table-body");
  if (tbody) tbody.innerHTML = tableRowsHtml;

  // Calculate Payback & IRR (simplified approximation for frontend preview)
  const payback = firstYearSavings > 0 ? net / firstYearSavings : 0;
  const netLifetimeSavings = cumSavings - net;
  const irr = payback > 0 ? (120 / payback) - 4 : 0; // Curve-fitted approximation
  const npv = netLifetimeSavings * 0.45; // Discounted approximation

  // Save values in global object for sliders
  systemData = {
    name, state, bill, units, roof, grid, panelTier, storage, property,
    size, spaceNeeded, gross, subsidy, net, annualGen, firstYearSavings, cumSavings,
    payback, netLifetimeSavings, irr, npv
  };

  // Populate Overview elements
  document.getElementById("analysis-site-name").textContent = `${name}'s Feasibility Run (${state.toUpperCase()})`;
  document.getElementById("ov-payback").textContent = `${payback.toFixed(1)} Years`;
  document.getElementById("ov-irr").textContent = `${irr.toFixed(1)}%`;
  document.getElementById("ov-savings").textContent = `Rs.${Math.round(netLifetimeSavings).toLocaleString("en-IN")}`;
  document.getElementById("ov-npv").textContent = `Rs.${Math.round(npv).toLocaleString("en-IN")}`;
  document.getElementById("ov-capacity").textContent = `${size} kW DC`;
  document.getElementById("ov-area-req").textContent = `${spaceNeeded} Sq. Ft.`;

  // Populate Before/After
  document.getElementById("ba-bill-before").textContent = `Rs.${Math.round(bill).toLocaleString("en-IN")}`;
  const afterBill = Math.max(0, bill - (firstYearSavings / 12));
  document.getElementById("ba-bill-after").textContent = `Rs.${Math.round(afterBill).toLocaleString("en-IN")}`;
  const savingPct = bill > 0 ? ((bill - afterBill) / bill) * 100 : 0;
  document.getElementById("ba-bill-diff").textContent = `Savings of ${Math.round(savingPct)}% per month`;
  
  const solarContribPct = Math.min(95, Math.round((annualGen / (units * 12)) * 100));
  document.getElementById("ba-grid-after").textContent = `${100 - solarContribPct}%`;
  document.getElementById("ba-offset-after").textContent = `${solarContribPct}%`;

  // Populate Eco Offset
  const co2 = annualGen * 0.82; // 0.82 kg CO2 per kWh baseline
  const trees = Math.round(co2 / 22);
  const coal = annualGen * 0.00045; // Tons of coal per kWh
  document.getElementById("env-trees").textContent = `${trees.toLocaleString("en-IN")} Trees`;
  document.getElementById("env-co2").textContent = `${Math.round(co2).toLocaleString("en-IN")} kg`;
  document.getElementById("env-coal").textContent = `${coal.toFixed(2)} Tons`;

  // Render Energy Chart Bars
  renderMonthlyEnergyChart(annualGen / 12, units);

  // Populate Comparisons
  renderScenariosCompareGrid(size, net, payback, irr, netLifetimeSavings);

  // Populate Printable Report
  document.getElementById("rep-name").textContent = name;
  document.getElementById("rep-state").textContent = state.toUpperCase();
  document.getElementById("rep-zip").textContent = document.getElementById("calc-zip").value || "N/A";
  document.getElementById("rep-date").textContent = new Date().toLocaleDateString("en-IN");
  document.getElementById("rep-size").textContent = `${size} kW`;
  document.getElementById("rep-savings").textContent = `Rs.${Math.round(netLifetimeSavings).toLocaleString("en-IN")}`;
  document.getElementById("rep-payback").textContent = `${payback.toFixed(1)} Years`;

  // Submit Submission as Lead (demo mode handles API downtime automatically)
  api.post("/calculator/submit", {
    name,
    email: document.getElementById("calc-email").value,
    phone: document.getElementById("calc-phone").value,
    monthly_bill: bill,
    monthly_units: units,
    location: state,
    install_type: grid
  }).then(res => {
    // If authenticated customer, save calculation to history
    const userSession = JSON.parse(localStorage.getItem("sunplus_customer_session") || "null");
    if (userSession) {
      const historyKey = `customer_calcs_${userSession.email}`;
      const calcs = JSON.parse(localStorage.getItem(historyKey) || "[]");
      calcs.push({
        id: "CALC-" + Math.floor(100000 + Math.random() * 900000),
        name: name,
        date: new Date().toLocaleDateString("en-IN"),
        size: `${size} kW`,
        payback: `${payback.toFixed(1)} Years`,
        status: "Completed",
        inputs: systemData
      });
      localStorage.setItem(historyKey, JSON.stringify(calcs));
    }
  }).catch(err => console.error("Auto submission error: ", err));

  // Run initial sensitivity calculations
  runSensitivityRecalculations();
}

/** Render Scenarios comparison grid */
function renderScenariosCompareGrid(cap, net, pb, irr, life) {
  const container = document.getElementById("scenarios-compare-grid");
  if (!container) return;

  const scenarios = [
    {
      title: "Balanced Scenario",
      desc: "Optimized sizing for highest rate of return (IRR).",
      capacity: `${cap} kW`,
      netCost: `Rs.${Math.round(net).toLocaleString("en-IN")}`,
      payback: `${pb.toFixed(1)} Years`,
      irr: `${irr.toFixed(1)}%`,
      savings: `Rs.${Math.round(life).toLocaleString("en-IN")}`,
      active: true
    },
    {
      title: "Max Savings Scenario",
      desc: "Maximum solar footprint sizing to offset 95% of utility grid.",
      capacity: `${Math.round(cap * 1.3 * 10) / 10} kW`,
      netCost: `Rs.${Math.round(net * 1.25).toLocaleString("en-IN")}`,
      payback: `${(pb * 1.1).toFixed(1)} Years`,
      irr: `${(irr * 0.9).toFixed(1)}%`,
      savings: `Rs.${Math.round(life * 1.25).toLocaleString("en-IN")}`,
      active: false
    },
    {
      title: "Balanced Fixed Scenario",
      desc: "Standard tier fixed rooftop design without trackers.",
      capacity: `${Math.round(cap * 0.9 * 10) / 10} kW`,
      netCost: `Rs.${Math.round(net * 0.8).toLocaleString("en-IN")}`,
      payback: `${(pb * 1.15).toFixed(1)} Years`,
      irr: `${(irr * 0.85).toFixed(1)}%`,
      savings: `Rs.${Math.round(life * 0.8).toLocaleString("en-IN")}`,
      active: false
    }
  ];

  container.innerHTML = scenarios.map(sc => `
    <div class="p-6 bg-white rounded border ${sc.active ? 'border-primary ring-1 ring-primary/10' : 'border-surface-container'} shadow-sm space-y-4">
      <div class="flex justify-between items-center">
        <h4 class="font-bold text-on-surface">${sc.title}</h4>
        ${sc.active ? '<span class="text-[10px] uppercase font-bold bg-primary text-white px-2 py-0.5 rounded">Active</span>' : ''}
      </div>
      <p class="text-xs text-secondary">${sc.desc}</p>
      <div class="space-y-2 border-t border-surface-container pt-3 text-xs">
        <div class="flex justify-between"><span>Capacity Size:</span><span class="font-bold text-on-surface">${sc.capacity}</span></div>
        <div class="flex justify-between"><span>Net Investment:</span><span class="font-bold text-on-surface">${sc.netCost}</span></div>
        <div class="flex justify-between"><span>Payback Period:</span><span class="font-bold text-primary">${sc.payback}</span></div>
        <div class="flex justify-between"><span>Projected IRR:</span><span class="font-bold text-on-surface">${sc.irr}</span></div>
        <div class="flex justify-between"><span>25-Year Net Value:</span><span class="font-bold text-green-600">${sc.savings}</span></div>
      </div>
    </div>
  `).join("");
}

/** Render simple energy bar chart */
function renderMonthlyEnergyChart(avgSolar, monthlyUnits) {
  const container = document.getElementById("energy-chart-container");
  if (!container) return;

  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  
  // Simulated solar seasonal variances
  const variances = [0.85, 0.95, 1.1, 1.2, 1.15, 0.9, 0.7, 0.75, 0.9, 1.05, 1.0, 0.85];

  const html = months.map((mon, idx) => {
    const sol = avgSolar * variances[idx];
    const dem = monthlyUnits;
    const maxVal = Math.max(dem, avgSolar * 1.3);

    const solPct = Math.min(100, Math.round((sol / maxVal) * 100));
    const demPct = Math.min(100, Math.round((dem / maxVal) * 100));

    return `
      <div class="flex flex-col items-center flex-1 h-full gap-1">
        <div class="flex items-end justify-center w-full h-[85%] gap-0.5">
          <div class="w-3 bg-surface-container-high rounded-t transition-all duration-700" style="height: ${demPct}%" title="Demand: ${Math.round(dem)} kWh"></div>
          <div class="w-3 bg-primary rounded-t transition-all duration-700" style="height: ${solPct}%" title="Generation: ${Math.round(sol)} kWh"></div>
        </div>
        <span class="text-[9px] font-bold text-tertiary mt-2">${mon}</span>
      </div>
    `;
  }).join("");

  container.innerHTML = `<div class="w-full flex items-end justify-between px-2 gap-1 h-full">${html}</div>`;
}

/** Run sensitivity analysis live updates */
function runSensitivityRecalculations() {
  if (!systemData.net) return;

  const capFactor = parseFloat(document.getElementById("sens-slider-capex").value) / 100;
  const tariffRate = parseFloat(document.getElementById("sens-slider-tariff").value);

  document.getElementById("sens-val-capex").textContent = `${Math.round(capFactor * 100)}%`;
  document.getElementById("sens-val-tariff").textContent = `${tariffRate.toFixed(1)}%`;

  // Compute sensitivity adjustments
  const adjNetCost = systemData.net * capFactor;
  const adjPayback = systemData.firstYearSavings > 0 ? adjNetCost / (systemData.firstYearSavings * (1 + (tariffRate - 4.0)/100)) : 0;
  const adjIrr = adjPayback > 0 ? (120 / adjPayback) - 4 : 0;

  document.getElementById("sens-res-payback").textContent = `${adjPayback.toFixed(1)} Years`;
  document.getElementById("sens-res-irr").textContent = `${adjIrr.toFixed(1)}%`;
}

/** Trigger quote modal flow */
function requestQuoteFlow() {
  const modal = document.getElementById("quote-modal");
  if (modal) modal.classList.remove("hidden");
  if (modal) modal.classList.add("flex");
}

function closeQuoteModal() {
  const modal = document.getElementById("quote-modal");
  if (modal) modal.classList.add("hidden");
  if (modal) modal.classList.remove("flex");
}

async function submitQuoteRequest(event) {
  event.preventDefault();
  const btn = document.getElementById("quote-submit-btn");
  const origText = btn.innerHTML;
  
  btn.disabled = true;
  btn.innerHTML = `<span class="material-symbols-outlined animate-spin text-sm">autorenew</span> Submitting...`;

  const intent = document.getElementById("quote-intent").value;
  const comments = document.getElementById("quote-comments").value;

  try {
    const result = await api.post("/leads", {
      name: systemData.name || "Calculator Customer",
      email: document.getElementById("calc-email").value,
      phone: document.getElementById("calc-phone").value,
      subject: intent,
      message: `System Capacity: ${systemData.size} kW DC. Net Cost: Rs.${systemData.net}. Zip Code: ${document.getElementById("calc-zip").value}. Notes: ${comments}`,
      source_page: window.location.pathname
    });

    const msg = result.demoMode 
      ? "Demo Mode: Sizing request captured and stored locally for audit."
      : "Sizing request submitted successfully! We'll contact you.";
    
    // Save request in customer requests list if logged in
    const userSession = JSON.parse(localStorage.getItem("sunplus_customer_session") || "null");
    if (userSession) {
      const reqsKey = `customer_reqs_${userSession.email}`;
      const list = JSON.parse(localStorage.getItem(reqsKey) || "[]");
      list.push({
        id: "REQ-" + Math.floor(100000 + Math.random() * 900000),
        subject: intent,
        date: new Date().toLocaleDateString("en-IN"),
        status: "Pending Details",
        description: comments || "Solar survey request details."
      });
      localStorage.setItem(reqsKey, JSON.stringify(list));
    }

    window.showToast(msg, "success", "quote-form-feedback");
    setTimeout(() => {
      closeQuoteModal();
      document.getElementById("quote-submission-form").reset();
    }, 2000);
  } catch (err) {
    window.showToast(err.message || "Failed to submit request.", "error", "quote-form-feedback");
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

/** Routing cleanly helper */
function switchView(viewName) {
  const wizard = document.getElementById("calculator-wizard-view");
  const processing = document.getElementById("calculator-processing-view");
  const analysis = document.getElementById("analysis-workspace-view");

  if (wizard) wizard.classList.add("hidden");
  if (processing) processing.classList.add("hidden");
  if (analysis) analysis.classList.add("hidden");

  if (viewName === "wizard") {
    if (wizard) wizard.classList.remove("hidden");
  } else if (viewName === "processing") {
    if (processing) processing.classList.remove("hidden");
  } else if (viewName === "analysis") {
    if (analysis) analysis.classList.remove("hidden");
  }
}

function switchTab(tabName) {
  const tabs = document.querySelectorAll(".tab-pane");
  tabs.forEach(pane => pane.classList.add("hidden"));

  const targetPane = document.getElementById(`tab-pane-${tabName}`);
  if (targetPane) targetPane.classList.remove("hidden");

  // Reset tab button highlights
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => btn.className = "tab-btn pb-2 border-b-2 border-transparent hover:text-primary transition-all");

  const activeBtn = document.getElementById(`tab-${tabName}`);
  if (activeBtn) activeBtn.className = "tab-btn pb-2 border-b-2 border-primary text-primary font-bold transition-all tab-active";

  currentTab = tabName;
  history.pushState({ view: "analysis", tab: tabName }, "", `/analysis/${tabName}`);
}

function handleCleanRouting() {
  const path = window.location.pathname;
  if (path === "/solar-calculator") {
    switchView("wizard");
    showStep(1);
  } else if (path === "/calculator/processing") {
    switchView("processing");
    runAnalysisWorkflow();
  } else if (path.startsWith("/analysis")) {
    switchView("analysis");
    // Extract tab name from sub-route
    const tabName = path.split("/").pop() || "overview";
    
    // Fallback if calculations haven't been run yet (ensure default mock configurations)
    if (!systemData.net) {
      // Simulate defaults
      document.getElementById("calc-name").value = "SunPlus Partner Demo";
      document.getElementById("calc-state").value = "uttar pradesh";
      document.getElementById("input-bill").value = 15000;
      document.getElementById("input-units").value = 2143;
      runCalculatorEngine();
    }
    
    const validTabs = ["overview", "before-after", "energy", "financial", "environmental", "sensitivity", "compare", "report"];
    if (validTabs.includes(tabName)) {
      switchTab(tabName);
    } else {
      switchTab("overview");
    }
  }
}

// Expose globally
window.wizardNext = wizardNext;
window.wizardPrev = wizardPrev;
window.saveCalculatorDraft = saveCalculatorDraft;
window.runAnalysisWorkflow = runAnalysisWorkflow;
window.switchTab = switchTab;
window.switchView = switchView;
window.closeQuoteModal = closeQuoteModal;
window.requestQuoteFlow = requestQuoteFlow;
window.submitQuoteRequest = submitQuoteRequest;
