// Global state
let state = {
  currentStep: 1,
  customer: {
    type: 'residential',
    name: '',
    organization: '',
    email: '',
    phone: '',
    pin: '',
    city: '',
    state: 'Uttar Pradesh'
  },
  energy: {
    inputMethod: 'bill',
    monthlyBill: 0,
    monthlyConsumption: 0,
    tariff: 7,
    connectionType: 'domestic',
    sanctionedLoad: 0
  },
  site: {
    propertyType: 'residential',
    roofType: 'rcc',
    availableArea: 0,
    address: '',
    pin: '',
    city: '',
    state: 'Uttar Pradesh',
    lat: 26.8467,
    lng: 80.9462
  },
  system: {
    type: 'grid',
    panelTech: 'monocrystalline',
    systemLoss: 15,
    inverterEfficiency: 97,
    battery: false,
    capacityMode: 'auto',
    preferredCapacity: 0,
    recommendedCapacity: 0,
    annualGeneration: 0,
    areaRequired: 0,
    feasible: true
  },
  financial: {
    costPerKw: 55000,
    tariffEscalation: 4,
    omCost: 1000,
    omEscalation: 3,
    degradation: 0.5,
    projectLife: 25,
    discountRate: 8,
    financingType: 'cash',
    downPayment: 20,
    interestRate: 9,
    loanTenure: 10
  }
};

// State-wise solar irradiance (kWh/kW/day)
const STATE_IRRADIANCE = {
  'Andhra Pradesh': 5.5,
  'Arunachal Pradesh': 4.5,
  'Assam': 4.5,
  'Bihar': 5.0,
  'Chhattisgarh': 5.2,
  'Goa': 5.3,
  'Gujarat': 5.8,
  'Haryana': 5.3,
  'Himachal Pradesh': 5.0,
  'Jharkhand': 5.1,
  'Karnataka': 5.4,
  'Kerala': 5.0,
  'Madhya Pradesh': 5.5,
  'Maharashtra': 5.3,
  'Manipur': 4.8,
  'Meghalaya': 4.6,
  'Mizoram': 4.7,
  'Nagaland': 4.6,
  'Odisha': 5.2,
  'Punjab': 5.2,
  'Rajasthan': 5.8,
  'Sikkim': 4.7,
  'Tamil Nadu': 5.3,
  'Telangana': 5.4,
  'Tripura': 4.7,
  'Uttar Pradesh': 5.1,
  'Uttarakhand': 5.0,
  'West Bengal': 4.9,
  'Andaman and Nicobar Islands': 5.2,
  'Chandigarh': 5.2,
  'Dadra and Nagar Haveli': 5.4,
  'Daman and Diu': 5.5,
  'Delhi': 5.1,
  'Lakshadweep': 5.3,
  'Puducherry': 5.3
};

let map = null;
let marker = null;
let energyChart = null;
let financialChart = null;

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  updateSidebar();

  // Add download report button listener
  const downloadBtn = document.getElementById('btn-download-report');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadReport);
  }
});

