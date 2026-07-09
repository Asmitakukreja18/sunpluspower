import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger("sunplus_email")

class EmailService:
    @staticmethod
    def _send_email_raw(to_email: str, subject: str, html_content: str):
        # Check if SMTP configuration is provided
        if not settings.SMTP_HOST or not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            logger.warning(f"SMTP settings not fully configured. Email to '{to_email}' with subject '{subject}' not sent.")
            return

        try:
            # Create MIME message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM
            msg["To"] = to_email
            
            part = MIMEText(html_content, "html")
            msg.attach(part)
            
            # Connect to SMTP server
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                if settings.SMTP_PORT == 587:
                    server.starttls()
                
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
                
            logger.info(f"Email sent successfully to {to_email} with subject: {subject}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email} with subject: {subject}. Error: {str(e)}")

    def send_lead_notification(self, data: Dict[str, Any]):
        # 1. Acknowledgment to the user
        user_subject = "Thank you for contacting SunPlus Power India"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['name']},</h3>
                <p>Thank you for reaching out to SunPlus Power India. We have received your inquiry regarding <b>{data['subject']}</b>.</p>
                <p>Our engineering team is reviewing your message and will get back to you within 24-48 business hours.</p>
                <br>
                <p><b>Your Message summary:</b></p>
                <p><i>"{data['message']}"</i></p>
                <br>
                <hr>
                <p>Best regards,<br><b>SunPlus Power India Pvt. Ltd.</b><br>Engineering India's Solar Future</p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)
        
        # 2. Internal team notification
        sales_subject = f"[New Lead] inquiry from {data['name']} ({data['company'] or 'No Company'})"
        sales_html = f"""
        <html>
            <body>
                <h2>New Lead Submission</h2>
                <p><b>Name:</b> {data['name']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone']}</p>
                <p><b>Company:</b> {data['company'] or 'N/A'}</p>
                <p><b>Subject:</b> {data['subject']}</p>
                <p><b>Source Page:</b> {data['source_page']}</p>
                <p><b>Message:</b></p>
                <p>{data['message']}</p>
                <br>
                <p><i>View and manage this lead in the SunPlus admin dashboard.</i></p>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_SALES, sales_subject, sales_html)

    def send_calculator_notification(self, data: Dict[str, Any]):
        # 1. Acknowledgment to user with solar results
        user_subject = "Your SunPlus Solar Assessment Report"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['name']},</h3>
                <p>Thank you for using the SunPlus Solar Calculator. Here is the engineering assessment for your installation in <b>{data['location']}</b>:</p>
                <table border="1" cellpadding="8" style="border-collapse: collapse; border-color: #edeef0;">
                    <tr style="background-color: #f8f9fb;"><td><b>Metric</b></td><td><b>Estimated Value</b></td></tr>
                    <tr><td>Monthly Electricity Bill</td><td>₹{data['monthly_bill']}</td></tr>
                    <tr><td>Required Solar System Size</td><td><b>{data['calculated_system_size_kw']} kW</b></td></tr>
                    <tr><td>Estimated Gross Cost</td><td>₹{data['estimated_cost']}</td></tr>
                    <tr><td>Government Subsidy Eligible</td><td>₹{data['subsidy_amount']}</td></tr>
                    <tr><td><b>Net Investment Cost</b></td><td><b>₹{data['net_cost']}</b></td></tr>
                    <tr><td>Annual Savings on Tariff</td><td>₹{data['annual_savings']}</td></tr>
                    <tr><td>Expected Payback Period</td><td><b>{data['payback_years']} Years</b></td></tr>
                    <tr><td>Lifetime Savings (25 Yrs)</td><td>₹{data['lifetime_savings_25yr']}</td></tr>
                    <tr><td>Annual Carbon Offset</td><td>{data['co2_offset_kg']} kg CO2</td></tr>
                </table>
                <p>Our sales engineering team will call you to schedule a site inspection and provide a detailed structural quote.</p>
                <hr>
                <p>Best regards,<br><b>SunPlus Power India Pvt. Ltd.</b></p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)

        # 2. Internal team notification
        sales_subject = f"[Calculator Lead] {data['name']} - {data['calculated_system_size_kw']}kW solar inquiry"
        sales_html = f"""
        <html>
            <body>
                <h2>New Solar Calculator Lead</h2>
                <p><b>Name:</b> {data['name']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone'] or 'N/A'}</p>
                <p><b>Location:</b> {data['location']}</p>
                <p><b>Install Type:</b> {data['install_type']}</p>
                <h3>Calculated System Specs:</h3>
                <ul>
                    <li><b>System Size:</b> {data['calculated_system_size_kw']} kW</li>
                    <li><b>Net Cost:</b> ₹{data['net_cost']} (Gross: ₹{data['estimated_cost']}, Subsidy: ₹{data['subsidy_amount']})</li>
                    <li><b>Payback:</b> {data['payback_years']} Years</li>
                    <li><b>Annual Savings:</b> ₹{data['annual_savings']}</li>
                    <li><b>25-Yr Savings:</b> ₹{data['lifetime_savings_25yr']}</li>
                </ul>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_SALES, sales_subject, sales_html)

    def send_distributor_notification(self, data: Dict[str, Any]):
        # 1. Acknowledgment to user
        user_subject = "SunPlus Power Partner Program Application Received"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['contact_person']},</h3>
                <p>Thank you for applying to the SunPlus Power Authorized Distributor Network. We have received your corporate profile for <b>{data['company_name']}</b>.</p>
                <p>Our channel development manager is reviewing your territory request (<b>{data['region']}</b>) and will contact you directly to discuss commercial terms.</p>
                <hr>
                <p>Best regards,<br><b>SunPlus Power India Channel Development Team</b></p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)

        # 2. Internal sales team notification
        sales_subject = f"[Distributor Application] {data['company_name']} - Region: {data['region']}"
        sales_html = f"""
        <html>
            <body>
                <h2>New Distributor Application</h2>
                <p><b>Company:</b> {data['company_name']}</p>
                <p><b>Contact Person:</b> {data['contact_person']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone']}</p>
                <p><b>Region:</b> {data['region']}</p>
                <p><b>Business Type:</b> {data['business_type']}</p>
                <p><b>Years in Business:</b> {data['years_in_business']}</p>
                <p><b>Message:</b></p>
                <p>{data['message']}</p>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_SALES, sales_subject, sales_html)

    def send_warranty_notification(self, data: Dict[str, Any]):
        # 1. User email
        user_subject = "SunPlus Power Warranty Registration Confirmation"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['customer_name']},</h3>
                <p>We are pleased to confirm that your warranty registration for product type <b>{data['product_type']}</b> has been processed.</p>
                <p><b>Registration details:</b></p>
                <ul>
                    <li><b>Serial Number / Project ID:</b> {data['serial_or_project_id']}</li>
                    <li><b>Installation Date:</b> {data['installation_date']}</li>
                    <li><b>Installer Name:</b> {data['installer_name']}</li>
                </ul>
                <p>Please keep a copy of your purchase invoice. Your warranty is active starting from the installation date.</p>
                <hr>
                <p>Best regards,<br><b>SunPlus Power India Quality Assurance Department</b></p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)

        # 2. Internal accounts email
        internal_subject = f"[Warranty Registration] Serial: {data['serial_or_project_id']} - {data['customer_name']}"
        internal_html = f"""
        <html>
            <body>
                <h2>New Product Warranty Registration</h2>
                <p><b>Customer:</b> {data['customer_name']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone']}</p>
                <p><b>Product Type:</b> {data['product_type']}</p>
                <p><b>Serial/Project ID:</b> {data['serial_or_project_id']}</p>
                <p><b>Installation Date:</b> {data['installation_date']}</p>
                <p><b>Installer:</b> {data['installer_name']}</p>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_ACCOUNTS, internal_subject, internal_html)

    def send_complaint_notification(self, data: Dict[str, Any]):
        # 1. User ticket email
        user_subject = f"[Ticket Open] SunPlus Service Resolution request - Reference: {data['project_or_product_id']}"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['name']},</h3>
                <p>We take engineering performance and service standards very seriously. We have registered your complaint regarding: <b>{data['category'].upper()}</b>.</p>
                <p><b>Details:</b></p>
                <p><i>"{data['description']}"</i></p>
                <p>Our operations & maintenance service manager has been assigned this ticket and will call you shortly.</p>
                <hr>
                <p>Best regards,<br><b>SunPlus Power Customer Support Team</b></p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)

        # 2. Support team email
        support_subject = f"[Urgent Ticket] Complaint: {data['category']} - Reference: {data['project_or_product_id']}"
        support_html = f"""
        <html>
            <body>
                <h2>New Support Ticket / Complaint</h2>
                <p><b>Customer:</b> {data['name']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone']}</p>
                <p><b>Reference ID:</b> {data['project_or_product_id']}</p>
                <p><b>Category:</b> {data['category']}</p>
                <p><b>Photo URL:</b> {data['photo_url'] or 'No attachment'}</p>
                <p><b>Description:</b></p>
                <p>{data['description']}</p>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_SUPPORT, support_subject, support_html)

    def send_career_notification(self, data: Dict[str, Any]):
        # 1. Applicant email
        user_subject = f"Application Received: {data['job_title'] or 'General Application'} - SunPlus Power India"
        user_html = f"""
        <html>
            <body>
                <h3>Dear {data['name']},</h3>
                <p>Thank you for applying to SunPlus Power India. We have received your application for the <b>{data['job_title'] or 'General Inquiry'}</b> opening.</p>
                <p>Our HR department will review your credentials and contact you if your experience aligns with our requirements.</p>
                <hr>
                <p>Best regards,<br><b>SunPlus Power India Human Resources</b></p>
            </body>
        </html>
        """
        self._send_email_raw(data["email"], user_subject, user_html)

        # 2. Internal HR email
        hr_subject = f"[Job Application] {data['name']} - {data['job_title'] or 'General Candidate'}"
        hr_html = f"""
        <html>
            <body>
                <h2>New Job Application</h2>
                <p><b>Applicant Name:</b> {data['name']}</p>
                <p><b>Email:</b> {data['email']}</p>
                <p><b>Phone:</b> {data['phone']}</p>
                <p><b>Applied For:</b> {data['job_title'] or 'General Application'}</p>
                <p><b>Resume Link:</b> <a href="{data['resume_url']}">{data['resume_url']}</a></p>
                <p><b>Cover Letter:</b></p>
                <p>{data['cover_letter'] or 'N/A'}</p>
            </body>
        </html>
        """
        self._send_email_raw(settings.NOTIFICATION_EMAIL_ACCOUNTS, hr_subject, hr_html)

email_service = EmailService()
