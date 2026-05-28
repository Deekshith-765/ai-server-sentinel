"""Tests for the Ops Module."""

from predictive_failure import PredictiveFailureDetector
import numpy as np


def test_insufficient_data():
    detector = PredictiveFailureDetector(history_window=10)
    result = detector.predict_failure_risk()
    assert result["risk_level"] == "INSUFFICIENT_DATA"
    print("PASS: insufficient data detection works")


def test_normal_operation():
    detector = PredictiveFailureDetector(history_window=5)
    for i in range(8):
        detector.ingest_metrics({"cpu_percent": 30, "memory_percent": 40, "disk_percent": 50})
    result = detector.predict_failure_risk()
    assert result["risk_level"] in ("NORMAL", "WARNING")
    print("PASS: normal operation detected")


def test_rising_cpu_triggers_alert():
    detector = PredictiveFailureDetector(history_window=5)
    for i in range(10):
        cpu = 30 + i * 7
        detector.ingest_metrics({"cpu_percent": min(100, cpu), "memory_percent": 40, "disk_percent": 50})
    result = detector.predict_failure_risk()
    assert len(result["triggers"]) > 0
    assert result["risk_level"] in ("WARNING", "CRITICAL")
    print("PASS: rising CPU triggers alert")


def test_critical_at_high_usage():
    detector = PredictiveFailureDetector(history_window=3)
    detector.ingest_metrics({"cpu_percent": 98, "memory_percent": 95, "disk_percent": 50})
    detector.ingest_metrics({"cpu_percent": 99, "memory_percent": 96, "disk_percent": 50})
    detector.ingest_metrics({"cpu_percent": 100, "memory_percent": 97, "disk_percent": 50})
    detector.ingest_metrics({"cpu_percent": 100, "memory_percent": 98, "disk_percent": 50})
    result = detector.predict_failure_risk()
    assert result["risk_level"] == "CRITICAL"
    print("PASS: critical risk at high CPU+memory")


def test_calculate_gradient():
    detector = PredictiveFailureDetector()
    grad = detector.calculate_gradient([10, 20, 30, 40, 50])
    assert abs(grad - 10.0) < 0.1
    grad_falling = detector.calculate_gradient([50, 40, 30, 20, 10])
    assert abs(grad_falling - (-10.0)) < 0.1
    print("PASS: gradient calculation correct")


if __name__ == "__main__":
    test_insufficient_data()
    test_normal_operation()
    test_rising_cpu_triggers_alert()
    test_critical_at_high_usage()
    test_calculate_gradient()
    print("\nAll Ops Module tests passed!")
