import os
import re

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
        
    # 1. Remove Tailwind CDN script tag
    content = re.sub(
        r'<script[^>]*tailwindcss\.com[^>]*></script>',
        '',
        content
    )
    
    # 2. Inject CSS variables, base, components, and compiled tailwind styles
    css_links = """
    <link rel="stylesheet" href="assets/css/variables.css"/>
    <link rel="stylesheet" href="assets/css/base.css"/>
    <link rel="stylesheet" href="assets/css/components.css"/>
    <link rel="stylesheet" href="assets/css/tailwind-compiled.css"/>
    """
    content = content.replace("</head>", f"{css_links}\n</head>")
    
    # 3. Inject JS API client and main helpers
    js_scripts = """
    <script src="assets/js/api.js" defer></script>
    <script src="assets/js/main.js" defer></script>
    """
    
    # Inject page-specific scripts as well
    if target_file == "calculator.html":
        js_scripts += '<script src="assets/js/calculator.js" defer></script>\n'
    elif target_file in ["connect.html", "careers.html"]:
        js_scripts += '<script src="assets/js/forms.js" defer></script>\n'
        
    content = content.replace("</head>", f"{js_scripts}\n</head>")
    
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
    
    # 5. Fix navigation hyperlinks
    # Replace href="#" for navigation links
    # Desktop navigation menu
    content = content.replace('href="#"', 'href="index.html"') # fallback
    
    # Replace navigation text anchors to their matching pages
    content = re.sub(r'href="[^"]+">Home</a>', 'href="index.html">Home</a>', content)
    content = re.sub(r'href="[^"]+">About</a>', 'href="about.html">About Us</a>', content)
    content = re.sub(r'href="[^"]+">Services</a>', 'href="services.html">Services</a>', content)
    content = re.sub(r'href="[^"]+">Projects</a>', 'href="projects.html">Projects</a>', content)
    content = re.sub(r'href="[^"]+">Products</a>', 'href="products.html">Products</a>', content)
    content = re.sub(r'href="[^"]+">Careers</a>', 'href="careers.html">Careers</a>', content)
    
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
        
        # Replace step 2 fields: Zip Code, Name, Email, Phone
        content = re.sub(
            r'<div>\s*<label class="block text-label-md font-bold text-on-surface mb-2">Zip Code</label>\s*<input class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="90210" type="text"/>\s*</div>',
            r'<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Zip Code</label>\n<input id="calc-zip" name="zipcode" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="226001" type="text"/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Full Name</label>\n<input id="calc-name" name="name" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="John Doe" type="text" required/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Email Address</label>\n<input id="calc-email" name="email" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="john@company.com" type="email" required/>\n</div>\n<div>\n<label class="block text-label-md font-bold text-on-surface mb-2">Phone Number</label>\n<input id="calc-phone" name="phone" class="w-full px-4 py-3 bg-surface-container-lowest border border-surface-container-highest rounded focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" placeholder="+91 98765 43210" type="text"/>\n</div>',
            content
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
        content = re.sub(r'<span class="text-headline-lg font-bold text-white">\$42,850</span>', '<span id="res-savings-lifetime" class="text-headline-lg font-bold text-white">-</span>', content)
        
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
        # Fix download button
        content = re.sub(
            r'<button class="w-full mt-8 bg-on-surface text-white[^>]*>(\s*Download Full Report\s*[^<]*)</button>',
            r'<button onclick="mockDownloadReport()" class="w-full mt-8 bg-on-surface text-white py-3 rounded font-label-md hover:bg-tertiary transition-all flex items-center justify-center gap-2">\1</button>',
            content
        )
        
        # Update Chart Bars
        content = content.replace(
            '<div class="w-full bg-surface-container-high rounded-t h-1/5"></div>\n<div class="w-full bg-primary rounded-t h-[10%]"></div>',
            '<div class="bar-utility w-full bg-surface-container-high rounded-t h-[20%] transition-all duration-1000"></div>\n<div class="bar-solar w-full bg-primary rounded-t h-[5%] transition-all duration-1000"></div>'
        )
        content = content.replace(
            '<div class="w-full bg-surface-container-high rounded-t h-2/5"></div>\n<div class="w-full bg-primary rounded-t h-[12%]"></div>',
            '<div class="bar-utility w-full bg-surface-container-high rounded-t h-[40%] transition-all duration-1000"></div>\n<div class="bar-solar w-full bg-primary rounded-t h-[7%] transition-all duration-1000"></div>'
        )
        content = content.replace(
            '<div class="w-full bg-surface-container-high rounded-t h-3/5"></div>\n<div class="w-full bg-primary rounded-t h-[15%]"></div>',
            '<div class="bar-utility w-full bg-surface-container-high rounded-t h-[60%] transition-all duration-1000"></div>\n<div class="bar-solar w-full bg-primary rounded-t h-[10%] transition-all duration-1000"></div>'
        )
        content = content.replace(
            '<div class="w-full bg-surface-container-high rounded-t h-4/5"></div>\n<div class="w-full bg-primary rounded-t h-[18%]"></div>',
            '<div class="bar-utility w-full bg-surface-container-high rounded-t h-[80%] transition-all duration-1000"></div>\n<div class="bar-solar w-full bg-primary rounded-t h-[15%] transition-all duration-1000"></div>'
        )
        content = content.replace(
            '<div class="w-full bg-surface-container-high rounded-t h-full"></div>\n<div class="w-full bg-primary rounded-t h-[20%]"></div>',
            '<div class="bar-utility w-full bg-surface-container-high rounded-t h-[100%] transition-all duration-1000"></div>\n<div class="bar-solar w-full bg-primary rounded-t h-[20%] transition-all duration-1000"></div>'
        )
        
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
