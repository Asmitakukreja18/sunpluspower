/**
 * SunPlus Power Public Forms Handlers
 */

document.addEventListener("DOMContentLoaded", () => {
  // Bind Contact form
  setupFormSubmit("contact-form", "/leads", (data) => {
    return {
      name: data.name,
      email: data.email,
      phone: data.phone,
      company: data.company || null,
      subject: data.subject || "General Inquiry",
      message: data.message,
      source_page: window.location.pathname
    };
  });

  // Bind Distributor form
  setupFormSubmit("distributor-form", "/distributor-applications", (data) => {
    return {
      company_name: data.company_name,
      contact_person: data.contact_person,
      region: data.region,
      business_type: data.business_type,
      years_in_business: parseInt(data.years_in_business) || 0,
      phone: data.phone,
      email: data.email,
      message: data.message
    };
  });

  // Bind Warranty form
  setupFormSubmit("warranty-form", "/warranty-registrations", (data) => {
    return {
      product_type: data.product_type,
      serial_or_project_id: data.serial_or_project_id,
      installation_date: data.installation_date,
      customer_name: data.customer_name,
      phone: data.phone,
      email: data.email,
      installer_name: data.installer_name
    };
  });

  // Bind Complaint form (Multipart form-data)
  setupMultipartFormSubmit("complaint-form", "/complaints");

  // Bind Job Application forms (Multipart form-data)
  setupMultipartFormSubmit("job-apply-form", null); // endpoint is set dynamically by action
  setupMultipartFormSubmit("general-apply-form", "/careers/apply-general", (formData) => {
    // Backend has no dedicated "role" field, so fold the selected role into the cover letter
    const role = formData.get("role");
    formData.delete("role");
    if (role && role !== "Select a position...") {
      const existing = formData.get("cover_letter") || "";
      formData.set("cover_letter", `Applied for: ${role}\n\n${existing}`);
    }
  });
});

/**
 * Standard JSON Form Submission Handler helper
 * @param {string} formId - HTML element id
 * @param {string} endpoint - API endpoint
 * @param {function} transformFn - Converts inputs to request payload
 */
function setupFormSubmit(formId, endpoint, transformFn) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Check form validations
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    // Set loading state
    setButtonLoading(submitBtn, true);

    const formData = new FormData(form);
    const formProps = Object.fromEntries(formData);
    const payload = transformFn(formProps);

    try {
      const result = await api.post(endpoint, payload);
      
      // Clear forms on success
      form.reset();
      
      // Show success notification with honest demo mode information
      const msg = result.demoMode
        ? "Demo Mode: Submission processed and stored locally for testing."
        : "Your submission was sent successfully. We'll be in touch!";
      window.showToast(msg, "success", `${formId}-feedback`);
    } catch (err) {
      window.showToast(err.message || "An error occurred. Please try again.", "error", `${formId}-feedback`);
    } finally {
      setButtonLoading(submitBtn, false, originalBtnText);
    }
  });
}

/**
 * Multipart/Form-data Submission Handler helper for file uploads (Complaints and Careers)
 * @param {string} formId - HTML Form element id
 * @param {string} defaultEndpoint - Fallback endpoint URL
 * @param {function} [transformFn] - Optional hook to mutate the FormData before sending
 */
function setupMultipartFormSubmit(formId, defaultEndpoint, transformFn) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    setButtonLoading(submitBtn, true);

    const endpoint = defaultEndpoint || form.getAttribute("action");
    const formData = new FormData(form);
    if (transformFn) transformFn(formData);

    try {
      const result = await api.post(endpoint, formData, true);
      form.reset();
      
      const msg = result.demoMode
        ? "Demo Mode: Application and files processed and stored locally."
        : "Your file and details have been uploaded successfully!";
      window.showToast(msg, "success", `${formId}-feedback`);
    } catch (err) {
      window.showToast(err.message || "Upload failed. Please check file format and sizes.", "error", `${formId}-feedback`);
    } finally {
      setButtonLoading(submitBtn, false, originalBtnText);
    }
  });
}

/**
 * Utility function to toggle loading spinners on submit buttons
 */
function setButtonLoading(button, isLoading, originalText = "") {
  if (!button) return;
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = originalText || button.innerHTML;
    button.innerHTML = `<span class="spinner"></span> Submitting...`;
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || originalText;
  }
}
