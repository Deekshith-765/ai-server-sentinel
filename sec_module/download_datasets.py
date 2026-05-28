"""Downloads NSL-KDD and CICIDS2017 intrusion detection datasets."""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

DATASETS_DIR = Path(__file__).parent / "datasets"

NSL_KDD_URLS = {
    "KDDTrain+.csv": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.csv",
    "KDDTest+.csv": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.csv",
}

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


def download_file(url, dest):
    print(f"Downloading {url} -> {dest}")
    try:
        urllib.request.urlretrieve(url, dest)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"  Done ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


def download_nsl_kdd():
    print("=" * 50)
    print("Downloading NSL-KDD dataset...")
    print("=" * 50)
    for filename, url in NSL_KDD_URLS.items():
        dest = DATASETS_DIR / filename
        if dest.exists():
            print(f"  Already exists: {filename}")
            continue
        download_file(url, dest)
    print()


def download_cicids2017():
    print("=" * 50)
    print("Downloading CICIDS2017 sample (Wednesday traffic)...")
    print("=" * 50)
    cicids_filename = "CICIDS2017_sample.csv"
    dest = DATASETS_DIR / cicids_filename
    if dest.exists():
        print(f"  Already exists: {cicids_filename}")
        return

    cicids_urls = [
        "https://raw.githubusercontent.com/defcom17/CICIDS2017/master/MachineLearningCSV/CICIDS2017_sample.csv",
        "https://raw.githubusercontent.com/cicids/cicids2017/main/sample.csv",
    ]
    for url in cicids_urls:
        if download_file(url, dest):
            return

    print("  Auto-download unavailable for CICIDS2017 (requires form acceptance).")
    print()
    print("  Manual download options:")
    print("    Option A — Official source (requires filling a form):")
    print("      URL: http://cicresearch.ca/CICDataset/CIC-IDS-2017/")
    print("      Download MachineLearningCSV.zip, extract Wednesday-workingHours.pcap_ISCX.csv")
    print("      Then copy it to: sec_module/datasets/CICIDS2017_sample.csv")
    print()
    print("    Option B — Kaggle (requires kaggle account + API key):")
    print("      pip install kagglehub")
    print("      python3 -c \"import kagglehub;")
    print("      path = kagglehub.dataset_download('dhoogla/cicids2017')\")
    print("      import shutil; shutil.copy(path+'/Bruteforce-Tuesday-no-metadata.parquet', '.')")
    print()
    print("    Option C — Use NSL-KDD instead (already downloaded, simpler):")
    print("      python3 sec_module/ai_classifier.py --dataset nsl-kdd")
    print()


def verify_downloads():
    print("=" * 50)
    print("Verifying downloaded files...")
    print("=" * 50)
    files = list(DATASETS_DIR.glob("*"))
    if not files:
        print("  No files found. You may need to download manually.")
        print("  See: https://github.com/defcom17/NSL_KDD")
        return False
    for f in sorted(files):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name}: {size_kb:.1f} KB")
    print()
    return True


def main():
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    download_nsl_kdd()
    download_cicids2017()
    verify_downloads()

    print("\nNext step: Train the AI classifier with:")
    print("  python3 sec_module/ai_classifier.py --dataset nsl-kdd")


if __name__ == "__main__":
    main()
