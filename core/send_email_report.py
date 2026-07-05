import os
import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load env variables from root or local directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(parent_dir, ".env"))

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email(subject, body_text, body_html=None):
    """Sends an email using configured SMTP settings, or simulates it if unconfigured."""
    print(f"\n--- [EMAIL TRIGGERED] Subject: {subject} ---")
    
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, SENDER_EMAIL, RECIPIENT_EMAIL]):
        print("⚠️ SMTP credentials not fully configured in .env file.")
        print("📺 Simulated Email Content:")
        print(body_text)
        print("-------------------------------------------\n")
        
        # Write to local file as a simulated mailbox for testing/verification
        sim_mailbox_path = os.path.join(parent_dir, "logs", "simulated_emails.log")
        os.makedirs(os.path.dirname(sim_mailbox_path), exist_ok=True)
        with open(sim_mailbox_path, "a") as f:
            f.write(f"\n==================================================\n")
            f.write(f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"FROM: {SENDER_EMAIL or 'mock-sender@darkmatterk3.org'}\n")
            f.write(f"TO: {RECIPIENT_EMAIL or 'user@domain.com'}\n")
            f.write(f"SUBJECT: {subject}\n")
            f.write(f"--------------------------------------------------\n")
            f.write(body_text)
            f.write(f"\n==================================================\n")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL

        # Attach text version
        msg.attach(MIMEText(body_text, "plain"))
        
        # Attach HTML version if available
        if body_html:
            msg.attach(MIMEText(body_html, "html"))

        # Connection establishment
        server = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully via SMTP!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email via SMTP: {e}")
        return False

if __name__ == "__main__":
    # Test script if executed directly
    test_subject = "🌌 DarkMatterK3@Home - Test Notification"
    test_body = f"This is a test notification from the central T4 Compute Node.\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    send_email(test_subject, test_body)
