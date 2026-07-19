import os
import re

def get_navbar(target_file):
    # Determine which link is active
    home_class = "text-secondary-container nav-active pb-1 relative" if target_file == "index.html" else "text-on-surface hover:text-secondary-container transition-colors"
    company_class = "text-secondary-container nav-active pb-1 relative" if target_file == "about.html" else "text-on-surface hover:text-secondary-container transition-colors"
    services_class = "text-secondary-container nav-active pb-1 relative" if target_file == "services.html" else "text-on-surface hover:text-secondary-container transition-colors"
    projects_class = "text-secondary-container nav-active pb-1 relative" if target_file == "projects.html" else "text-on-surface hover:text-secondary-container transition-colors"
    products_class = "text-secondary-container nav-active pb-1 relative" if target_file == "products.html" else "text-on-surface hover:text-secondary-container transition-colors"
    media_class = "text-secondary-container nav-active pb-1 relative" if target_file == "media.html" else "text-on-surface hover:text-secondary-container transition-colors"
    careers_class = "text-secondary-container nav-active pb-1 relative" if target_file == "careers.html" else "text-on-surface hover:text-secondary-container transition-colors"
    connect_class = "text-secondary-container nav-active pb-1 relative" if target_file == "connect.html" else "text-on-surface hover:text-secondary-container transition-colors"
    
    return f"""<!-- TopNavBar -->
<nav class="fixed top-0 w-full z-50 bg-white border-b border-outline-technical transition-all duration-300 ease-in-out">
<div class="flex justify-between items-center px-margin-desktop py-3 w-full max-w-full">
<a href="index.html" class="flex items-center shrink-0">
                <img src="assets/images/logo.svg" alt="SunPlus Power" class="h-10 w-auto object-contain" style="max-width:200px;"/>
            </a>
<div class="hidden lg:flex items-center space-x-8">
<a class="font-label-technical text-label-technical uppercase tracking-widest {home_class}" href="index.html">Home</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {company_class}" href="about.html">Company</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {services_class}" href="services.html">Services</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {projects_class}" href="projects.html">Projects</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {products_class}" href="products.html">Products</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {media_class}" href="media.html">Solar Intelligence</a>
<a class="font-label-technical text-label-technical uppercase tracking-widest {careers_class}" href="careers.html">Careers</a>
<div class="relative group">
<a class="font-label-technical text-label-technical uppercase tracking-widest {connect_class} inline-flex items-center gap-1 cursor-pointer" href="connect.html">
Connect
<span class="material-symbols-outlined text-[16px] transition-transform group-hover:rotate-180">expand_more</span>
</a>
<div class="absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
<div class="py-1" role="menu">
<a href="connect.html?tab=distributor" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-primary transition-colors" role="menuitem">Apply for Distributor</a>
<a href="connect.html?tab=warranty" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-primary transition-colors" role="menuitem">Warranty Registration</a>
<a href="connect.html?tab=complaint" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-primary transition-colors" role="menuitem">Complaint / Support</a>
</div>
</div>
</div>
</div>
</div>
</div>
</nav>"""



