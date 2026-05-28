"""Sec Module: AI Security Classifier
Trains on NSL-KDD, CICIDS2017, or text logs to detect attacks."""

import sys
import argparse
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).parent))
from log_parser import (
    parse_log_line, parse_log_file, extract_log_features,
    load_nsl_kdd, load_cicids2017,
)

DATASETS_DIR = Path(__file__).parent / "datasets"


def train_on_text_logs(normal_path, attack_path):
    normal_df = parse_log_file(normal_path)
    attack_df = parse_log_file(attack_path)
    normal_df["label"] = 0
    attack_df["label"] = 1
    df = pd.concat([normal_df, attack_df], ignore_index=True)
    X = extract_log_features(df)
    y = df["label"]
    return X, y, "text logs (regex features)"


def train_on_nsl_kdd():
    train_path = DATASETS_DIR / "KDDTrain+.csv"
    if not train_path.exists():
        print("NSL-KDD not found. Run: python3 sec_module/download_datasets.py")
        return None
    X, y, _ = load_nsl_kdd(train_path)
    return X, y, "NSL-KDD (41 network features)"


def train_on_cicids2017():
    for pattern in ["*.csv"]:
        candidates = list(DATASETS_DIR.glob(pattern))
        cicids = [c for c in candidates if "CICID" in c.name.upper() or "cicid" in c.name]
        if cicids:
            path = cicids[0]
            break
    else:
        print("CICIDS2017 not found in datasets/. Download manually or use nsl-kdd.")
        return None
    X, y, _ = load_cicids2017(path, sample_rows=50000)
    return X, y, "CICIDS2017 (~80 flow features)"


def train_classifier(dataset="text-logs"):
    if dataset == "nsl-kdd":
        result = train_on_nsl_kdd()
    elif dataset == "cicids2017":
        result = train_on_cicids2017()
    else:
        normal = str(Path(__file__).parent / "sample_logs/normal_logs.txt")
        attack = str(Path(__file__).parent / "sample_logs/attack_logs.txt")
        result = train_on_text_logs(normal, attack)

    if result is None:
        return None
    X, y, source = result

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("=" * 60)
    print(f"AI SECURITY CLASSIFIER — {source}")
    print(f"Features: {X.shape[1]} | Train: {len(X_train)} | Test: {len(X_test)}")
    print("=" * 60)
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['Normal', 'Attack'])}")

    top_n = min(10, len(X.columns))
    importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print(f"\nTop {top_n} Features by Importance:")
    for name, val in importances.head(top_n).items():
        print(f"  {name}: {val:.4f}")

    return clf


def predict_log_line(clf, log_line, feature_type="text"):
    parsed = parse_log_line(log_line)
    if parsed is None:
        return "UNPARSABLE"
    df = pd.DataFrame([parsed])
    if feature_type == "text":
        features = extract_log_features(df)
    else:
        return "N/A (model trained on network features)"
    pred = clf.predict(features)[0]
    return "ATTACK" if pred == 1 else "NORMAL"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["text-logs", "nsl-kdd", "cicids2017"],
                        default="text-logs", help="Dataset to train on")
    args = parser.parse_args()
    model = train_classifier(args.dataset)
    if model is None:
        return
    print("\nModel ready. Use --dataset text-logs for log-line predictions.")


if __name__ == "__main__":
    main()