function initEventListeners() {
  // Step 1: Customer Profile
  document.getElementById('calc-customer-type').addEventListener('change', (e) => {
    state.customer.type = e.target.value;
    updateSidebar();
  });
  document.getElementById('calc-name').addEventListener('input', (e) => {
    state.customer.name = e.target.value;
    updateSidebar();
  });
  document.getElementById('calc-organization').addEventListener('input', (e) => {
    state.customer.organization = e.target.value;
  });
  document.getElementById('calc-email').addEventListener('input', (e) => {
    state.customer.email = e.target.value;
  });
  document.getElementById('calc-phone').addEventListener('input', (e) => {
    state.customer.phone = e.target.value;
  });
  document.getElementById('calc-pin').addEventListener('input', (e) => {
    state.customer.pin = e.target.value;
  });
  document.getElementById('calc-city').addEventListener('input', (e) => {
    state.customer.city = e.target.value;
  });
  document.getElementById('calc-state').addEventListener('change', (e) => {
    state.customer.state = e.target.value;
    state.site.state = e.target.value;
    updateSidebar();
  });

  // Step 2: Energy Profile
  document.getElementById('input-method-bill').addEventListener('change', () => {
    state.energy.inputMethod = 'bill';
    document.getElementById('bill-input-container').classList.remove('hidden');
    document.getElementById('consumption-input-container').classList.add('hidden');
  });
  document.getElementById('input-method-consumption').addEventListener('change', () => {
    state.energy.inputMethod = 'consumption';
    document.getElementById('bill-input-container').classList.add('hidden');
    document.getElementById('consumption-input-container').classList.remove('hidden');
  });
  document.getElementById('calc-bill').addEventListener('input', (e) => {
    state.energy.monthlyBill = parseFloat(e.target.value) || 0;
    updateSidebar();
    updatePreview();
  });
  document.getElementById('calc-consumption').addEventListener('input', (e) => {
    state.energy.monthlyConsumption = parseFloat(e.target.value) || 0;
    updateSidebar();
    updatePreview();
  });
  document.getElementById('calc-tariff').addEventListener('input', (e) => {
    state.energy.tariff = parseFloat(e.target.value) || 7;
    updatePreview();
  });
  document.getElementById('calc-connection-type').addEventListener('change', (e) => {
    state.energy.connectionType = e.target.value;
  });
  document.getElementById('calc-sanctioned-load').addEventListener('input', (e) => {
    state.energy.sanctionedLoad = parseFloat(e.target.value) || 0;
  });

  // Step 3: Property & Site
  document.getElementById('calc-property-type').addEventListener('change', (e) => {
    state.site.propertyType = e.target.value;
  });
  document.getElementById('calc-roof-type').addEventListener('change', (e) => {
    state.site.roofType = e.target.value;
  });
  document.getElementById('calc-area').addEventListener('input', (e) => {
    state.site.availableArea = parseFloat(e.target.value) || 0;
    updatePreview();
  });
  document.getElementById('calc-site-address').addEventListener('input', (e) => {
    state.site.address = e.target.value;
  });
  document.getElementById('calc-site-pin').addEventListener('input', (e) => {
    state.site.pin = e.target.value;
    updateMapFromSite();
  });
  document.getElementById('calc-site-city').addEventListener('input', (e) => {
    state.site.city = e.target.value;
    updateMapFromSite();
  });
  document.getElementById('calc-site-state').addEventListener('change', (e) => {
    state.site.state = e.target.value;
    updatePreview();
    updateMapFromSite();
  });

  // Step 4: Solar System
  document.querySelectorAll('input[name="system-type"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      state.system.type = e.target.value;
      updateSystemTypeUI();
      updatePreview();
    });
  });
  document.getElementById('calc-panel-tech').addEventListener('change', (e) => {
    state.system.panelTech = e.target.value;
  });
  document.getElementById('calc-loss').addEventListener('input', (e) => {
    state.system.systemLoss = parseFloat(e.target.value) || 15;
    updatePreview();
  });
  document.getElementById('calc-inverter-efficiency').addEventListener('input', (e) => {
    state.system.inverterEfficiency = parseFloat(e.target.value) || 97;
    updatePreview();
  });
  document.getElementById('calc-battery').addEventListener('change', (e) => {
    state.system.battery = e.target.checked;
  });
  document.getElementById('capacity-auto').addEventListener('change', () => {
    state.system.capacityMode = 'auto';
    document.getElementById('manual-capacity-container').classList.add('hidden');
    updatePreview();
  });
  document.getElementById('capacity-manual').addEventListener('change', () => {
    state.system.capacityMode = 'manual';
    document.getElementById('manual-capacity-container').classList.remove('hidden');
  });
  document.getElementById('calc-capacity').addEventListener('input', (e) => {
    state.system.preferredCapacity = parseFloat(e.target.value) || 0;
    updatePreview();
  });

  // Step 5: Financial Model
  document.getElementById('calc-cost-per-kw').addEventListener('input', (e) => {
    state.financial.costPerKw = parseFloat(e.target.value) || 55000;
  });
  document.getElementById('calc-tariff-escalation').addEventListener('input', (e) => {
    state.financial.tariffEscalation = parseFloat(e.target.value) || 4;
  });
  document.getElementById('calc-om-cost').addEventListener('input', (e) => {
    state.financial.omCost = parseFloat(e.target.value) || 1000;
  });
  document.getElementById('calc-om-escalation').addEventListener('input', (e) => {
    state.financial.omEscalation = parseFloat(e.target.value) || 3;
  });
  document.getElementById('calc-degradation').addEventListener('input', (e) => {
    state.financial.degradation = parseFloat(e.target.value) || 0.5;
  });
  document.getElementById('calc-project-life').addEventListener('input', (e) => {
    state.financial.projectLife = parseInt(e.target.value) || 25;
  });
  document.getElementById('calc-discount-rate').addEventListener('input', (e) => {
    state.financial.discountRate = parseFloat(e.target.value) || 8;
  });
  document.getElementById('financing-cash').addEventListener('change', () => {
    state.financial.financingType = 'cash';
    document.getElementById('loan-fields').classList.add('hidden');
  });
  document.getElementById('financing-loan').addEventListener('change', () => {
    state.financial.financingType = 'loan';
    document.getElementById('loan-fields').classList.remove('hidden');
  });
  document.getElementById('calc-down-payment').addEventListener('input', (e) => {
    state.financial.downPayment = parseFloat(e.target.value) || 20;
  });
  document.getElementById('calc-interest-rate').addEventListener('input', (e) => {
    state.financial.interestRate = parseFloat(e.target.value) || 9;
  });
  document.getElementById('calc-loan-tenure').addEventListener('input', (e) => {
    state.financial.loanTenure = parseInt(e.target.value) || 10;
  });
}

