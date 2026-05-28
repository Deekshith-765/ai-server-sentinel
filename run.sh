#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -r requirements.txt -q

if [ ! -f sec_module/datasets/KDDTrain+.csv ]; then
    echo "Downloading NSL-KDD dataset..."
    python3 sec_module/download_datasets.py
fi

python3 main.py
