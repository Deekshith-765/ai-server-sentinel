"""Phase 1: Python Basics - Loops"""

import time

print("=" * 50)
print("MONITORING LOOP SIMULATION")
print("=" * 50)

for second in range(1, 6):
    cpu = 50 + (second * 8)
    ram = 60 + (second * 3)
    print(f"[t+{second}s] CPU: {cpu}% | RAM: {ram}%")
    time.sleep(0.5)

print("\nBatch processing log entries:")
log_entries = [
    "Login from 192.168.1.1",
    "Failed password for root",
    "Login from 10.0.0.5",
    "Failed password for admin x3",
    "sudo command executed",
]
for i, entry in enumerate(log_entries, 1):
    print(f"  [{i}] {entry}")

print("\nContinuous monitoring (press Ctrl+C to stop)...")
try:
    counter = 0
    while counter < 3:
        counter += 1
        print(f"  Heartbeat check #{counter} ... OK")
        time.sleep(1)
except KeyboardInterrupt:
    print("Monitoring stopped.")
