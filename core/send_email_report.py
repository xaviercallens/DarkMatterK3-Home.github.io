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

API_URL = os.getenv("API_URL")
EMAIL_API_SECRET = os.getenv("EMAIL_API_SECRET")

# Local SMTP variables as fallback
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def get_gcp_identity_token(audience):
    """Retrieves an OIDC identity token from the GCP Metadata Server for the given audience."""
    import requests
    url = f"http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience={audience}"
    headers = {"Metadata-Flavor": "Google"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        # Expected if running locally where the metadata server doesn't exist
        pass
    return None

def _log_simulated_email(subject, body_text):
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

def send_email(subject, body_text, body_html=None):
    """Sends an email using configured SMTP settings, or via Cloud Run SMTP Relay, or simulates it."""
    print(f"\n--- [EMAIL TRIGGERED] Subject: {subject} ---")
    
    # 1. Attempt sending via Cloud Run SMTP Relay API
    if API_URL and EMAIL_API_SECRET:
        print(f"📡 Routing email via Cloud Run SMTP Relay API at {API_URL}...")
        try:
            import requests
            url = f"{API_URL.rstrip('/')}/api/v1/send_email"
            payload = {
                "subject": subject,
                "body": body_text,
                "secret_key": EMAIL_API_SECRET
            }
            
            headers = {}
            # Try to get GCP identity token if on GCP Compute Engine VM
            token = get_gcp_identity_token(API_URL)
            if token:
                headers["Authorization"] = f"Bearer {token}"
                print("🔒 Authenticated using GCP metadata identity token.")
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("status") == "success":
                    print("✅ Email sent successfully via Cloud Run SMTP Relay!")
                    return True
                elif res_data.get("status") == "simulated":
                    print(f"ℹ️ Cloud Run SMTP Relay is running in simulated mode: {res_data.get('message')}")
                    _log_simulated_email(subject, body_text)
                    return True
            else:
                print(f"⚠️ Cloud Run SMTP Relay API returned error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Failed to route email via Cloud Run SMTP Relay API: {e}")
            print("Falling back to local SMTP/simulation...")

    # 2. Local SMTP configuration check
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, SENDER_EMAIL, RECIPIENT_EMAIL]):
        print("⚠️ SMTP credentials not fully configured in .env file.")
        _log_simulated_email(subject, body_text)
        return False

    # 3. Direct local SMTP fallback
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
        
        print("✅ Email sent successfully via direct local SMTP!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email via direct local SMTP: {e}")
        return False

if __name__ == "__main__":
    # Test script if executed directly
    test_subject = "🌌 DarkMatterK3@Home - Test Notification"
    test_body = f"This is a test notification from the central T4 Compute Node.\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    send_email(test_subject, test_body)