def get_footer():
    return """<!-- Footer -->
<footer class="bg-surface-dim text-white border-t border-white/10 w-full mt-24">
<div class="grid grid-cols-1 md:grid-cols-5 gap-gutter px-margin-desktop py-20 w-full max-w-container-max mx-auto">
<div class="md:col-span-2 space-y-6">
<a href="index.html" class="flex items-center">
  <img src="assets/images/logo.svg" alt="SunPlus Power" class="h-12 w-auto brightness-0 invert" style="max-width:220px;"/>
</a>
<p class="text-white/60 max-w-sm font-body-md leading-relaxed">Engineering the global energy transition through rigorous technical modeling and industrial-scale solar deployment.</p>
</div>
<div>
<h4 class="font-label-technical text-label-technical uppercase text-white mb-8 tracking-widest">Quick Links</h4>
<ul class="space-y-4 font-body-md">
<li><a class="text-white/60 hover:text-primary transition-colors" href="about.html">Company</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="services.html">Services</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="projects.html">Projects</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="products.html">Products</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="media.html">Solar Intelligence</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="careers.html">Careers</a></li>
</ul>
</div>
<div>
<h4 class="font-label-technical text-label-technical uppercase text-white mb-8 tracking-widest">Connect</h4>
<ul class="space-y-4 font-body-md">
<li><a class="text-white/60 hover:text-primary transition-colors" href="connect.html?tab=distributor">Apply for Distributor</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="connect.html?tab=warranty">Warranty Registration</a></li>
<li><a class="text-white/60 hover:text-primary transition-colors" href="connect.html?tab=complaint">Complaint / Support</a></li>
</ul>
</div>
<div>
<h4 class="font-label-technical text-label-technical uppercase text-white mb-8 tracking-widest">Contact</h4>
<p class="text-white/60 font-body-md mb-4 leading-relaxed">
    <b>Corporate Address:</b><br/>
    1st Floor, D134, Vibhuti Khand<br/>
    Gomti Nagar, Lucknow<br/>
    Uttar Pradesh, India - 226010
</p>
<p class="text-white/60 font-body-md leading-relaxed">
    <b>Sales Help:</b> <a class="hover:text-primary" href="mailto:sales@sunpluspower.in">sales@sunpluspower.in</a><br/>
    <b>Technical Support:</b> <a class="hover:text-primary" href="mailto:info@sunpluspower.in">info@sunpluspower.in</a><br/>
    <b>Official Phone:</b> +91-9648045063
</p>
</div>
</div>
<div class="px-margin-desktop py-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 max-w-container-max mx-auto">
<div class="font-body-md text-body-md text-white/40">© 2026 SUNPLUS POWER. ALL RIGHTS RESERVED.</div>
<div class="flex gap-8">
<a class="text-white/40 hover:text-white text-label-technical uppercase font-label-technical tracking-widest" href="connect.html">Privacy Policy</a>
<a class="text-white/40 hover:text-white text-label-technical uppercase font-label-technical tracking-widest" href="connect.html">Terms of Use</a>
</div>
</div>
</footer>"""


# List of source folders and target HTML files
pages_map = {
    "homepage_decent_theme": "index.html",
    "about_us_decent_theme": "about.html",
    "services_decent_theme": "services.html",
    "projects_portfolio_decent_theme": "projects.html",
    "solar_calculator_decent_theme": "calculator.html",
    "products_decent_theme": "products.html",
    "group_business_decent_theme": "group-business.html",
    "media_hub_decent_theme": "media.html",
    "faq_decent_theme": "faq.html",
    "careers_decent_theme": "careers.html",
    "let_s_connect_decent_theme": "connect.html"
}

source_dir = "stitch_sunplus_power_solar_website"
target_dir = "frontend"

os.makedirs(target_dir, exist_ok=True)

