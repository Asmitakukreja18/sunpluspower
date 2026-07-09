/**
 * SunPlus Power Admin Panel Operations Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  // Check auth state for protected dashboard pages
  const isLoginPage = window.location.pathname.includes("login.html");
  if (!isLoginPage && !api.isAuthenticated()) {
    window.location.href = "login.html";
    return;
  }

  // 1. Login Handler
  setupAdminLogin();

  // 2. Dashboard General Stats
  if (document.getElementById("admin-dashboard-view")) {
    loadDashboardStats();
  }

  // 3. Submissions Page Binding
  if (document.getElementById("submissions-view")) {
    loadSubmissionsData();
  }

  // 4. Projects CRUD Page Binding
  if (document.getElementById("projects-crud-view")) {
    loadAdminProjects();
    setupCRUDModal("project-form", "projects");
  }

  // 5. Blogs CRUD Page Binding
  if (document.getElementById("blogs-crud-view")) {
    loadAdminBlogs();
    setupCRUDModal("blog-form", "blogs");
  }

  // 6. Careers CRUD Page Binding
  if (document.getElementById("careers-crud-view")) {
    loadAdminCareers();
    setupCRUDModal("career-form", "careers");
  }
});

// --- Authentication Operations ---

function setupAdminLogin() {
  const loginForm = document.getElementById("admin-login-form");
  if (!loginForm) return;

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const btn = loginForm.querySelector("button");
    const originalText = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> Logging in...`;

    try {
      const response = await api.post("/admin/login", { email, password });
      api.setToken(response.access_token);
      window.location.href = "dashboard.html";
    } catch (err) {
      window.showToast("Login failed. Check your admin credentials.", "error", "login-error-container");
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  });
}

function adminLogout() {
  api.clearToken();
  window.location.href = "login.html";
}
window.adminLogout = adminLogout;

// --- Dashboard Operations ---

async function loadDashboardStats() {
  try {
    const stats = await api.get("/admin/dashboard-stats");
    setText("stat-leads", stats.leads_count);
    setText("stat-calc", stats.calculator_submissions_count);
    setText("stat-dist", stats.distributor_applications_count);
    setText("stat-tickets", stats.complaints_count);
    setText("stat-projects", stats.projects_count);
    setText("stat-jobs", stats.careers_count);
  } catch (err) {
    window.showToast("Failed to fetch dashboard metrics.", "error");
  }
}

// --- Submissions Listing & Updates ---

let currentSubmissionsTab = "leads";

function switchSubmissionsTab(tabName) {
  currentSubmissionsTab = tabName;
  
  // Toggle tab buttons styles
  document.querySelectorAll(".sub-tab-btn").forEach(btn => {
    btn.classList.remove("border-primary", "text-on-surface");
    btn.classList.add("border-transparent", "text-secondary");
  });
  document.getElementById(`tab-${tabName}`).classList.add("border-primary", "text-on-surface");
  document.getElementById(`tab-${tabName}`).classList.remove("border-transparent", "text-secondary");

  // Toggle table views container
  document.querySelectorAll(".submission-table-container").forEach(table => {
    table.classList.add("hidden");
  });
  document.getElementById(`${tabName}-table-container`).classList.remove("hidden");
}
window.switchSubmissionsTab = switchSubmissionsTab;

async function loadSubmissionsData() {
  try {
    // 1. Fetch leads
    const leads = await api.get("/admin/leads");
    renderLeadsTable(leads);

    // 2. Fetch solar calculator entries
    const calcs = await api.get("/admin/calculator-submissions");
    renderCalculatorTable(calcs);

    // 3. Fetch distributors
    const dists = await api.get("/admin/distributor-applications");
    renderDistributorsTable(dists);

    // 4. Fetch warranties
    const warranties = await api.get("/admin/warranty-registrations");
    renderWarrantiesTable(warranties);

    // 5. Fetch complaints
    const complaints = await api.get("/admin/complaints");
    renderComplaintsTable(complaints);

    // 6. Fetch job applications
    const jobApps = await api.get("/admin/job-applications");
    renderJobAppsTable(jobApps);

  } catch (err) {
    window.showToast("Failed to populate submissions grids.", "error");
  }
}

function renderLeadsTable(leads) {
  const body = document.getElementById("leads-table-body");
  if (!body) return;
  body.innerHTML = leads.map(l => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4 font-bold">${l.name}</td>
      <td class="p-4">${l.email}<br><small class="text-secondary">${l.phone}</small></td>
      <td class="p-4 font-semibold text-secondary">${l.company || 'N/A'}</td>
      <td class="p-4"><b>${l.subject}</b><br><small class="text-secondary">${l.message}</small></td>
      <td class="p-4"><span class="chip">${l.source_page}</span></td>
      <td class="p-4">
        <select onchange="updateSubmissionStatus('leads', ${l.id}, this.value)" class="form-select text-sm p-1.5 border border-outline rounded bg-white">
          <option value="new" ${l.status === 'new' ? 'selected' : ''}>New</option>
          <option value="contacted" ${l.status === 'contacted' ? 'selected' : ''}>Contacted</option>
          <option value="closed" ${l.status === 'closed' ? 'selected' : ''}>Closed</option>
        </select>
      </td>
    </tr>
  `).join("");
}

function renderCalculatorTable(calcs) {
  const body = document.getElementById("calculator-table-body");
  if (!body) return;
  body.innerHTML = calcs.map(c => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4 font-bold">${c.name}</td>
      <td class="p-4">${c.email}<br><small class="text-secondary">${c.phone || 'No Phone'}</small></td>
      <td class="p-4 font-mono font-bold">₹${c.monthly_bill.toLocaleString()}</td>
      <td class="p-4">State: ${c.location}<br>Type: <span class="chip">${c.install_type}</span></td>
      <td class="p-4 font-bold text-primary">${c.calculated_system_size_kw} kW</td>
      <td class="p-4 font-semibold">Net Cost: ₹${c.net_cost.toLocaleString()}<br><small class="text-secondary">Savings: ₹${c.annual_savings.toLocaleString()}/yr</small></td>
      <td class="p-4 text-center font-bold">${c.payback_years} Yrs</td>
    </tr>
  `).join("");
}

function renderDistributorsTable(dists) {
  const body = document.getElementById("distributor-table-body");
  if (!body) return;
  body.innerHTML = dists.map(d => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4"><b>${d.company_name}</b><br><small class="text-secondary">By: ${d.contact_person}</small></td>
      <td class="p-4">${d.email}<br><small class="text-secondary">${d.phone}</small></td>
      <td class="p-4 font-semibold">${d.region}</td>
      <td class="p-4 text-center">${d.years_in_business} Yrs</td>
      <td class="p-4"><small class="text-secondary">${d.message}</small></td>
      <td class="p-4">
        <select onchange="updateSubmissionStatus('distributor-applications', ${d.id}, this.value)" class="form-select text-sm p-1.5 border border-outline rounded bg-white">
          <option value="pending" ${d.status === 'pending' ? 'selected' : ''}>Pending</option>
          <option value="approved" ${d.status === 'approved' ? 'selected' : ''}>Approved</option>
          <option value="rejected" ${d.status === 'rejected' ? 'selected' : ''}>Rejected</option>
        </select>
      </td>
    </tr>
  `).join("");
}

function renderWarrantiesTable(w) {
  const body = document.getElementById("warranty-table-body");
  if (!body) return;
  body.innerHTML = w.map(x => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4 font-bold">${x.customer_name}</td>
      <td class="p-4">${x.email}<br><small class="text-secondary">${x.phone}</small></td>
      <td class="p-4"><span class="chip">${x.product_type}</span></td>
      <td class="p-4 font-mono font-semibold">${x.serial_or_project_id}</td>
      <td class="p-4">${x.installation_date}</td>
      <td class="p-4 text-secondary">${x.installer_name}</td>
    </tr>
  `).join("");
}

function renderComplaintsTable(complaints) {
  const body = document.getElementById("complaints-table-body");
  if (!body) return;
  body.innerHTML = complaints.map(c => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4 font-bold">${c.name}</td>
      <td class="p-4">${c.email}<br><small class="text-secondary">${c.phone}</small></td>
      <td class="p-4 font-mono font-semibold">${c.project_or_product_id}</td>
      <td class="p-4"><span class="chip">${c.category}</span></td>
      <td class="p-4"><small class="text-secondary">${c.description}</small></td>
      <td class="p-4">
        ${c.photo_url ? `<a href="${c.photo_url}" target="_blank" class="text-primary font-bold hover:underline">View Photo</a>` : '<span class="text-secondary">None</span>'}
      </td>
      <td class="p-4">
        <select onchange="updateSubmissionStatus('complaints', ${c.id}, this.value)" class="form-select text-sm p-1.5 border border-outline rounded bg-white">
          <option value="open" ${c.status === 'open' ? 'selected' : ''}>Open</option>
          <option value="in_progress" ${c.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
          <option value="resolved" ${c.status === 'resolved' ? 'selected' : ''}>Resolved</option>
        </select>
      </td>
    </tr>
  `).join("");
}

function renderJobAppsTable(apps) {
  const body = document.getElementById("job-applications-table-body");
  if (!body) return;
  body.innerHTML = apps.map(a => `
    <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
      <td class="p-4 font-bold">${a.name}</td>
      <td class="p-4">${a.email}<br><small class="text-secondary">${a.phone}</small></td>
      <td class="p-4">ID Reference: ${a.career_id || 'General Application'}</td>
      <td class="p-4">
        <a href="${a.resume_url}" target="_blank" class="btn-primary p-1.5 text-xs rounded hover:opacity-90 inline-flex items-center gap-1">
          <span class="material-symbols-outlined text-[14px]">download</span>
          Open Resume
        </a>
      </td>
      <td class="p-4"><small class="text-secondary">${a.cover_letter || 'No Cover Letter'}</small></td>
    </tr>
  `).join("");
}

async function updateSubmissionStatus(entity, id, newStatus) {
  try {
    await api.request(`/admin/${entity}/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus })
    });
    window.showToast("Status updated successfully.", "success");
  } catch (err) {
    window.showToast("Failed to alter status code.", "error");
  }
}
window.updateSubmissionStatus = updateSubmissionStatus;


// --- CRUD operations for Projects ---

async function loadAdminProjects() {
  const body = document.getElementById("projects-crud-table-body");
  if (!body) return;

  try {
    const list = await api.get("/admin/projects");
    body.innerHTML = list.map(p => `
      <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
        <td class="p-4 font-bold">${p.name}</td>
        <td class="p-4 font-bold text-primary">${p.capacity_mw} MW</td>
        <td class="p-4">${p.location}, ${p.state}</td>
        <td class="p-4"><span class="chip">${p.status}</span></td>
        <td class="p-4 text-center">${p.commissioning_date}</td>
        <td class="p-4 flex gap-2 justify-center">
          <button onclick="editCRUDItem('projects', ${p.id}, ${JSON.stringify(p).replace(/"/g, '&quot;')})" class="btn-secondary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">edit</span> Edit
          </button>
          <button onclick="deleteCRUDItem('projects', ${p.id})" class="btn-primary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">delete</span> Delete
          </button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    window.showToast("Failed to fetch project listings.", "error");
  }
}

// --- CRUD operations for Blogs ---

async function loadAdminBlogs() {
  const body = document.getElementById("blogs-crud-table-body");
  if (!body) return;

  try {
    const list = await api.get("/admin/blogs");
    body.innerHTML = list.map(b => `
      <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
        <td class="p-4 font-bold">${b.title}</td>
        <td class="p-4 font-mono text-xs text-secondary">${b.slug}</td>
        <td class="p-4">${b.author}</td>
        <td class="p-4">
          <span class="status-dot ${b.published ? 'active' : 'critical'}"></span>
          ${b.published ? 'Published' : 'Draft'}
        </td>
        <td class="p-4 text-center">${b.published_at ? b.published_at.split('T')[0] : 'N/A'}</td>
        <td class="p-4 flex gap-2 justify-center">
          <button onclick="editCRUDItem('blogs', ${b.id}, ${JSON.stringify(b).replace(/"/g, '&quot;')})" class="btn-secondary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">edit</span> Edit
          </button>
          <button onclick="deleteCRUDItem('blogs', ${b.id})" class="btn-primary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">delete</span> Delete
          </button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    window.showToast("Failed to retrieve blog listings.", "error");
  }
}

// --- CRUD operations for Careers ---

async function loadAdminCareers() {
  const body = document.getElementById("careers-crud-table-body");
  if (!body) return;

  try {
    const list = await api.get("/admin/careers");
    body.innerHTML = list.map(c => `
      <tr class="border-b border-surface-container hover:bg-surface-container-low transition-colors">
        <td class="p-4 font-bold">${c.title}</td>
        <td class="p-4 font-semibold text-secondary">${c.department}</td>
        <td class="p-4">${c.location}</td>
        <td class="p-4">${c.experience_required}</td>
        <td class="p-4">
          <span class="status-dot ${c.is_active ? 'active' : 'critical'}"></span>
          ${c.is_active ? 'Active' : 'Closed'}
        </td>
        <td class="p-4 flex gap-2 justify-center">
          <button onclick="editCRUDItem('careers', ${c.id}, ${JSON.stringify(c).replace(/"/g, '&quot;')})" class="btn-secondary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">edit</span> Edit
          </button>
          <button onclick="deleteCRUDItem('careers', ${c.id})" class="btn-primary px-3 py-1.5 text-xs font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">delete</span> Delete
          </button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    window.showToast("Failed to list job positions.", "error");
  }
}


// --- CRUD Modal Bindings & Modifiers ---

function toggleCRUDModal(entity, show = true) {
  const modal = document.getElementById(`${entity}-modal`);
  if (!modal) return;
  
  if (show) {
    modal.classList.remove("hidden");
    // Clear forms for new entries using the singular form (e.g., project-form, project-id)
    const singularEntity = entity.slice(0, -1);
    const formEl = document.getElementById(`${singularEntity}-form`);
    if (formEl) formEl.reset();
    const idEl = document.getElementById(`${singularEntity}-id`);
    if (idEl) idEl.value = "";
    
    const titleEl = document.getElementById(`modal-${entity}-title`);
    if (titleEl) {
      titleEl.innerText = `New ${entity.charAt(0).toUpperCase() + entity.slice(1, -1)}`;
    }
  } else {
    modal.classList.add("hidden");
  }
}
window.toggleCRUDModal = toggleCRUDModal;

function setupCRUDModal(formId, entity) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const itemId = document.getElementById(`${entity.slice(0,-1)}-id`).value;
    const formData = new FormData(form);
    
    // Convert to JSON payload
    let payload = {};
    formData.forEach((value, key) => {
      // Convert published checkbox or active to boolean
      if (key === "published" || key === "is_active") {
        payload[key] = value === "on" || value === "true";
      } else if (key === "capacity_mw") {
        payload[key] = parseFloat(value);
      } else {
        payload[key] = value;
      }
    });

    // Fallbacks for checkboxes if not present in FormData
    if (entity === "blogs" && !payload.hasOwnProperty("published")) {
      payload["published"] = false;
    }
    if (entity === "careers" && !payload.hasOwnProperty("is_active")) {
      payload["is_active"] = false;
    }

    try {
      if (itemId) {
        // Edit Operation
        await api.put(`/admin/${entity}/${itemId}`, payload);
        window.showToast("Item updated successfully.", "success");
      } else {
        // Create Operation
        await api.post(`/admin/${entity}`, payload);
        window.showToast("Item created successfully.", "success");
      }
      
      toggleCRUDModal(entity, false);
      
      // Reload matching dataset
      if (entity === "projects") loadAdminProjects();
      if (entity === "blogs") loadAdminBlogs();
      if (entity === "careers") loadAdminCareers();

    } catch (err) {
      window.showToast(err.message || "Failed to save CRUD modifications.", "error");
    }
  });
}

function editCRUDItem(entity, id, data) {
  // Show Modal
  toggleCRUDModal(entity, true);
  
  const singularEntity = entity.slice(0, -1);
  
  // Set ID and update header label
  document.getElementById(`${singularEntity}-id`).value = id;
  const titleEl = document.getElementById(`modal-${entity}-title`);
  if (titleEl) {
    titleEl.innerText = `Edit ${entity.charAt(0).toUpperCase() + entity.slice(1, -1)}`;
  }

  // Populate form elements
  const form = document.getElementById(`${singularEntity}-form`);
  if (!form) return;
  
  for (const [key, val] of Object.entries(data)) {
    const input = form.elements[key];
    if (!input) continue;

    if (input.type === "checkbox") {
      input.checked = !!val;
    } else if (input.type === "select-one") {
      input.value = val;
    } else if (input.type === "date" && val) {
      // If date comes with time/timezone, format it to YYYY-MM-DD
      input.value = val.split("T")[0];
    } else {
      input.value = val;
    }
  }
}
window.editCRUDItem = editCRUDItem;

async function deleteCRUDItem(entity, id) {
  if (!confirm("Are you absolutely sure you want to delete this item?")) return;

  try {
    await api.delete(`/admin/${entity}/${id}`);
    window.showToast("Item deleted successfully.", "success");
    
    if (entity === "projects") loadAdminProjects();
    if (entity === "blogs") loadAdminBlogs();
    if (entity === "careers") loadAdminCareers();
  } catch (err) {
    window.showToast("Failed to delete database entry.", "error");
  }
}
window.deleteCRUDItem = deleteCRUDItem;


// --- Helpers ---

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.innerText = text;
}
