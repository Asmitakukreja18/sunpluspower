/**
 * SunPlus Power Shared Frontend Interactions
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Highlight Active Nav Item
  highlightActiveNav();

  // 2. Setup Mobile Navbar Toggles
  setupMobileNav();

  // 3. Scroll effects on Header
  setupHeaderScroll();
});

/**
 * Automatically detects the current page path and applies active class highlighting
 */
function highlightActiveNav() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll("header nav a, .mobile-nav-link");
  
  navLinks.forEach(link => {
    const href = link.getAttribute("href");
    if (!href) return;
    
    // Check if the current page matches the link destination
    const linkPath = href.split("/").pop();
    const activePath = currentPath.split("/").pop();
    
    if (linkPath === activePath || (activePath === "" && linkPath === "index.html")) {
      // Apply primary highlight classes
      link.classList.remove("text-white/70", "text-secondary");
      link.classList.add("text-primary", "font-bold");
      
      // If it's a desktop link, add bottom border style
      if (link.tagName === "A" && !link.classList.contains("mobile-nav-link")) {
        link.classList.add("border-b-2", "border-primary", "pb-1");
      }
    }
  });
}

/**
 * Initialises mobile dropdown toggle triggers
 */
function setupMobileNav() {
  const toggleBtn = document.getElementById("mobile-menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  
  if (toggleBtn && mobileMenu) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = !mobileMenu.classList.contains("hidden");
      if (isOpen) {
        mobileMenu.classList.add("hidden");
        toggleBtn.innerHTML = `<span class="material-symbols-outlined text-white">menu</span>`;
      } else {
        mobileMenu.classList.remove("hidden");
        toggleBtn.innerHTML = `<span class="material-symbols-outlined text-white">close</span>`;
      }
    });
  }
}

/**
 * Changes header overlay class on scroll to maintain contrast
 */
function setupHeaderScroll() {
  const header = document.querySelector("header");
  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        header.classList.add("bg-charcoal/95", "backdrop-blur-md", "shadow-md");
      } else {
        header.classList.remove("bg-charcoal/95", "backdrop-blur-md", "shadow-md");
      }
    });
  }
}

/**
 * Universal Toast Notification Banner Builder
 * @param {string} message - Message text
 * @param {string} type - 'success' or 'error'
 * @param {string} containerId - Target element ID to prepend/render inside
 */
function showToast(message, type = "success", containerId = null) {
  const banner = document.createElement("div");
  banner.className = `alert-banner ${type} animate-in fade-in duration-300`;
  
  const icon = type === "success" ? "check_circle" : "error";
  banner.innerHTML = `
    <span class="material-symbols-outlined">${icon}</span>
    <span>${message}</span>
  `;
  
  let target;
  if (containerId) {
    target = document.getElementById(containerId);
  }
  
  if (!target) {
    // If no container, show it at the top of the body
    banner.style.position = "fixed";
    banner.style.top = "90px";
    banner.style.right = "24px";
    banner.style.zIndex = "1000";
    banner.style.boxShadow = "0px 10px 25px rgba(0,0,0,0.1)";
    document.body.appendChild(banner);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      banner.remove();
    }, 5000);
  } else {
    // Empty target container and append
    target.innerHTML = "";
    target.appendChild(banner);
    target.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}
window.showToast = showToast;
