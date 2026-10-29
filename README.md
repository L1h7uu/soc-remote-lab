# SOC Incident Investigation & Remote Lab
**Author:** Le Trung Hieu ([@L1h7uu](https://github.com/L1h7uu))  
**Email:** kenken270506@gmail.com  
**Target:** SOC Tier 1 / Security Monitoring & Threat Triage  

---

## 📌 Project Overview
This repository provides an automated, containerized **Security Operations Center (SOC) Investigation Lab** designed for network traffic analysis, log correlation, and incident triage.

It includes:
1. **Interactive Web Interface:** Access terminal and investigative tools directly via browser using Guacamole & Web Terminal (`ttyd`).
2. **Detection & Triage Scripts:** Custom Python automation to parse Suricata EVE JSON alerts and detect reconnaissance patterns (port scanning) from Zeek `conn.log`.
3. **Artifact Datasets:** Sample IDS/IPS alerts, flow logs, and PCAP data representing real-world attack chains (Reconnaissance -> Web Shell -> Reverse Shell C2).

---

## 🛠️ Architecture & Components
```
[ Browser / Recruiter ] 
       │ (HTTPS via Cloudflare Zero Trust Tunnel)
       ▼
[ Cloudflare Edge ]
       │ (Secure Tunnel)
       ▼
[ Local Docker Container ]
       ├── ttyd / Guacamole (Port 7681 / 8080)
       ├── Detection & Triage Engine (Python)
       └── Log Data Store (Zeek, Suricata EVE JSON, PCAP)
```

- **Suricata Alert Triage (`parse_eve_alerts.py`):** Automatically categorizes alerts by severity, identifies top attacker IPs, targeted services, and extracts High-severity triggers.
- **Zeek Reconnaissance Detector (`detect_recon.py`):** Correlates `S0` (SYN sent without response) connection states across multiple ports to flag automated scanning activity.

---

## 🚀 Quick Start (Running the Lab)

### 1. Start the Environment
Make sure Docker is installed and running:
```bash
docker compose up -d
```

### 2. Access the Terminal via Browser
Open your browser and navigate to:
```
http://localhost:7681
```
- **Username:** `guest`
- **Password:** `Demo@123`

### 3. Run Analysis Tools
Inside the terminal, execute the triage tools:
```bash
# Triage Suricata alerts
python3 parse_eve_alerts.py sample_logs/eve.json

# Detect reconnaissance in Zeek flows
python3 detect_recon.py sample_logs/conn.log
```

---

## 🌐 Public Remote Access (For Interviewers & Recruiters)
To expose this lab securely over HTTPS without port forwarding:
```powershell
# Using Cloudflare Tunnel
cloudflared tunnel --url http://localhost:7681
```
The resulting URL (e.g., `https://<unique-id>.trycloudflare.com`) allows direct browser access to the live lab session.

---

## 📜 License
MIT License. Created for technical demonstration, CTF forensics research, and SOC Tier 1 operational training.
