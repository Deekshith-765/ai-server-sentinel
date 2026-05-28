"""Tests for the Sec Module — text logs, NSL-KDD, and CICIDS2017."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from log_parser import (
    parse_log_line, parse_log_file, extract_log_features,
    load_nsl_kdd, load_cicids2017,
)
from ai_classifier import train_classifier, predict_log_line


# ====== Text log tests (original) ======

def test_parse_normal_line():
    line = "2025-05-27 08:15:30 INFO Login successful for user alice from 192.168.1.10"
    result = parse_log_line(line)
    assert result is not None
    assert result["level"] == "INFO"
    assert result["ip_address"] == "192.168.1.10"
    assert result["has_failed_login"] is False
    print("PASS: normal line parsed correctly")


def test_parse_attack_line():
    line = "2025-05-27 03:00:01 ERROR Failed password for root from 10.0.0.99 port 22"
    result = parse_log_line(line)
    assert result["level"] == "ERROR"
    assert result["has_failed_login"] is True
    assert result["is_error"] is True
    print("PASS: attack line parsed correctly")


def test_parse_log_file():
    df = parse_log_file("sample_logs/normal_logs.txt")
    assert len(df) > 0
    assert "timestamp" in df.columns
    assert "ip_address" in df.columns
    print("PASS: log file parsed into DataFrame")


def test_log_feature_extraction():
    df = parse_log_file("sample_logs/attack_logs.txt")
    features = extract_log_features(df)
    assert isinstance(features, pd.DataFrame)
    assert features.shape[1] == 6
    assert features.iloc[0]["has_failed_login"] == 1
    print("PASS: log features extracted correctly")


def test_brute_force_detection():
    line = "2025-05-27 03:04:00 WARN Brute force pattern detected: 50 failed logins"
    result = parse_log_line(line)
    assert result["has_brute_force"] is True
    print("PASS: brute force pattern detected")


def test_predict_log_line():
    model = train_classifier("text-logs")
    result = predict_log_line(model, "2025-05-27 08:15:30 INFO Login successful")
    assert result == "NORMAL"
    result2 = predict_log_line(model, "2025-05-27 03:00:01 ERROR Failed password for root")
    assert result2 == "ATTACK"
    print("PASS: text-log predictions correct")


# ====== NSL-KDD tests ======

NSL_TRAIN = Path(__file__).parent / "datasets/KDDTrain+.csv"
NSL_TEST = Path(__file__).parent / "datasets/KDDTest+.csv"


def test_nsl_kdd_load():
    if not NSL_TRAIN.exists():
        print("SKIP: NSL-KDD training set not downloaded.")
        return
    X, y, labels = load_nsl_kdd(NSL_TRAIN)
    assert len(X) > 0
    assert len(X) == len(y)
    assert X.shape[1] == 41
    assert set(y.unique()) <= {0, 1}
    print(f"PASS: NSL-KDD loaded ({len(X)} rows, {X.shape[1]} features)")


def test_nsl_kdd_label_distribution():
    if not NSL_TRAIN.exists():
        print("SKIP: NSL-KDD not downloaded.")
        return
    _, _, labels = load_nsl_kdd(NSL_TRAIN)
    attack_pct = (labels != "normal").mean() * 100
    assert 30 < attack_pct < 70
    print(f"PASS: NSL-KDD has {attack_pct:.0f}% attacks (balanced)")


def test_nsl_kdd_model():
    if not NSL_TRAIN.exists():
        print("SKIP: NSL-KDD not downloaded.")
        return
    model = train_classifier("nsl-kdd")
    assert model is not None
    print("PASS: NSL-KDD model trained successfully")


# ====== CICIDS2017 tests ======

CICIDS_PATH = next((f for f in Path(__file__).parent.glob("datasets/*.csv")
                     if "CICID" in f.name.upper()), None)


def test_cicids_load():
    if CICIDS_PATH is None:
        print("SKIP: CICIDS2017 not found.")
        return
    X, y, labels = load_cicids2017(CICIDS_PATH, sample_rows=1000)
    assert len(X) > 0
    assert len(X) == len(y)
    print(f"PASS: CICIDS2017 loaded ({len(X)} rows, {X.shape[1]} features)")


def test_cicids_model():
    if CICIDS_PATH is None:
        print("SKIP: CICIDS2017 not found.")
        return
    model = train_classifier("cicids2017")
    assert model is not None
    print("PASS: CICIDS2017 model trained successfully")


if __name__ == "__main__":
    test_parse_normal_line()
    test_parse_attack_line()
    test_parse_log_file()
    test_log_feature_extraction()
    test_brute_force_detection()
    test_predict_log_line()
    test_nsl_kdd_load()
    test_nsl_kdd_label_distribution()
    test_nsl_kdd_model()
    test_cicids_load()
    test_cicids_model()
    print("\nAll Sec Module tests passed!")
