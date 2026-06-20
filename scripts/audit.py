#!/usr/bin/env python3
import subprocess, datetime, time, os

LOG = "/var/log/audit.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def get_cpu():
    r = subprocess.run(["top","-bn1"], capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if "Cpu(s)" in line:
            return line.strip()
    return "N/A"

def get_ram():
    r = subprocess.run(["free","-h"], capture_output=True, text=True)
    lines = r.stdout.strip().split("\n")
    return lines[1] if len(lines) > 1 else "N/A"

def get_disk():
    r = subprocess.run(["df","-h","/"], capture_output=True, text=True)
    lines = r.stdout.strip().split("\n")
    return lines[1] if len(lines) > 1 else "N/A"

def get_ssh():
    r = subprocess.run(["who"], capture_output=True, text=True)
    sessions = [l for l in r.stdout.strip().split("\n") if l]
    return f"{len(sessions)} session(s) active(s)"

while True:
    log("=== Audit système ===")
    log(f"CPU  : {get_cpu()}")
    log(f"RAM  : {get_ram()}")
    log(f"DISK : {get_disk()}")
    log(f"SSH  : {get_ssh()}")
    time.sleep(300)  # 5 minutes
