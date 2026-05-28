"""Sec Module: Log Parser
Reads server logs (text) and intrusion datasets (NSL-KDD, CICIDS2017) CSV files."""

import re
import pandas as pd
from pathlib import Path

REGEX_LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>\w+) "
    r"(?P<message>.+)$"
)
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

NSL_KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
]

CICIDS_CLEAN_PORT = re.compile(r"^(\d+)\s*-\s*\d+$")

# ---------- Text log parsing (original) ----------

def parse_log_line(line):
    match = REGEX_LOG_PATTERN.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    ips = IP_PATTERN.findall(data["message"])
    data["ip_address"] = ips[0] if ips else "N/A"
    data["has_failed_login"] = bool(re.search(r"Failed password", data["message"]))
    data["has_unusual_location"] = bool(re.search(r"Unusual login location", data["message"]))
    data["has_brute_force"] = bool(re.search(r"Brute force", data["message"]))
    data["has_sql_injection"] = bool(re.search(r"SQL injection", data["message"]))
    data["has_ddos"] = bool(re.search(r"DDoS", data["message"]))
    data["is_error"] = data["level"] in ("ERROR", "CRITICAL")
    return data


def parse_log_file(filepath):
    lines = Path(filepath).read_text().strip().split("\n")
    records = [parse_log_line(line) for line in lines]
    records = [r for r in records if r is not None]
    return pd.DataFrame(records)


def extract_log_features(df):
    cols = ["is_error", "has_failed_login", "has_unusual_location",
            "has_brute_force", "has_sql_injection", "has_ddos"]
    return df[cols].astype(int)


# ---------- NSL-KDD dataset loader ----------

def load_nsl_kdd(csv_path):
    df = pd.read_csv(csv_path, header=None, names=NSL_KDD_COLUMNS + ["label", "difficulty"])
    y = (df["label"] != "normal").astype(int)
    X = df.drop(columns=["label", "difficulty"])
    for col in X.select_dtypes(include="object").columns:
        X[col] = X[col].astype("category").cat.codes
    X = X.fillna(0)
    return X, y, df["label"]


# ---------- CICIDS2017 dataset loader ----------

def load_cicids2017(csv_path, sample_rows=None):
    df = pd.read_csv(csv_path, low_memory=False)
    label_col = "Label" if "Label" in df.columns else df.columns[-1]
    y = (df[label_col] != "BENIGN").astype(int)
    X = df.drop(columns=[label_col])
    for col in X.select_dtypes(include="object").columns:
        X[col] = X[col].astype("category").cat.codes
    for col in X.select_dtypes(include="float").columns:
        X[col] = X[col].fillna(0)
    X = X.select_dtypes(include="number").fillna(0)
    if sample_rows and len(X) > sample_rows:
        X = X.sample(sample_rows, random_state=42)
        y = y.loc[X.index]
    return X, y, df[label_col]


# ---------- Unified feature extraction ----------

def extract_features_for_ai(df):
    if "is_error" in df.columns:
        return extract_log_features(df)
    return df.select_dtypes(include="number")