function updateSystemTypeUI() {
  const labels = ['grid', 'off-grid', 'hybrid'];
  labels.forEach(type => {
    const radio = document.getElementById(`system-type-${type}`);
    const parent = radio.closest('label');
    if (radio.checked) {
      parent.classList.remove('border-surface-container-highest', 'hover:border-on-surface', 'bg-white');
      parent.classList.add('border-2', 'border-primary', 'bg-surface-container-lowest');
    } else {
      parent.classList.add('border', 'border-surface-container-highest', 'hover:border-on-surface', 'bg-white');
      parent.classList.remove('border-2', 'border-primary', 'bg-surface-container-lowest');
    }
  });
}

function initMap() {
  const mapContainer = document.getElementById('map');
  if (!mapContainer) return;

  map = L.map('map').setView([state.site.lat, state.site.lng], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map);

  marker = L.marker([state.site.lat, state.site.lng], { draggable: true }).addTo(map);
  marker.on('dragend', (e) => {
    const newPos = e.target.getLatLng();
    updateLocationInputs(newPos.lat, newPos.lng);
  });
  map.on('click', (e) => {
    marker.setLatLng(e.latlng);
    updateLocationInputs(e.latlng.lat, e.latlng.lng);
  });

  updateLocationInputs(state.site.lat, state.site.lng);
}

function updateLocationInputs(lat, lng) {
  state.site.lat = lat;
  state.site.lng = lng;
  document.getElementById('calc-lat').value = lat.toFixed(6);
  document.getElementById('calc-lng').value = lng.toFixed(6);
}

