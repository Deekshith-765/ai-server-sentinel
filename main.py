"""Intelligent Monitoring System - Main Entry Point
Orchestrates all three modules: Dev, Sec, and Ops."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dev_module.system_monitor import SystemMonitor
from sec_module.ai_classifier import train_classifier, predict_log_line, DATASETS_DIR
from ops_module.predictive_failure import PredictiveFailureDetector
from ops_module.alert_system import AlertSystem


def run_full_pipeline():
    print("=" * 60)
    print("INTELLIGENT MONITORING SYSTEM")
    print("=" * 60)

    monitor = SystemMonitor()
    detector = PredictiveFailureDetector()
    alert_sys = AlertSystem()

    print("\n[PHASE 1] Collecting system metrics...")
    for i in range(5):
        snap = monitor.collect_snapshot()
        detector.ingest_metrics({
            "cpu_percent": snap["cpu"]["percent"],
            "memory_percent": snap["memory"]["percent"],
            "disk_percent": snap["disk"]["percent"],
        })
        print(f"  Snapshot {i+1}: CPU={snap['cpu']['percent']}% "
              f"MEM={snap['memory']['percent']}% DISK={snap['disk']['percent']}%")
        time.sleep(0.5)
    monitor.save_json()

    print("\n[PHASE 2] Training AI Security Classifier...")
    has_nsl = (DATASETS_DIR / "KDDTrain+.csv").exists()
    has_cicids = any("CICID" in f.name.upper() for f in DATASETS_DIR.glob("*.csv"))

    if has_nsl:
        dataset = "nsl-kdd"
    elif has_cicids:
        dataset = "cicids2017"
    else:
        dataset = "text-logs"
    print(f"  Using dataset: {dataset}")

    model = train_classifier(dataset)
    if model is None:
        print("  Model training failed, using fallback.")
        return

    if dataset == "text-logs":
        test_lines = [
            "2025-05-27 08:15:30 INFO Login successful for user alice from 192.168.1.10",
            "2025-05-27 03:00:01 ERROR Failed password for root from 10.0.0.99 port 22",
        ]
        for line in test_lines:
            result = predict_log_line(model, line)
            print(f"  [{result}] {line[:60]}...")
    else:
        print(f"  (Text-log prediction skipped: model trained on {dataset} features)")

    print("\n[PHASE 3] Running Predictive Failure Analysis...")
    for i in range(12):
        snap = monitor.collect_snapshot()
        detector.ingest_metrics({
            "cpu_percent": snap["cpu"]["percent"],
            "memory_percent": snap["memory"]["percent"],
            "disk_percent": snap["disk"]["percent"],
        })
    prediction = detector.predict_failure_risk()
    print(f"  Risk Level: {prediction['risk_level']} (score: {prediction['risk_score']})")
    if prediction["triggers"]:
        for t in prediction["triggers"]:
            print(f"  Trigger: {t}")
        alert_sys.send_alert(prediction)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"Metrics collected: {len(monitor.metrics_history)}")
    print(f"AI model trained on: {dataset}")
    print(f"Risk assessment: {prediction['risk_level']}")


if __name__ == "__main__":
    run_full_pipeline()
