# Memory & Quick Restart Guide - DarkMatterK3@Home

## Project Overview
DarkMatterK3@Home is a federated research PoC mapping the topological asymmetry ($\Delta = |S_{12} - S_{21}|$) of Calabi-Yau K3 manifolds to detect dark matter signatures using real SDSS/Euclid astronomical data.

---

## 🚀 Quick Start / Restart

### 1. Unified Background Suite (Dashboard + GPU Worker + API Backend)
To launch the entire simulation and telemetry suite manually inside an isolated `tmux` background session:
```bash
./startup.sh
# or
./manage_darkmatter.sh start
```

### 2. Manual Daily Pipeline Orchestration (2-hour Run)
To trigger the automated daily execution immediately:
```bash
python3 core/daily_orchestrator.py
```

### 3. Quick 10-second Simulation Run (Testing the Whole Flow)
To verify the entire processing, telemetry push, email dispatch, and shutdown command work successfully without waiting for 2 hours:
```bash
TEST_PROCESSING_DURATION=10 python3 core/daily_orchestrator.py
```

### 4. Direct Email Report Dispatch Test
To test direct email routing from the VM to Cloud Run SMTP Relay:
```bash
python3 core/send_email_report.py
```

---

## 🛑 Stopping the System
To safely kill all background processes and clear PID files:
```bash
./stop_server.sh
# or
./manage_darkmatter.sh stop
```

---

## 📅 Daily VM lifecycle & Scheduling (Cost Optimization)
The VM has been configured with an automated power schedule using local crontab:
* **08:00 AM (Boot)**: GCP schedules the VM to boot up. The system's `@reboot` crontab automatically executes `startup.sh`, which triggers `core/daily_orchestrator.py`.
* **08:00 AM - 10:00 AM (Processing)**: The daily orchestrator runs the physics worker and telemetry APIs for 2 hours.
* **10:00 AM (Push & Shutdown)**: The orchestrator commits new findings, pushes them to GitHub to update the live Streamlit dashboard, sends final status emails, and executes a secure `poweroff` command to stop the VM and prevent further GCP charges.

---

## 🔒 Security & SMTP Relay Architecture
Google Compute Engine blocks outbound SMTP ports (25, 587, 465) by default. To bypass this, we use a custom decoupled mail delivery architecture:

```mermaid
graph TD
    VM[GCP T4 Compute VM] -- 1. Query Token --> Metadata[GCP Metadata Server]
    Metadata -- 2. Return OIDC Token --> VM
    VM -- 3. Secure POST with OIDC + API Secret --> CR[Cloud Run SMTP Relay]
    CR -- 4. Dispatch Email via TLS --> Gmail[Gmail SMTP Servers]
```

1. **GCP OIDC Authentication**: The VM dynamically requests an Identity Token from the local GCP Metadata Server (`http://metadata.google.internal`) for the target Cloud Run audience.
2. **Secure SMTP Relay**: Hosted under the `/api/v1/send_email` route on Google Cloud Run (`https://darkmatter-dispatcher-1003063861791.europe-west1.run.app`).
3. **Double Verification**: Cloud Run validates BOTH the GCP Identity Token (restricting access to authorized service accounts) and the custom `EMAIL_API_SECRET`.

---

## 💾 Local Environment Configurations (`.env`)
The root `.env` file is git-ignored and contains variables for direct connection fallbacks:
```ini
# Database & Cache Connection
DB_HOST="34.79.45.15"
DB_NAME="darkmatter"
DB_USER="postgres"
DB_PASSWORD="YourSecureDatabasePassword"
DB_PORT=5432
REDIS_HOST="10.227.136.59"
REDIS_PORT=6379

# API Endpoints & Secret Security Keys
API_URL="https://darkmatter-dispatcher-1003063861791.europe-west1.run.app"
EMAIL_API_SECRET="6dfe2a71246d6008c8d0c9e567be2a00b53d4c2cc54fe2ec"

# Fallback SMTP Relay (Used if Cloud Run is unconfigured)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
SENDER_EMAIL="your-email@gmail.com"
RECIPIENT_EMAIL="your-email@gmail.com"
```
