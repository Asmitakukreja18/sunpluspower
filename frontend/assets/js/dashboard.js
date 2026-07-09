/**
 * SunPlus Power Customer Dashboard SPA Controller
 */

let activePanel = "overview";

document.addEventListener("DOMContentLoaded", () => {
  // Bind form submissions
  const loginForm = document.getElementById("customer-login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", handleCustomerLogin);
  }

  const profileForm = document.getElementById("profile-update-form");
  if (profileForm) {
    profileForm.addEventListener("submit", saveCustomerProfile);
  }

  // Detect initial route
  checkAuthAndRoute();

  // Listen to browser forward/back buttons
  window.addEventListener("popstate", () => {
    checkAuthAndRoute();
  });
});

/** Auth validations */
function checkAuthAndRoute() {
  const session = JSON.parse(localStorage.getItem("sunplus_customer_session") || "null");
  const authView = document.getElementById("customer-auth-view");
  const dashView = document.getElementById("customer-dashboard-view");

  if (!session) {
    if (authView) authView.classList.remove("hidden");
    if (dashView) dashView.classList.add("hidden");
    return;
  }

  // Authenticated
  if (authView) authView.classList.add("hidden");
  if (dashView) dashView.classList.remove("hidden");

  // Populate user badge
  document.getElementById("user-email-badge").textContent = session.email;

  // Determine active panel from pathname
  const path = window.location.pathname;
  let panel = "overview";
  if (path.includes("/calculations")) panel = "calculations";
  else if (path.includes("/scenarios")) panel = "scenarios";
  else if (path.includes("/requests")) panel = "requests";
  else if (path.includes("/profile")) panel = "profile";

  showPanel(panel);
  loadDashboardData(session);
}

function handleCustomerLogin(e) {
  e.preventDefault();
  const email = document.getElementById("auth-email").value;
  const pass = document.getElementById("auth-password").value;

  if (!email || !pass) return;

  const btn = document.getElementById("auth-btn");
  btn.disabled = true;
  btn.innerHTML = `<span class="material-symbols-outlined animate-spin text-sm">autorenew</span> Connecting...`;

  setTimeout(() => {
    // Save customer session locally (mock auth)
    const session = {
      email,
      name: email.split("@")[0].toUpperCase(),
      phone: "+91 99999 88888",
      zip: "226010",
      pan: "LKNM16523D",
      loggedInAt: new Date().toISOString()
    };
    localStorage.setItem("sunplus_customer_session", JSON.stringify(session));
    
    // Seed initial mock data for the user if empty
    seedMockCustomerData(email);

    btn.disabled = false;
    btn.innerHTML = `Sign In <span class="material-symbols-outlined text-sm">login</span>`;

    // Navigate to dashboard overview
    history.pushState({ view: "dashboard" }, "", "/dashboard");
    checkAuthAndRoute();
  }, 1000);
}

function handleCustomerLogout() {
  localStorage.removeItem("sunplus_customer_session");
  history.pushState({ view: "login" }, "", "/dashboard");
  checkAuthAndRoute();
}

/** Dashboard Views Sizer */
function showPanel(panelName) {
  const panels = document.querySelectorAll(".dashboard-panel");
  panels.forEach(p => p.classList.add("hidden"));

  const target = document.getElementById(`panel-${panelName}`);
  if (target) target.classList.remove("hidden");

  // Highlight active sidebar links
  const btnIds = ["overview", "calculations", "scenarios", "requests", "profile"];
  btnIds.forEach(id => {
    const btn = document.getElementById(`side-nav-${id}`);
    if (btn) {
      if (id === panelName) {
        btn.className = "w-full text-left px-4 py-3 rounded text-sm font-bold text-primary bg-[#ffdad6] transition-colors flex items-center gap-3 sidebar-active";
      } else {
        btn.className = "w-full text-left px-4 py-3 rounded text-sm font-semibold text-secondary hover:bg-surface-container-low transition-colors flex items-center gap-3";
      }
    }
  });

  activePanel = panelName;
}

function navigateDashboard(path) {
  history.pushState({ view: "dashboard", path }, "", path);
  checkAuthAndRoute();
}