for src_folder, target_file in pages_map.items():
    src_path = os.path.join(source_dir, src_folder, "code.html")
    dest_path = os.path.join(target_dir, target_file)
    
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}")
        continue
        
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Remove Tailwind CDN script tag and inline config block
    content = re.sub(
        r'<script[^>]*tailwindcss\.com[^>]*></script>',
        '',
        content
    )
    content = re.sub(
        r'<script id="tailwind-config">.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 2. Inject CSS variables, base, components, and compiled tailwind styles
    css_links = """
    <link rel="stylesheet" href="assets/css/variables.css?v=5"/>
    <link rel="stylesheet" href="assets/css/base.css?v=5"/>
    <link rel="stylesheet" href="assets/css/components.css?v=5"/>
    <link rel="stylesheet" href="assets/css/tailwind-compiled.css?v=5"/>
    """
    content = content.replace("</head>", f"{css_links}\n</head>")
    
    # 3. Inject JS API client and main helpers
    js_scripts = """
    <script src="assets/js/api.js?v=5" defer></script>
    <script src="assets/js/main.js?v=5" defer></script>
    """
    
    # Inject page-specific scripts as well
    if target_file == "calculator.html":
        js_scripts += '<script src="assets/js/calculator.js?v=5" defer></script>\n'
    elif target_file in ["connect.html", "careers.html"]:
        js_scripts += '<script src="assets/js/forms.js?v=5" defer></script>\n'
        
    content = content.replace("</head>", f"{js_scripts}\n</head>")
    
    # 3.5. Inject dynamic global navbar
    if "<!-- TopNavBar -->" in content:
        # Determine the closing tag: header or nav
        navbar_part = content.split("<!-- TopNavBar -->", 1)[1].strip()
        if navbar_part.startswith("<header"):
            end_tag = "</header>"
        else:
            end_tag = "</nav>"
        
        # Replace the entire block from <!-- TopNavBar --> to the end_tag
        before_nav, after_nav = content.split("<!-- TopNavBar -->", 1)
        after_nav_cleaned = after_nav.split(end_tag, 1)[1]
        
        # Build dynamic navbar
        navbar_html = get_navbar(target_file)
        content = before_nav + navbar_html + after_nav_cleaned
    
    # 3.6. Inject dynamic global footer
    if "<!-- Footer -->" in content:
        before_footer, after_footer = content.split("<!-- Footer -->", 1)
        after_footer_cleaned = after_footer.split("</footer>", 1)[1]
        
        # Build dynamic footer
        footer_html = get_footer()
        content = before_footer + footer_html + after_footer_cleaned

    # 4. Replace external logo URLs with local SVG logo
    # In navbar (normally has brightness-0 invert)
    # Match any src inside img having alt="SunPlus Power Logo" or similar
    content = re.sub(
        r'src="https://lh3\.googleusercontent\.com/aida-public/[^"]+"([^>]*alt="SunPlus Power Logo")',
        'src="assets/images/logo.svg"\\1',
        content
    )
    # Handle matches with alt before src
    content = re.sub(
        r'(alt="SunPlus Power Logo"[^>]*src=")https://lh3\.googleusercontent\.com/aida-public/[^"]+"',
        '\\1assets/images/logo.svg"',
        content
    )
    # General clean replacement for any sunplus logo image tags (fallback if above didn't catch it)
    content = re.sub(
        r'<img([^>]*alt="[^"]*Logo[^"]*"[^>]*src=")[^"]+"',
        '<img\\1assets/images/logo.svg"',
        content
    )
    
    # Wrap the navbar logo image in an anchor leading to index.html
    # We find '<div class="flex items-center gap-3">\s*<img[^>]+logo\.svg[^>]+>'
    content = re.sub(
        r'(<div class="flex items-center gap-[^"]*">\s*)(<img[^>]+logo\.svg[^>]+>)',
        '\\1<a href="index.html" class="flex items-center gap-3">\\2</a>',
        content
    )
    
    # 3.7. Fix hero section image cut-off on smaller screens
    # Replace min-h-[90vh] with min-h-[500px] md:min-h-[90vh] for responsiveness
    content = content.replace(
        'class="relative min-h-[90vh] flex items-center overflow-hidden',
        'class="relative min-h-[520px] md:min-h-[90vh] flex items-center overflow-hidden'
    )
    content = content.replace(
        'class="relative min-h-[80vh] flex items-center overflow-hidden',
        'class="relative min-h-[480px] md:min-h-[80vh] flex items-center overflow-hidden'
    )
    # Ensure hero background images use bg-cover and bg-center correctly
    content = re.sub(
        r'(class="[^"]*w-full h-full)(")(\s*style="background-image)',
        r'\1 bg-cover bg-center object-cover\2\3',
        content
    )
    
    # 5. Fix navigation hyperlinks
    # Replace navigation text anchors to their matching pages
    content = re.sub(r'href="[^"]+">Home</a>', 'href="index.html">Home</a>', content)
    content = re.sub(r'href="[^"]+">Company</a>', 'href="about.html">Company</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Company</a>', 'href="about.html" class="font-bold">Company</a>', content)
    content = re.sub(r'href="[^"]+">About</a>', 'href="about.html">About Us</a>', content)
    content = re.sub(r'href="[^"]+">Services</a>', 'href="services.html">Services</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Services</a>', 'href="services.html" class="font-bold">Services</a>', content)
    content = re.sub(r'href="[^"]+">Projects</a>', 'href="projects.html">Projects</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Projects</a>', 'href="projects.html" class="font-bold">Projects</a>', content)
    content = re.sub(r'href="[^"]+">Products</a>', 'href="products.html">Products</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Products</a>', 'href="products.html" class="font-bold">Products</a>', content)
    content = re.sub(r'href="[^"]+">Solar Intelligence</a>', 'href="media.html">Solar Intelligence</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Solar Intelligence</a>', 'href="media.html" class="font-bold">Solar Intelligence</a>', content)
    content = re.sub(r'href="[^"]+">Careers</a>', 'href="careers.html">Careers</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Careers</a>', 'href="careers.html" class="font-bold">Careers</a>', content)
    content = re.sub(r'href="[^"]+">Connect</a>', 'href="connect.html">Connect</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Connect</a>', 'href="connect.html" class="font-bold">Connect</a>', content)
    
    # Replace remaining generic href="#" for navigation links
    content = content.replace('href="#"', 'href="index.html"')
    
    # Ensure Careers link is in the navbar list if not already present
    if 'href="careers.html"' not in content:
        content = content.replace(
            'href="products.html">Products</a>',
            'href="products.html">Products</a>\n<a class="text-on-surface font-label-md hover:text-primary transition-colors" href="careers.html">Careers</a>'
        )
    
    # Replace solar calculator buttons to calculator.html
    # Look for button text "Solar Calculator" or similar
    content = re.sub(
        r'<button([^>]*onclick="[^"]*")>Solar Calculator</button>',
        r'<a href="calculator.html" class="btn-primary text-sm font-bold">Solar Calculator</a>',
        content
    )
    content = re.sub(
        r'<button([^>]*)>(\s*Solar Calculator\s*)</button>',
        r'<a href="calculator.html" class="btn-primary text-sm font-bold">\2</a>',
        content
    )
    
    # In footer links
    content = re.sub(r'href="[^"]+">Sitemap</a>', 'href="index.html">Sitemap</a>', content)
    content = re.sub(r'href="[^"]+ font-bold">Contact</a>', 'href="connect.html" class="text-white font-bold">Contact</a>', content)
    content = re.sub(r'href="[^"]+">Contact</a>', 'href="connect.html">Contact</a>', content)
    content = re.sub(r'href="[^"]+">Media</a>', 'href="media.html">Media Hub</a>', content)
    content = re.sub(r'href="[^"]+">Privacy Policy</a>', 'href="connect.html">Privacy Policy</a>', content)
    content = re.sub(r'href="[^"]+">Terms of Service</a>', 'href="connect.html">Terms of Service</a>', content)
    
    # 6. Form binding updates
    # Contact Form ID on connect.html
    if target_file == "connect.html":
        # Form contact
        content = content.replace('<form class="space-y-6">', '<form id="contact-form" class="space-y-6">', 1)
        # Form distributor
        content = content.replace('<form class="space-y-6">', '<form id="distributor-form" class="space-y-6">', 1)
        # Form warranty
        content = content.replace('<form class="space-y-6">', '<form id="warranty-form" class="space-y-6">', 1)
        # Form complaint
        content = content.replace('<form class="space-y-6">', '<form id="complaint-form" action="/api/complaints" method="POST" enctype="multipart/form-data" class="space-y-6">', 1)
        
        # Inject target feedback divs above the forms or buttons
        content = re.sub(
            r'(<form id="contact-form"[^>]*>)',
            '\\1<div id="contact-form-feedback"></div>',
            content
        )
        content = re.sub(
            r'(<form id="distributor-form"[^>]*>)',
            '\\1<div id="distributor-form-feedback"></div>',
            content
        )
        content = re.sub(
            r'(<form id="warranty-form"[^>]*>)',
            '\\1<div id="warranty-form-feedback"></div>',
            content
        )
        content = re.sub(
            r'(<form id="complaint-form"[^>]*>)',
            '\\1<div id="complaint-form-feedback"></div>',
            content
        )
        
        # Map fields in forms to submit correctly
        # Contact form fields
        content = re.sub(r'(<input [^>]*placeholder="John Doe"[^>]*)>', '\\1 name="name" required>', content)
        content = re.sub(r'(<input [^>]*placeholder="john@company.com"[^>]*)>', '\\1 name="email" required>', content)
        # Add a phone field to Contact Form in HTML if missing
        content = content.replace(
            '<div class="flex flex-col">\n<label class="text-label-md text-on-surface mb-2">Subject</label>',
            '<div class="flex flex-col">\n<label class="text-label-md text-on-surface mb-2">Phone Number</label>\n<input name="phone" type="text" class="border border-outline rounded p-3 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all" placeholder="+91 9876543210" required />\n</div>\n<div class="flex flex-col">\n<label class="text-label-md text-on-surface mb-2">Subject</label>'
        )
        content = re.sub(r'(<select [^>]*)>', '\\1 name="subject">', content)
        content = re.sub(r'(<textarea [^>]*placeholder="Describe your project[^>]*)>', '\\1 name="message" required>', content)
        
        # Distributor form fields
        content = re.sub(r'(<input class="border border-outline rounded p-3[^>]*>)\s*(</div>\s*<div class="flex flex-col">\s*<label class="text-label-md text-on-surface mb-2">Annual Revenue)', '<input name="company_name" required class="border border-outline rounded p-3 outline-none" type="text">\\2', content)
        # Replace remaining distributor inputs to support contact_person, region, business_type, years_in_business, phone, email, message
        # Let's adjust inputs in distributor applications
        content = content.replace(
            '<form id="distributor-form" class="space-y-6">',
            """<form id="distributor-form" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Company Name</label>
                        <input name="company_name" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Contact Person Name</label>
                        <input name="contact_person" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Region / Territory of Interest</label>
                        <input name="region" class="border border-outline rounded p-3 outline-none focus:border-primary" placeholder="State/Country" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Business Type</label>
                        <input name="business_type" class="border border-outline rounded p-3 outline-none focus:border-primary" placeholder="EPC/Retail/Distributor" type="text" required />
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Years in Business</label>
                        <input name="years_in_business" class="border border-outline rounded p-3 outline-none focus:border-primary" type="number" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Corporate Email</label>
                        <input name="email" class="border border-outline rounded p-3 outline-none focus:border-primary" type="email" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Phone Number</label>
                        <input name="phone" class="border border-outline rounded p-3 outline-none focus:border-primary" placeholder="+91 98765 43210" type="text" required />
                    </div>
                </div>
                <div class="flex flex-col">
                    <label class="text-label-md text-on-surface mb-2">Partnership Proposal / Message</label>
                    <textarea name="message" class="border border-outline rounded p-3 outline-none focus:border-primary" rows="4" required></textarea>
                </div>
                <button class="w-full bg-primary text-white font-label-md py-4 rounded hover:bg-primary-dark transition-all" type="submit">Submit Application</button>
            </form>
            <!-- REMOVED ORIGINAL DISTRIBUTOR FORM"""
        )
        # Close comment for removed distributor form
        content = content.replace('</form>\n</div>\n<!-- Warranty Form', '-->\n</div>\n<!-- Warranty Form')

        # Warranty registration form mapping
        content = content.replace(
            '<form id="warranty-form" class="space-y-6">',
            """<form id="warranty-form" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Product Category</label>
                        <select name="product_type" class="border border-outline rounded p-3 outline-none focus:border-primary bg-white">
                            <option>Solar Inverter</option>
                            <option>PV Modules</option>
                            <option>Battery Storage</option>
                            <option>BOS / Cables</option>
                        </select>
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Serial Number / Project ID</label>
                        <input name="serial_or_project_id" class="border border-outline rounded p-3 outline-none focus:border-primary" placeholder="SPP-XXXX-XXXX" type="text" required />
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Installation Date</label>
                        <input name="installation_date" class="border border-outline rounded p-3 outline-none focus:border-primary" type="date" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Customer Full Name</label>
                        <input name="customer_name" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Authorized Installer Name</label>
                        <input name="installer_name" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Contact Email</label>
                        <input name="email" class="border border-outline rounded p-3 outline-none focus:border-primary" type="email" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Phone Number</label>
                        <input name="phone" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                </div>
                <button class="w-full bg-primary text-white font-label-md py-4 rounded hover:bg-primary-dark transition-all" type="submit">Register Warranty</button>
            </form>
            <!-- REMOVED ORIGINAL WARRANTY FORM"""
        )
        content = content.replace('</form>\n</div>\n<!-- Complaint Form', '-->\n</div>\n<!-- Complaint Form')

        # Complaint form mapping
        content = content.replace(
            '<form id="complaint-form" action="/api/complaints" method="POST" enctype="multipart/form-data" class="space-y-6">',
            """<form id="complaint-form" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Full Name</label>
                        <input name="name" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Phone Number</label>
                        <input name="phone" class="border border-outline rounded p-3 outline-none focus:border-primary" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Contact Email</label>
                        <input name="email" class="border border-outline rounded p-3 outline-none focus:border-primary" type="email" required />
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Associated Reference / Project ID</label>
                        <input name="project_or_product_id" class="border border-outline rounded p-3 outline-none focus:border-primary" placeholder="SPP-XXXX" type="text" required />
                    </div>
                    <div class="flex flex-col">
                        <label class="text-label-md text-on-surface mb-2">Nature of Issue</label>
                        <select name="category" class="border border-outline rounded p-3 outline-none focus:border-primary bg-white">
                            <option value="installation">Installation</option>
                            <option value="om">O&M / Maintenance</option>
                            <option value="product">Product Malfunction</option>
                            <option value="billing">Billing Dispute</option>
                            <option value="other">Other Support</option>
                        </select>
                    </div>
                </div>
                <div class="flex flex-col">
                    <label class="text-label-md text-on-surface mb-2">Incident Description</label>
                    <textarea name="description" class="border border-outline rounded p-3 outline-none focus:border-primary" rows="4" required></textarea>
                </div>
                <div class="p-4 bg-surface-container rounded border-l-4 border-primary">
                    <p class="text-label-sm text-on-surface uppercase tracking-wider mb-1">Attachment Required (Optional)</p>
                    <p class="text-body-md mb-4">Please upload a photo of the issue (JPG/PNG under 5MB).</p>
                    <input name="photo" type="file" accept="image/*" class="text-body-md text-secondary" />
                </div>
                <button class="w-full bg-primary text-white font-label-md py-4 rounded hover:bg-primary-dark transition-all" type="submit">Submit Urgent Ticket</button>
            </form>
            <!-- REMOVED ORIGINAL COMPLAINTS FORM"""
        )
        content = content.replace('</form>\n</div>\n</div>\n<!-- Sidebar', '-->\n</div>\n</div>\n<!-- Sidebar')

    # Solar Calculator Binding on calculator.html
    if target_file == "calculator.html":
        # Form values mapping
        content = content.replace(
            '<section class="p-8" id="form-step-1">',
            '<section class="p-8" id="form-step-1"><form id="solar-calculator-form">',
            1
        )
        content = content.replace(
            '</section>\n<!-- Step 3 -->',
            '</form></section>\n<!-- Step 3 -->',
            1
        )
        
        # Modify stepper inputs to match names
        content = re.sub(r'type="number"\s*/?>', 'id="calc-bill" name="monthly_bill" type="number" required>', content)
        content = re.sub(
            r'<select([^>]*)>\s*<option>Select utility company</option>[^<]*<option>[^<]*</option>[^<]*<option>[^<]*</option>[^<]*<option>[^<]*</option>\s*</select>',
            r'<select id="calc-state" name="location" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all">\n<option value="">Select State</option>\n<option value="uttar pradesh">Uttar Pradesh (Lucknow HQ)</option>\n<option value="madhya pradesh">Madhya Pradesh</option>\n<option value="punjab">Punjab</option>\n<option value="maharashtra">Maharashtra</option>\n<option value="gujarat">Gujarat</option>\n<option value="rajasthan">Rajasthan</option>\n<option value="karnataka">Karnataka</option>\n<option value="tamil nadu">Tamil Nadu</option>\n<option value="telangana">Telangana</option>\n<option value="delhi">Delhi</option>\n</select>',
            content
        )
        
        # Replace step 2 fields: Zip Code, Name, Email, Phone, Roof Area
        content = re.sub(
            r'<div>\s*<label class="block text-label-md font-bold text-on-surface mb-2">Zip Code</label>\s*<input class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="90210" type="text"/>\s*</div>',
            r'<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Zip Code</label>\n<input id="calc-zip" name="zipcode" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="226001" type="text"/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Full Name</label>\n<input id="calc-name" name="name" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="John Doe" type="text" required/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Email Address</label>\n<input id="calc-email" name="email" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="john@company.com" type="email" required/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Phone Number</label>\n<input id="calc-phone" name="phone" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="+91 98765 43210" type="text"/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Available Roof Area (sq. ft.)</label>\n<input id="calc-roof-area" name="roof_area" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="1000" type="number" required/>\n</div>',
            content
        )
        
        # Add id to Property Type select in step 2
        content = content.replace(
            '<label class="block text-label-md font-bold text-on-surface mb-2">Property Type</label>\n<select class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all">',
            '<label class="block text-label-md font-bold text-on-surface mb-2">Property Type</label>\n<select id="calc-property-type" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all">'
        )
        
        # Replace step 3 type buttons with click actions
        content = content.replace(
            '<button class="p-6 border-2 border-primary bg-surface-container-lowest rounded text-left transition-all ring-1 ring-primary/10">',
            '<button id="calc-type-rooftop" type="button" class="p-6 border-2 border-primary bg-surface-container-lowest rounded text-left transition-all ring-1 ring-primary/10">'
        )
        content = content.replace(
            '<button class="p-6 border border-surface-container-highest hover:border-on-surface bg-white rounded text-left transition-all">',
            '<button id="calc-type-ground" type="button" class="p-6 border border-surface-container-highest hover:border-on-surface bg-white rounded text-left transition-all">'
        )
        
        # Replace calculate ROI button trigger
        content = re.sub(
            r'<button class="bg-primary text-white[^>]+onclick="showResults\(\)"[^>]*>(\s*Calculate ROI\s*[^<]*)</button>',
            r'<button id="calculate-roi-btn" type="button" onclick="calculateROI()" class="bg-primary text-white px-10 py-4 rounded font-label-md flex items-center gap-2 shadow-lg shadow-primary/20 hover:scale-[1.02] transition-all">\1</button>',
            content
        )
        
        # Map dynamic results IDs
        # System size kW
        content = re.sub(r'<span class="text-headline-lg font-bold text-on-surface">8\.4</span>', '<span id="res-system-size" class="text-headline-lg font-bold text-on-surface">-</span>', content)
        # Payback
        content = re.sub(r'<span class="text-headline-lg font-bold text-on-surface">6\.2</span>', '<span id="res-payback" class="text-headline-lg font-bold text-on-surface">-</span>', content)
        # Projected savings
        content = re.sub(r'<span class="text-headline-lg font-bold text-white">₹2,50,000</span>', '<span id="res-savings-lifetime" class="text-headline-lg font-bold text-white">-</span>', content)
        
        # Map ROI sidebar specs
        content = content.replace(
            '<div class="mt-12 p-4 bg-surface-container-low rounded border border-surface-container-highest">',
            """<div class="mt-8 space-y-4 border-t border-surface-container pt-4 text-sm text-secondary">
                <div class="flex justify-between"><span>Gross Project Cost:</span><span id="res-gross-cost" class="font-bold text-on-surface">-</span></div>
                <div class="flex justify-between"><span>Subsidy Benefit:</span><span id="res-subsidy" class="font-bold text-primary">-</span></div>
                <div class="flex justify-between border-t border-surface-container pt-2"><span><b>Net Out-of-pocket:</b></span><span id="res-net-cost" class="font-bold text-on-surface text-base">-</span></div>
                <div class="flex justify-between pt-2"><span>Annual Savings:</span><span id="res-annual-savings" class="font-bold text-on-surface">-</span></div>
                <div class="flex justify-between"><span>Annual Carbon Offset:</span><span id="res-co2-offset" class="font-bold text-green-600">-</span> kg CO2</div>
            </div>
            <div class="mt-12 p-4 bg-surface-container-low rounded border border-surface-container-highest">"""
        )
        # Fix the Calculate ROI button (showResults → calculateROI)
        content = content.replace(
            'onclick="showResults()"',
            'onclick="calculateROI()"'
        )
        # Add the id attribute to the ROI button if missing
        content = content.replace(
            '<button class="bg-primary text-white px-10 py-4 rounded font-label-md flex items-center gap-2 shadow-lg shadow-primary/20 hover:scale-[1.02] transition-all" onclick="calculateROI()">',
            '<button id="calculate-roi-btn" class="bg-primary text-white px-10 py-4 rounded font-label-md flex items-center gap-2 shadow-lg shadow-primary/20 hover:scale-[1.02] transition-all" onclick="calculateROI()">'
        )
        # Fix download button
        content = re.sub(
            r'<button class="w-full mt-8 bg-on-surface text-white[^>]*>(\s*Download Full Report\s*[^<]*)</button>',
            r'<button onclick="mockDownloadReport()" class="w-full mt-8 bg-on-surface text-white py-3 rounded font-label-md hover:bg-tertiary transition-all flex items-center justify-center gap-2">\1</button>',
            content
        )
        
        # Replace fake map image with real OpenStreetMap iframe
        content = re.sub(
            r'<div class="w-full h-48 rounded bg-surface-container relative overflow-hidden border border-surface-container-highest">.*?</div>\s*</div>',
            '''<div class="w-full rounded overflow-hidden border border-surface-container-highest" style="height:192px;">
  <iframe
    title="SunPlus Power HQ — Lucknow"
    src="https://www.openstreetmap.org/export/embed.html?bbox=80.9783%2C26.8527%2C80.9983%2C26.8727&layer=mapnik&marker=26.8627%2C80.9883"
    style="width:100%;height:100%;border:0;"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>
<p class="text-[10px] text-tertiary mt-1">&#128205; Lucknow, UP — SunPlus Power HQ</p>
</div>''',
            content,
            count=1,
            flags=re.DOTALL
        )
        
        # Replace old broken bar chart with dynamic SVG line chart
        old_chart_pattern = r'<div class="relative h-64 w-full flex items-end justify-between gap-2 border-b border-l border-surface-container-highest p-4 bg-surface-container-lowest">.*?</div>\s*</div>'
        new_chart_svg = '''<div class="relative w-full" style="height:260px;">
  <svg id="projection-chart" width="100%" height="100%" viewBox="0 0 800 240" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <line x1="60" y1="10" x2="60" y2="210" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="60" y1="210" x2="790" y2="210" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="60" y1="10" x2="790" y2="10" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4 4"/>
    <line x1="60" y1="60" x2="790" y2="60" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4 4"/>
    <line x1="60" y1="110" x2="790" y2="110" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4 4"/>
    <line x1="60" y1="160" x2="790" y2="160" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4 4"/>
    <text id="chart-y4" x="55" y="14" text-anchor="end" font-size="10" fill="#94a3b8"></text>
    <text id="chart-y3" x="55" y="64" text-anchor="end" font-size="10" fill="#94a3b8"></text>
    <text id="chart-y2" x="55" y="114" text-anchor="end" font-size="10" fill="#94a3b8"></text>
    <text id="chart-y1" x="55" y="164" text-anchor="end" font-size="10" fill="#94a3b8"></text>
    <text x="55" y="214" text-anchor="end" font-size="10" fill="#94a3b8">0</text>
    <text x="60" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y1</text>
    <text x="208" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y5</text>
    <text x="356" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y10</text>
    <text x="504" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y15</text>
    <text x="652" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y20</text>
    <text x="790" y="226" text-anchor="middle" font-size="10" fill="#94a3b8">Y25</text>
    <polyline id="chart-utility-line" points="" fill="none" stroke="#cbd5e1" stroke-width="2.5" stroke-linejoin="round"/>
    <polyline id="chart-solar-line" points="" fill="none" stroke="#b5111a" stroke-width="2.5" stroke-linejoin="round"/>
    <line id="chart-crossover-line" x1="0" y1="0" x2="0" y2="0" stroke="#b5111a" stroke-width="1" stroke-dasharray="4 3" opacity="0"/>
    <text id="chart-crossover-label" x="0" y="0" font-size="10" fill="#b5111a" font-weight="bold" opacity="0"></text>
    <text id="chart-placeholder" x="400" y="115" text-anchor="middle" font-size="13" fill="#94a3b8">Run the calculator to see your financial projection</text>
  </svg>
</div>'''
        content = re.sub(old_chart_pattern, new_chart_svg, content, count=1, flags=re.DOTALL)
        
        # Remove embedded script at footer since we are linking calculator.js
        content = re.sub(
            r'<script>\s*function nextStep\(step\).*?<\/script>',
            '',
            content,
            flags=re.DOTALL
        )


    # Careers page updates
    if target_file == "careers.html":
        # Wire up dynamic navigation details
        # Let's adjust openings rendering so it triggers dynamic listings
        # In careers.html we will add a container div and dynamic scripts
        pass
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Generated page: {dest_path}")

print("Basic HTML conversion complete.")
