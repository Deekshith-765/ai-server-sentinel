"""Ops Module: Predictive Failure System
Analyzes time-series metrics to predict crashes before they happen."""

import numpy as np
import json
import time
from datetime import datetime, timedelta
from pathlib import Path


class PredictiveFailureDetector:
    def __init__(self, history_window=10):
        self.history = []
        self.history_window = history_window
        self.alert_thresholds = {
            "cpu_gradient": 5.0,
            "memory_gradient": 4.0,
            "disk_gradient": 2.0,
        }

    def ingest_metrics(self, metrics_dict):
        self.history.append({
            "timestamp": datetime.now(),
            "cpu": metrics_dict.get("cpu_percent", 0),
            "memory": metrics_dict.get("memory_percent", 0),
            "disk": metrics_dict.get("disk_percent", 0),
        })
        if len(self.history) > self.history_window * 3:
            self.history.pop(0)

    def calculate_gradient(self, values):
        if len(values) < 3:
            return 0.0
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        return coeffs[0]

    def predict_failure_risk(self):
        if len(self.history) < self.history_window:
            return {
                "risk_score": 0.0,
                "risk_level": "INSUFFICIENT_DATA",
                "time_to_failure_min": None,
                "cpu_gradient": 0,
                "memory_gradient": 0,
                "disk_gradient": 0,
                "triggers": [],
            }

        recent = self.history[-self.history_window:]
        cpu_vals = [h["cpu"] for h in recent]
        mem_vals = [h["memory"] for h in recent]
        disk_vals = [h["disk"] for h in recent]

        cpu_grad = self.calculate_gradient(cpu_vals)
        mem_grad = self.calculate_gradient(mem_vals)
        disk_grad = self.calculate_gradient(disk_vals)

        triggers = []
        if cpu_grad > self.alert_thresholds["cpu_gradient"]:
            triggers.append(f"CPU rising fast ({cpu_grad:.1f}%/interval)")
        if mem_grad > self.alert_thresholds["memory_gradient"]:
            triggers.append(f"Memory rising fast ({mem_grad:.1f}%/interval)")
        if disk_grad > self.alert_thresholds["disk_gradient"]:
            triggers.append(f"Disk filling fast ({disk_grad:.1f}%/interval)")

        raw_risk = sum([
            max(0, cpu_grad / self.alert_thresholds["cpu_gradient"]),
            max(0, mem_grad / self.alert_thresholds["memory_gradient"]),
            max(0, disk_grad / self.alert_thresholds["disk_gradient"]),
        ]) / 3
        risk_score = min(1.0, raw_risk)

        if risk_score > 0.7:
            risk_level = "CRITICAL"
            time_to_failure = max(3, int(10 - risk_score * 10))
        elif risk_score > 0.4:
            risk_level = "WARNING"
            time_to_failure = max(5, int(15 - risk_score * 10))
        else:
            risk_level = "NORMAL"
            time_to_failure = None

        latest_cpu = cpu_vals[-1]
        latest_mem = mem_vals[-1]
        if latest_cpu > 95 and latest_mem > 90:
            risk_score = min(1.0, risk_score + 0.2)
            risk_level = "CRITICAL"
            triggers.append("CRITICAL: CPU+Memory both near max")
            time_to_failure = 1

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "time_to_failure_min": time_to_failure,
            "cpu_gradient": round(cpu_grad, 2),
            "memory_gradient": round(mem_grad, 2),
            "disk_gradient": round(disk_grad, 2),
            "triggers": triggers,
            "latest_cpu": latest_cpu,
            "latest_memory": latest_mem,
        }

    def simulate(self, steps=15):
        cpu = 30.0
        mem = 40.0
        disk = 50.0
        print("=" * 60)
        print("PREDICTIVE FAILURE SIMULATION")
        print("=" * 60)
        for i in range(steps):
            cpu += np.random.uniform(-2, 6)
            mem += np.random.uniform(-1, 4)
            disk += np.random.uniform(-0.5, 1)
            cpu = max(0, min(100, cpu))
            mem = max(0, min(100, mem))
            disk = max(0, min(100, disk))
            self.ingest_metrics({
                "cpu_percent": cpu,
                "memory_percent": mem,
                "disk_percent": disk,
            })
            prediction = self.predict_failure_risk()
            bar_len = int(cpu // 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"[{i+1:2d}/{steps}] CPU:{cpu:5.1f} MEM:{mem:5.1f} DSK:{disk:5.1f} "
                  f"| Risk: {prediction['risk_level']:8s} ({prediction['risk_score']:.2f})"
                  f"{' ⚠ ' + str(prediction['triggers']) if prediction['triggers'] else ''}")
            time.sleep(0.3)
        return prediction


if __name__ == "__main__":
    detector = PredictiveFailureDetector()
    result = detector.simulate()
    print("\nFinal Prediction:", json.dumps(result, indent=2))
