#!/usr/bin/env python3
"""
Suricata EVE JSON Alert Parser & Triage Tool
Author: Le Trung Hieu (kenken270506@gmail.com)
Usage: python3 parse_eve_alerts.py [log_file]
"""

import json
import sys
from collections import Counter
from datetime import datetime

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample_logs/eve.json"

def main():
    print("=" * 60)
    print("  SOC TRIAGE TOOL: SURICATA EVE.JSON ALERT ANALYZER")
    print(f"  Target Log: {LOG_FILE}")
    print("=" * 60)

    alerts = []
    src_ips = Counter()
    dest_ips = Counter()
    signatures = Counter()
    severities = Counter()

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record.get("event_type") == "alert":
                        alert_data = record.get("alert", {})
                        alerts.append(record)
                        src_ips[record.get("src_ip")] += 1
                        dest_ips[record.get("dest_ip")] += 1
                        signatures[alert_data.get("signature", "Unknown Signature")] += 1
                        severities[alert_data.get("severity", 3)] += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"[!] Error: File '{LOG_FILE}' not found.")
        return

    print(f"\n[*] Total Alerts Detected: {len(alerts)}")
    print("\n[+] Alert Breakdown by Severity (1: High, 2: Medium, 3: Low):")
    for sev, count in sorted(severities.items()):
        sev_label = {1: "HIGH (Critical)", 2: "MEDIUM", 3: "LOW/INFO"}.get(sev, str(sev))
        print(f"    - Severity {sev} [{sev_label}]: {count} occurrences")

    print("\n[+] Top Attacker IPs (Source):")
    for ip, count in src_ips.most_common(5):
        print(f"    - {ip:18} : {count} events")

    print("\n[+] Top Targeted IPs (Destination):")
    for ip, count in dest_ips.most_common(5):
        print(f"    - {ip:18} : {count} events")

    print("\n[+] Top Triggered Signatures:")
    for sig, count in signatures.most_common(5):
        print(f"    - [{count:2d}x] {sig}")

    print("\n" + "=" * 60)
    print("  RECENT HIGH-SEVERITY ALERTS (TRIAGE VIEW)")
    print("=" * 60)
    high_sev = [a for a in alerts if a.get("alert", {}).get("severity") == 1]
    for idx, alert in enumerate(high_sev[:3], 1):
        ts = alert.get("timestamp", "")
        src = f"{alert.get('src_ip')}:{alert.get('src_port')}"
        dst = f"{alert.get('dest_ip')}:{alert.get('dest_port')}"
        sig = alert.get("alert", {}).get("signature")
        category = alert.get("alert", {}).get("category", "General")
        print(f"[{idx}] {ts} | {category}")
        print(f"    Flow: {src} -> {dst}")
        print(f"    Signature: {sig}\n")

if __name__ == "__main__":
    main()
