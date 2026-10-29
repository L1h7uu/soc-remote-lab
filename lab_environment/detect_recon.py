#!/usr/bin/env python3
"""
Zeek conn.log Port Scan & Reconnaissance Detector
Author: Le Trung Hieu (kenken270506@gmail.com)
Usage: python3 detect_recon.py [conn.log]
"""

import sys
from collections import defaultdict

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample_logs/conn.log"

def main():
    print("=" * 60)
    print("  ZEEK CONN.LOG RECONNAISSANCE & PORT SCAN DETECTOR")
    print(f"  Target Log: {LOG_FILE}")
    print("=" * 60)

    # Dictionary: src_ip -> set of dest_ports where conn_state == 'S0' (SYN sent, no response)
    syn_scans = defaultdict(lambda: {"ports": set(), "targets": set(), "total": 0})

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 12:
                    continue
                
                # Zeek standard fields:
                # 0: ts, 2: id.orig_h, 3: id.orig_p, 4: id.resp_h, 5: id.resp_p, 11: conn_state
                src_ip = parts[2]
                dst_ip = parts[4]
                dst_port = parts[5]
                conn_state = parts[11]

                if conn_state in ["S0", "REJ"]:
                    syn_scans[src_ip]["ports"].add(dst_port)
                    syn_scans[src_ip]["targets"].add(dst_ip)
                    syn_scans[src_ip]["total"] += 1

    except FileNotFoundError:
        print(f"[!] Error: File '{LOG_FILE}' not found.")
        return

    print("\n[+] Detection Results (Suspicious Reconnaissance Activity):")
    detected = False
    for ip, data in syn_scans.items():
        unique_ports = len(data["ports"])
        if unique_ports >= 5 or data["total"] >= 10:
            detected = True
            print(f"\n[ALERT] Potential Port Scanner Detected: {ip}")
            print(f"        - Total Unanswered Connection Attempts: {data['total']}")
            print(f"        - Unique Destination Ports Probed: {unique_ports}")
            print(f"        - Target Hosts: {', '.join(data['targets'])}")
            sample_ports = sorted(list(data["ports"]), key=lambda x: int(x) if x.isdigit() else 0)[:10]
            print(f"        - Sample Ports: {', '.join(sample_ports)}")

    if not detected:
        print("    No abnormal scanning patterns identified based on threshold.")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
