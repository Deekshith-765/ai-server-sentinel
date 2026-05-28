"""Dev Module: System Monitoring Agent
Tracks CPU, RAM, Disk, and Network like a fitness tracker for your computer."""

import psutil
import time
import json
import csv
from datetime import datetime
from pathlib import Path


class SystemMonitor:
    def __init__(self):
        self.metrics_history = []
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

    def get_cpu(self):
        return {
            "percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }

    def get_memory(self):
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent": mem.percent,
        }

    def get_disk(self):
        disk = psutil.disk_usage("/")
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        }

    def get_network(self):
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": round(net.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net.bytes_recv / (1024**2), 2),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
        }

    def collect_snapshot(self):
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "cpu": self.get_cpu(),
            "memory": self.get_memory(),
            "disk": self.get_disk(),
            "network": self.get_network(),
        }
        self.metrics_history.append(snapshot)
        return snapshot

    def save_json(self, filename=None):
        if filename is None:
            filename = self.log_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.metrics_history, f, indent=2)
        print(f"Saved JSON: {filename}")
        return filename

    def save_csv(self, filename=None):
        if filename is None:
            filename = self.log_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if not self.metrics_history:
            print("No data to save.")
            return
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "cpu_percent", "ram_percent", "disk_percent",
                             "net_sent_mb", "net_recv_mb"])
            for snap in self.metrics_history:
                writer.writerow([
                    snap["timestamp"],
                    snap["cpu"]["percent"],
                    snap["memory"]["percent"],
                    snap["disk"]["percent"],
                    snap["network"]["bytes_sent_mb"],
                    snap["network"]["bytes_recv_mb"],
                ])
        print(f"Saved CSV: {filename}")
        return filename

    def live_monitor(self, interval=2, count=5):
        print(f"Monitoring system for {count} intervals (every {interval}s)...")
        for i in range(count):
            snap = self.collect_snapshot()
            c = snap["cpu"]["percent"]
            m = snap["memory"]["percent"]
            d = snap["disk"]["percent"]
            bar = "█" * int(c // 10) + "░" * (10 - int(c // 10))
            print(f"[{i+1}/{count}] CPU: {c:5.1f}% {bar} | RAM: {m:5.1f}% | DISK: {d:5.1f}%")
            if i < count - 1:
                time.sleep(interval)
        self.save_json()
        self.save_csv()


if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.live_monitor(interval=1, count=5)
