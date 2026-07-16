/**
 * SunPlus Power API Client Helper
 */

const API_BASE = "https://sunplus-backend.onrender.com/api";

class ApiClient {
  constructor() {
    this.tokenKey = "sunplus_admin_token";
  }

  // Get current JWT token
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  // Store token
  setToken(token) {
    localStorage.setItem(this.tokenKey, token);
  }

  // Clear token (logout)
  clearToken() {
    localStorage.removeItem(this.tokenKey);
  }

  // Check if admin is authenticated
  isAuthenticated() {
    return !!this.getToken();
  }

  // Show a global loading spinner if present in DOM
  showLoader() {
    const loader = document.getElementById("global-loader");
    if (loader) {
      loader.classList.remove("hidden");
    }
  }

  // Hide global loader
  hideLoader() {
    const loader = document.getElementById("global-loader");
    if (loader) {
      loader.classList.add("hidden");
    }
  }

  /**
   * Universal fetch wrapper
   * @param {string} endpoint - API path (e.g. "/leads")
   * @param {object} options - Fetch option configuration
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    
    // Set headers
    const headers = { ...options.headers };
    
    // Check if sending FormData (don't set Content-Type header manually for FormData)
    const isFormData = options.body instanceof FormData;
    if (!isFormData && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }

    // Attach JWT Authorization if logged in
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers
    };

    this.showLoader();

    try {
      const response = await fetch(url, config);
      
      // Handle unauthorized (expired JWT)
      if (response.status === 401) {
        // Only redirect to login if we are inside the admin dashboard
        if (window.location.pathname.includes("/admin/") && !window.location.pathname.includes("login.html")) {
          this.clearToken();
          window.location.href = "/admin/login.html?expired=true";
          return;
        }
      }

      // Check if response is No Content (244 DELETE success)
      if (response.status === 204) {
        this.hideLoader();
        return { success: true };
      }

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || `API Request failed with status ${response.status}`);
      }

      this.hideLoader();
      return data;
    } catch (error) {
      this.hideLoader();
      
      // Frontend Demo Submission Adapter Fallback
      if (config.method === "POST") {
        console.warn(`Backend connection failed for ${endpoint}. Activating frontend demo submission adapter...`, error);
        
        // Simulate network latency
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Parse submission data for local storage representation
        let submissionData = {};
        if (options.body instanceof FormData) {
          for (let pair of options.body.entries()) {
            submissionData[pair[0]] = pair[1] instanceof File ? pair[1].name : pair[1];
          }
        } else if (typeof options.body === "string") {
          try {
            submissionData = JSON.parse(options.body);
          } catch(e) {
            submissionData = { raw: options.body };
          }
        }
        
        submissionData.demoMode = true;
        submissionData.timestamp = new Date().toISOString();
        
        // Persist locally in localStorage
        const demoKey = `demo_submissions_${endpoint.replace(/\//g, '_')}`;
        const list = JSON.parse(localStorage.getItem(demoKey) || "[]");
        list.push(submissionData);
        localStorage.setItem(demoKey, JSON.stringify(list));
        
        return {
          success: true,
          demoMode: true,
          message: "Processed locally in demo mode (Offline fallback)",
          data: submissionData
        };
      }
      
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }

  // HTTP GET Wrapper
  async get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  }

  // HTTP POST Wrapper
  async post(endpoint, body, isMultipart = false) {
    return this.request(endpoint, {
      method: "POST",
      body: isMultipart ? body : JSON.stringify(body)
    });
  }

  // HTTP PUT Wrapper
  async put(endpoint, body) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(body)
    });
  }

  // HTTP DELETE Wrapper
  async delete(endpoint) {
    return this.request(endpoint, { method: "DELETE" });
  }
}

// Global instance
const api = new ApiClient();