/** Seed demo user datasets */
function seedMockCustomerData(email) {
  const calcsKey = `customer_calcs_${email}`;
  const reqsKey = `customer_reqs_${email}`;

  if (!localStorage.getItem(calcsKey)) {
    const defaultCalcs = [
      {
        id: "CALC-92841",
        name: "Residential Villa Sizing",
        date: "2026-07-08",
        size: "15 kW DC",
        payback: "4.8 Years",
        status: "Completed",
        inputs: {
          name: "Residential Villa Sizing",
          location: "uttar pradesh",
          monthly_bill: 15000,
          monthly_units: 2000,
          available_area: 1800,
          grid_mode: "rooftop",
          panel_tier: "high",
          storage_kwh: 0,
          finance_mode: "cash",
          tariff_escalation: 4.0,
          om_escalation: 3.5,
          discount_rate: 8.0,
          net: 750000,
          gross: 828000,
          subsidy: 78000,
          firstYearSavings: 156000
        }
      }
    ];
    localStorage.setItem(calcsKey, JSON.stringify(defaultCalcs));
  }

  if (!localStorage.getItem(reqsKey)) {
    const defaultReqs = [
      {
        id: "REQ-74291",
        subject: "Site Survey Request",
        date: "2026-07-09",
        status: "In Progress",
        description: "Assessing concrete roof load limits for 15 kW TOPCon array sizing."
      }
    ];
    localStorage.setItem(reqsKey, JSON.stringify(defaultReqs));
  }
}

/** Load records into layout rows */
function loadDashboardData(session) {
  const calcsKey = `customer_calcs_${session.email}`;
  const reqsKey = `customer_reqs_${session.email}`;

  const calcs = JSON.parse(localStorage.getItem(calcsKey) || "[]");
  const reqs = JSON.parse(localStorage.getItem(reqsKey) || "[]");

  // Overview metrics
  document.getElementById("stat-calcs").textContent = calcs.length;
  document.getElementById("stat-surveys").textContent = reqs.filter(r => r.status === "Completed").length;
  document.getElementById("stat-requests").textContent = reqs.filter(r => r.status !== "Completed").length;

  // Render Saved Calculations list
  const historyTbody = document.getElementById("calculations-history-rows");
  if (historyTbody) {
    if (calcs.length === 0) {
      historyTbody.innerHTML = `
        <tr>
          <td colspan="6" class="p-8 text-center text-secondary italic">No calculations saved. Start sizing configurations in the modeling studio!</td>
        </tr>
      `;
    } else {
      historyTbody.innerHTML = calcs.map(item => `
        <tr class="border-b border-surface-container">
          <td class="p-4 font-bold text-on-surface">${item.id}</td>
          <td class="p-4">${item.name}</td>
          <td class="p-4 text-xs text-secondary">${item.date}</td>
          <td class="p-4 font-semibold text-primary">${item.size}</td>
          <td class="p-4"><span class="text-[10px] bg-green-600/10 text-green-700 px-2 py-0.5 rounded font-bold">${item.status}</span></td>
          <td class="p-4 text-right space-x-2">
            <button onclick="loadCalcIntoStudio('${session.email}', '${item.id}')" class="text-xs text-primary font-bold hover:underline">Open Model</button>
            <button onclick="deleteCalculation('${session.email}', '${item.id}')" class="text-xs text-red-600 font-bold hover:underline">Delete</button>
          </td>
        </tr>
      `).join("");
    }
  }

  // Render Comparisons Scenarios
  const scenariosGrid = document.getElementById("saved-scenarios-cards");
  if (scenariosGrid) {
    if (calcs.length === 0) {
      scenariosGrid.innerHTML = `
        <div class="col-span-2 p-6 bg-surface-container-low rounded border border-surface-container text-center italic text-secondary">
          No comparison scenarios available. Run calculations to save profiles.
        </div>
      `;
    } else {
      scenariosGrid.innerHTML = calcs.map(item => `
        <div class="p-6 bg-white border border-surface-container rounded-lg shadow-sm space-y-3">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-bold text-on-surface">${item.name}</h4>
              <span class="text-[10px] text-secondary font-mono">${item.id}</span>
            </div>
            <span class="text-xs font-bold text-primary">${item.size}</span>
          </div>
          <div class="text-xs space-y-1 text-secondary border-t border-surface-container pt-3">
            <div class="flex justify-between"><span>Payback Period:</span><span class="font-bold text-on-surface">${item.payback}</span></div>
            <div class="flex justify-between"><span>Net Cost Estimate:</span><span class="font-bold text-on-surface">Rs.${(item.inputs.net || 0).toLocaleString("en-IN")}</span></div>
          </div>
          <button onclick="loadCalcIntoStudio('${session.email}', '${item.id}')" class="w-full text-center py-2 bg-surface-container-low border border-surface-container-highest text-xs font-bold rounded hover:bg-surface-container transition-colors">
            Load Studio Workspace
          </button>
        </div>
      `).join("");
    }
  }

  // Render Requests Tracker panel
  const reqTimeline = document.getElementById("panel-requests");
  if (reqTimeline && reqs.length > 0) {
    const activeReq = reqs[0];
    document.getElementById("survey-title").textContent = `${activeReq.subject} (${activeReq.id})`;
    document.getElementById("survey-status").textContent = activeReq.status;
  }

  // Set Profile fields
  document.getElementById("profile-name").value = session.name || "";
  document.getElementById("profile-phone").value = session.phone || "";
  document.getElementById("profile-zip").value = session.zip || "";
  document.getElementById("profile-pan").value = session.pan || "";
}