async function updateMapFromSite() {
  // Create query string based on what info we have
  let queryParts = [];
  if (state.site.city) queryParts.push(state.site.city);
  if (state.site.state) queryParts.push(state.site.state);
  if (state.site.pin) queryParts.push(state.site.pin);
  queryParts.push('India');

  const query = queryParts.join(', ');
  if (!state.site.city && !state.site.pin) return;

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`
    );
    const data = await response.json();
    if (data && data.length > 0) {
      const firstResult = data[0];
      const lat = parseFloat(firstResult.lat);
      const lng = parseFloat(firstResult.lon);
      if (map && marker) {
        map.setView([lat, lng], 13);
        marker.setLatLng([lat, lng]);
        updateLocationInputs(lat, lng);
      }
    }
  } catch (error) {
    console.error('Error updating map from site:', error);
  }
}

function nextStep(step) {
  if (step > state.currentStep) {
    const valid = validateStep(state.currentStep);
    if (!valid) return;
  }

  state.currentStep = step;

  // Update UI
  document.querySelectorAll('section[id^="form-step-"]').forEach(s => s.classList.add('hidden'));
  const target = document.getElementById(`form-step-${step}`);
  if (target) target.classList.remove('hidden');

  // Update progress
  const progressBar = document.getElementById('progress-bar');
  const progressLabel = document.getElementById('step-label');
  const progress = ((step - 1) / 5) * 100;
  if (progressBar) progressBar.style.width = `${progress}%`;
  if (progressLabel) progressLabel.textContent = `Step ${step} of 6`;

  if (step === 6) {
    updateReviewSection();
  }

  if (step === 4) {
    updatePreview();
  }

  if (step === 3) {
    if (!map) {
      initMap();
    }
    setTimeout(() => {
      if (map) {
        map.invalidateSize(); // Fix grey tiles by invalidating size
      }
    }, 100);
    updateMapFromSite();
  }
}

function downloadReport() {
  // Calculate results first
  const results = calculateFinancials();
  
  // Create report content
  let report = `
SUNPLUS POWER SOLAR CALCULATION REPORT
=====================================
Date: ${new Date().toLocaleDateString()}

CUSTOMER DETAILS
-----------------
Name: ${state.customer.name || '-'}
Organization: ${state.customer.organization || '-'}
Email: ${state.customer.email || '-'}
Phone: ${state.customer.phone || '-'}
Location: ${state.customer.city || '-'}, ${state.customer.state}, ${state.customer.pin || '-'}

ENERGY PROFILE
--------------
Input Method: ${state.energy.inputMethod === 'bill' ? 'Monthly Bill' : 'Monthly Consumption'}
Monthly Bill: ${state.energy.inputMethod === 'bill' ? '₹' + state.energy.monthlyBill.toLocaleString('en-IN') : '-'}
Monthly Consumption: ${state.energy.inputMethod === 'consumption' ? state.energy.monthlyConsumption.toFixed(0) + ' kWh' : (state.energy.monthlyBill / state.energy.tariff).toFixed(0) + ' kWh'}
Tariff: ₹${state.energy.tariff.toFixed(2)}/kWh
Connection Type: ${state.energy.connectionType}
Sanctioned Load: ${state.energy.sanctionedLoad.toFixed(0)} kW

SITE DETAILS
------------
Property Type: ${state.site.propertyType}
Roof Type: ${state.site.roofType}
Available Area: ${state.site.availableArea.toFixed(0)} sq. ft.
Address: ${state.site.address || '-'}
Coordinates: ${state.site.lat.toFixed(6)}, ${state.site.lng.toFixed(6)}

SYSTEM CONFIGURATION
--------------------
System Type: ${state.system.type}
Panel Technology: ${state.system.panelTech}
System Loss: ${state.system.systemLoss}%
Inverter Efficiency: ${state.system.inverterEfficiency}%
Battery: ${state.system.battery ? 'Yes' : 'No'}
Recommended Capacity: ${results.systemSize.toFixed(2)} kW

FINANCIAL SUMMARY
-----------------
Gross Cost: ₹${results.grossCost.toLocaleString('en-IN')}
Subsidy: ₹${results.subsidy.toLocaleString('en-IN')}
Net Investment: ₹${results.netInvestment.toLocaleString('en-IN')}
Payback Period: ${results.paybackYear ? results.paybackYear.toFixed(1) + ' Years' : '-'}
ROI: ${results.roi.toFixed(1)}%
Lifetime Savings (25 years): ₹${results.lifetimeSavings.toLocaleString('en-IN')}
Annual Generation: ${results.annualGeneration.toFixed(0)} kWh
CO2 Offset: ${results.co2Offset.toFixed(0)} kg CO2/year
Trees Planted Equivalent: ${results.treesPlanted.toFixed(0)} trees/year
  `;

  // Create blob and download
  const blob = new Blob([report], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `sunplus-solar-report-${Date.now()}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function validateStep(step) {
  if (step === 1) {
    const name = document.getElementById('calc-name').value.trim();
    const email = document.getElementById('calc-email').value.trim();
    const pin = document.getElementById('calc-pin').value.trim();
    const city = document.getElementById('calc-city').value.trim();

    if (!name) {
      alert('Please enter your name.');
      return false;
    }
    if (!email || !email.includes('@')) {
      alert('Please enter a valid email.');
      return false;
    }
    if (!pin) {
      alert('Please enter your PIN code.');
      return false;
    }
    if (!city) {
      alert('Please enter your city.');
      return false;
    }
  } else if (step === 3) {
    const area = parseFloat(document.getElementById('calc-area').value);
    if (!area || area <= 0) {
      alert('Please enter available area.');
      return false;
    }
  }
  return true;
}

function updateReviewSection() {
  document.getElementById('review-name').textContent = state.customer.name || '-';
  document.getElementById('review-email').textContent = state.customer.email || '-';
  document.getElementById('review-phone').textContent = state.customer.phone || '-';
  document.getElementById('review-location').textContent = `${state.customer.city}, ${state.customer.state}, ${state.customer.pin}` || '-';

  if (state.energy.inputMethod === 'bill') {
    document.getElementById('review-bill').textContent = `₹${state.energy.monthlyBill.toLocaleString('en-IN')}`;
    const consumption = state.energy.monthlyBill / state.energy.tariff;
    document.getElementById('review-consumption').textContent = `${consumption.toFixed(0)} kWh`;
  } else {
    document.getElementById('review-bill').textContent = `₹${(state.energy.monthlyConsumption * state.energy.tariff).toLocaleString('en-IN')}`;
    document.getElementById('review-consumption').textContent = `${state.energy.monthlyConsumption.toFixed(0)} kWh`;
  }
  document.getElementById('review-tariff').textContent = `₹${state.energy.tariff.toFixed(2)}/kWh`;

  document.getElementById('review-property').textContent = state.site.propertyType.charAt(0).toUpperCase() + state.site.propertyType.slice(1);
  document.getElementById('review-area').textContent = `${state.site.availableArea.toFixed(0)} sq. ft.`;
  document.getElementById('review-coords').textContent = `${state.site.lat.toFixed(4)}, ${state.site.lng.toFixed(4)}`;

  document.getElementById('review-system-type').textContent = state.system.type.charAt(0).toUpperCase() + state.system.type.slice(1);
  document.getElementById('review-capacity').textContent = `${state.system.recommendedCapacity.toFixed(2)} kW`;
  document.getElementById('review-panel-tech').textContent = state.system.panelTech.charAt(0).toUpperCase() + state.system.panelTech.slice(1);
}

function updatePreview() {
  calculateSystemSize();
  document.getElementById('preview-capacity').textContent = `${state.system.recommendedCapacity.toFixed(2)} kW`;
  document.getElementById('preview-generation').textContent = `${state.system.annualGeneration.toFixed(0)} kWh`;
  document.getElementById('preview-area').textContent = `${state.system.areaRequired.toFixed(0)} sq. ft.`;

  if (state.system.feasible) {
    document.getElementById('preview-feasibility').textContent = 'Feasible';
    document.getElementById('preview-feasibility').classList.remove('text-red-600');
    document.getElementById('preview-feasibility').classList.add('text-green-600');
  } else {
    document.getElementById('preview-feasibility').textContent = 'Area Insufficient';
    document.getElementById('preview-feasibility').classList.add('text-red-600');
    document.getElementById('preview-feasibility').classList.remove('text-green-600');
  }
}

function calculateSystemSize() {
  // Get monthly consumption
  let monthlyConsumption;
  if (state.energy.inputMethod === 'bill') {
    monthlyConsumption = state.energy.monthlyBill / state.energy.tariff;
  } else {
    monthlyConsumption = state.energy.monthlyConsumption;
  }

  const dailyConsumption = monthlyConsumption / 30;
  const irradiance = STATE_IRRADIANCE[state.site.state] || 5.0;

  // Calculate system size (kW)
  const systemLoss = state.system.systemLoss / 100;
  const inverterEfficiency = state.system.inverterEfficiency / 100;
  const systemSize = dailyConsumption / (irradiance * (1 - systemLoss) * inverterEfficiency);

  if (state.system.capacityMode === 'auto') {
    state.system.recommendedCapacity = systemSize;
  } else {
    state.system.recommendedCapacity = state.system.preferredCapacity || systemSize;
  }

  // Annual generation
  state.system.annualGeneration = state.system.recommendedCapacity * irradiance * 365 * (1 - systemLoss) * inverterEfficiency;

  // Area required (100 sq ft per kW)
  state.system.areaRequired = state.system.recommendedCapacity * 100;

  // Feasibility
  state.system.feasible = state.site.availableArea >= state.system.areaRequired;
}

function updateSidebar() {
  document.getElementById('sidebar-name').textContent = state.customer.name || 'Not provided';

  if (state.energy.inputMethod === 'bill') {
    document.getElementById('sidebar-bill').textContent = `₹${state.energy.monthlyBill.toLocaleString('en-IN')}/mo`;
  } else {
    document.getElementById('sidebar-bill').textContent = `${state.energy.monthlyConsumption.toFixed(0)} kWh/mo`;
  }

  document.getElementById('sidebar-location').textContent = `${state.customer.city || 'Not provided'}, ${state.customer.state}`;
  document.getElementById('sidebar-system').textContent = `${state.system.recommendedCapacity.toFixed(2)} kW ${state.system.type.charAt(0).toUpperCase() + state.system.type.slice(1)}`;
}

async function runAnalysis() {
  const btn = document.getElementById('btn-run-analysis');
  const originalContent = btn.innerHTML;
  btn.innerHTML = '<span class="material-symbols-outlined animate-spin">autorenew</span> Analyzing...';
  btn.disabled = true;

  // Perform calculations
  const results = calculateFinancials();

  // Show results
  document.getElementById('results-area').classList.remove('hidden');
  populateResults(results);
  drawCharts(results);

  btn.innerHTML = originalContent;
  btn.disabled = false;

  document.getElementById('results-area').scrollIntoView({ behavior: 'smooth' });
}

function calculateFinancials() {
  calculateSystemSize();

  const systemSize = state.system.recommendedCapacity;
  const costPerKw = state.financial.costPerKw;
  const tariff = state.energy.tariff;
  const tariffEscalation = state.financial.tariffEscalation / 100;
  const omCostPerKw = state.financial.omCost;
  const omEscalation = state.financial.omEscalation / 100;
  const degradationRate = state.financial.degradation / 100;
  const projectLife = state.financial.projectLife;
  const discountRate = state.financial.discountRate / 100;

  const grossCost = systemSize * costPerKw;

  // Subsidy calculation (only for residential rooftop up to 3 kW)
  let subsidy = 0;
  if (state.customer.type === 'residential' && state.site.roofType !== 'ground') {
    if (systemSize <= 2) {
      subsidy = systemSize * 30000;
    } else if (systemSize <= 3) {
      subsidy = (2 * 30000) + ((systemSize - 2) * 18000);
    }
    subsidy = Math.min(subsidy, 78000);
  }

  const netInvestment = grossCost - subsidy;

  // Calculate annual generation and savings
  const years = [];
  const annualSavings = [];
  const utilityCosts = [];
  const solarCosts = [];
  let cumulativeSavings = 0;
  let cumulativeUtility = 0;
  let cumulativeSolar = 0;

  let annualGeneration = state.system.annualGeneration;

  let monthlyConsumption;
  if (state.energy.inputMethod === 'bill') {
    monthlyConsumption = state.energy.monthlyBill / tariff;
  } else {
    monthlyConsumption = state.energy.monthlyConsumption;
  }
  const annualConsumption = monthlyConsumption * 12;

  for (let year = 1; year <= projectLife; year++) {
    const escalationFactor = Math.pow(1 + tariffEscalation, year - 1);
    const omFactor = Math.pow(1 + omEscalation, year - 1);
    const degFactor = Math.pow(1 - degradationRate, year - 1);

    const yearGeneration = annualGeneration * degFactor;
    const yearTariff = tariff * escalationFactor;
    const yearOMCost = systemSize * omCostPerKw * omFactor;

    const utilityCost = annualConsumption * yearTariff;
    const solarSaving = yearGeneration * yearTariff;
    const yearNetSaving = solarSaving - yearOMCost;

    years.push(year);
    annualSavings.push(yearNetSaving);
    utilityCosts.push(utilityCost);
    solarCosts.push(utilityCost - yearNetSaving);

    cumulativeUtility += utilityCost / Math.pow(1 + discountRate, year - 1);
    cumulativeSolar += (utilityCost - yearNetSaving) / Math.pow(1 + discountRate, year - 1);
    cumulativeSavings += yearNetSaving / Math.pow(1 + discountRate, year - 1);
  }

  const roi = ((cumulativeSavings - netInvestment) / netInvestment) * 100;

  // Payback period
  let paybackYear = null;
  let cumulative = 0;
  for (let year = 1; year <= projectLife; year++) {
    const escalationFactor = Math.pow(1 + tariffEscalation, year - 1);
    const omFactor = Math.pow(1 + omEscalation, year - 1);
    const degFactor = Math.pow(1 - degradationRate, year - 1);
    const yearGeneration = annualGeneration * degFactor;
    const yearTariff = tariff * escalationFactor;
    const yearOMCost = systemSize * omCostPerKw * omFactor;
    const yearNetSaving = (yearGeneration * yearTariff) - yearOMCost;

    cumulative += yearNetSaving;
    if (cumulative >= netInvestment && paybackYear === null) {
      // Interpolate
      const prevCumulative = cumulative - yearNetSaving;
      const fraction = (netInvestment - prevCumulative) / yearNetSaving;
      paybackYear = year - 1 + fraction;
    }
  }

  const lifetimeSavings = cumulativeSavings;
  const co2Offset = annualGeneration * 0.82; // kg CO2 per kWh
  const treesPlanted = co2Offset * 0.045;

  return {
    systemSize,
    annualGeneration,
    grossCost,
    subsidy,
    netInvestment,
    paybackYear,
    roi,
    lifetimeSavings,
    annualSavings,
    utilityCosts,
    solarCosts,
    years,
    co2Offset,
    treesPlanted,
    annualConsumption
  };
}

function populateResults(results) {
  document.getElementById('res-system-size').textContent = results.systemSize.toFixed(2);
  document.getElementById('res-annual-generation').textContent = results.annualGeneration.toFixed(0);
  document.getElementById('res-net-investment').textContent = `₹${results.netInvestment.toLocaleString('en-IN')}`;
  document.getElementById('res-payback').textContent = results.paybackYear ? results.paybackYear.toFixed(1) : '-';
  document.getElementById('res-roi').textContent = results.roi.toFixed(1);
  document.getElementById('res-savings-lifetime').textContent = `₹${results.lifetimeSavings.toLocaleString('en-IN')}`;

  // Comparison section
  document.getElementById('comp-before-consumption').textContent = `${results.annualConsumption.toFixed(0)} kWh`;
  const annualBill = results.annualConsumption * state.energy.tariff;
  document.getElementById('comp-before-cost').textContent = `₹${annualBill.toLocaleString('en-IN')}`;
  document.getElementById('comp-before-monthly').textContent = `₹${(annualBill / 12).toLocaleString('en-IN')}`;

  document.getElementById('comp-after-generation').textContent = `${results.annualGeneration.toFixed(0)} kWh`;
  const remainingConsumption = Math.max(0, results.annualConsumption - results.annualGeneration);
  document.getElementById('comp-after-grid').textContent = `${remainingConsumption.toFixed(0)} kWh`;
  document.getElementById('comp-after-cost').textContent = `₹${(remainingConsumption * state.energy.tariff).toLocaleString('en-IN')}`;

  document.getElementById('comp-savings').textContent = `₹${(annualBill - (remainingConsumption * state.energy.tariff)).toLocaleString('en-IN')}`;
  document.getElementById('comp-co2').textContent = `${results.co2Offset.toFixed(0)} kg CO2`;
  document.getElementById('comp-trees').textContent = `${results.treesPlanted.toFixed(0)} trees/yr`;
}

function drawCharts(results) {
  // Energy Chart
  const energyCtx = document.getElementById('energy-chart');
  if (energyCtx) {
    if (energyChart) energyChart.destroy();
    energyChart = new Chart(energyCtx, {
      type: 'bar',
      data: {
        labels: ['Annual Consumption', 'Annual Generation'],
        datasets: [{
          label: 'kWh',
          data: [results.annualConsumption, results.annualGeneration],
          backgroundColor: ['#9ca3af', '#b5111a'],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });
  }

  // Financial Chart
  const financialCtx = document.getElementById('financial-chart');
  if (financialCtx) {
    if (financialChart) financialChart.destroy();

    const labels = [];
    const utilityData = [];
    const solarData = [];
    let cumUtility = 0;
    let cumSolar = results.netInvestment;

    for (let i = 0; i < Math.min(results.years.length, 25); i++) {
      if (i % 5 === 0 || i === results.years.length - 1) {
        labels.push(`Year ${results.years[i]}`);
      } else {
        labels.push('');
      }
      cumUtility += results.utilityCosts[i];
      cumSolar += results.solarCosts[i];
      utilityData.push(cumUtility);
      solarData.push(cumSolar);
    }

    financialChart = new Chart(financialCtx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Traditional Utility',
            data: utilityData,
            borderColor: '#9ca3af',
            backgroundColor: 'rgba(156, 163, 175, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 2
          },
          {
            label: 'Solar',
            data: solarData,
            borderColor: '#b5111a',
            backgroundColor: 'rgba(181, 17, 26, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return '₹' + (value / 100000).toFixed(1) + 'L';
              }
            }
          }
        }
      }
    });
  }
}

function resetCalculator() {
  location.reload();
}