/** Actions */
function deleteCalculation(email, id) {
  const calcsKey = `customer_calcs_${email}`;
  let calcs = JSON.parse(localStorage.getItem(calcsKey) || "[]");
  calcs = calcs.filter(c => c.id !== id);
  localStorage.setItem(calcsKey, JSON.stringify(calcs));
  
  const session = JSON.parse(localStorage.getItem("sunplus_customer_session"));
  loadDashboardData(session);
  window.showToast("Calculation model deleted.", "success");
}

function loadCalcIntoStudio(email, id) {
  const calcsKey = `customer_calcs_${email}`;
  const calcs = JSON.parse(localStorage.getItem(calcsKey) || "[]");
  const model = calcs.find(c => c.id === id);
  if (!model) return;

  // Load into calculator workspace draft
  localStorage.setItem("sunplus_calculator_draft", JSON.stringify({
    ...model.inputs,
    currentStep: 6
  }));

  // Navigate to analysis workspace
  window.location.href = "/analysis/overview";
}

function saveCustomerProfile(e) {
  e.preventDefault();
  const session = JSON.parse(localStorage.getItem("sunplus_customer_session"));
  if (!session) return;

  session.name = document.getElementById("profile-name").value;
  session.phone = document.getElementById("profile-phone").value;
  session.zip = document.getElementById("profile-zip").value;
  session.pan = document.getElementById("profile-pan").value;

  localStorage.setItem("sunplus_customer_session", JSON.stringify(session));
  window.showToast("Profile settings updated successfully.", "success", "profile-feedback");
}

function toggleAuthMode() {
  const loginForm = document.getElementById("customer-login-form");
  const authTitle = document.querySelector("#customer-auth-view h2");
  
  if (loginForm.dataset.mode === "signup") {
    loginForm.dataset.mode = "login";
    authTitle.textContent = "Customer Portal Login";
    document.querySelector("#customer-login-form button").innerHTML = `Sign In <span class="material-symbols-outlined text-sm">login</span>`;
    document.querySelector("#customer-auth-view button[onclick='toggleAuthMode()']").textContent = "Don't have an account? Sign Up";
  } else {
    loginForm.dataset.mode = "signup";
    authTitle.textContent = "Customer Portal Signup";
    document.querySelector("#customer-login-form button").innerHTML = `Create Account <span class="material-symbols-outlined text-sm">person_add</span>`;
    document.querySelector("#customer-auth-view button[onclick='toggleAuthMode()']").textContent = "Already have an account? Sign In";
  }
}

// Expose globally
window.handleCustomerLogin = handleCustomerLogin;
window.handleCustomerLogout = handleCustomerLogout;
window.navigateDashboard = navigateDashboard;
window.deleteCalculation = deleteCalculation;
window.loadCalcIntoStudio = loadCalcIntoStudio;
window.saveCustomerProfile = saveCustomerProfile;
window.toggleAuthMode = toggleAuthMode;
