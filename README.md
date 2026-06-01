<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=DevSecOps%20Intelligent%20Monitoring%20System&fontSize=30&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Real-Time%20Metrics%20%7C%20ML%20Security%20Classification%20%7C%20Predictive%20Failure%20Detection&descAlignY=65&descSize=13" width="100%"/>

 
## Overview
 
An automated, containerized server monitoring pipeline that unifies **real-time metric collection**, **machine learning-driven security classification**, and **predictive operational failure detection** into a single DevSecOps workflow.
 
---
 
## Architecture
 
```
Collect Metrics  -->  Train / Evaluate Classifier  -->  Predict Failure Risk  -->  Trigger Alerts
      |                          |                               |                        |
 dev_module                 sec_module                      ops_module              Webhook /
 (psutil agent)          (RandomForest IDS)            (Gradient Analysis)         Discord
```
 
---
 
## Module Breakdown
 
### `dev_module` — Telemetry & Data Collection
 
> Lightweight agent using `psutil` to capture live, high-frequency system metrics.
 
- Collects **CPU, Memory, Disk, and Network** traffic in real time
- Auto-exports structured data to **JSON** for downstream consumption
---
 
### `sec_module` — AI Security Classifier
 
> Intrusion detection engine built on `scikit-learn`.
 
- Accepts **text logs** or tabular network benchmark datasets
- Trained and evaluated on **NSL-KDD** and **CICIDS2017**
- Classifies traffic as `NORMAL` or `ATTACK` with ensemble voting
| Dataset | Use Case |
|:---|:---|
| NSL-KDD | Complex network flow anomalies & known attack signatures |
| CICIDS2017 | Port scans, DoS, and advanced intrusion patterns |
| Custom Logs | Direct feature extraction from live server text logs |
 
---
 
### `ops_module` — Predictive Failure & Alerting
 
> Proactive health engine for catching crashes before they happen.
 
- Ingests **time-series metrics** and computes system gradient degradation
- Outputs risk levels: `NORMAL` -> `WARNING` -> `CRITICAL`
- Calculates **Time-to-Failure (TTF)** estimates
- Dispatches alerts via **Webhooks** or **Discord**
---
 
### `dashboard/` — Visualization Layer
 
> Modern, decoupled frontend + backend interface.
 
| Layer | Technology | Role |
|:---|:---|:---|
| Backend | `FastAPI` + `uvicorn` | High-performance REST API serving metrics & predictions |
| Frontend | `Streamlit` | Real-time analytics dashboard with tabbed views |
 
---
 
### `phase1_basics/` — Foundation Layer
 
> Core structural Python engineering modules serving as the pipeline's automation baseline.
 
- Variables, conditionals, loops, functions
- Provides reusable scripting patterns for the pipeline automation scripts
---
 
## Tech Stack
 
**Infrastructure**
 
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
 
**Core Libraries**
 
![Psutil](https://img.shields.io/badge/psutil-4EAA25?style=flat-square&logo=linux&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
 
**Frameworks**
 
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
 
---
 
## Project Structure
 
```
devsecops-monitor/
├── dev_module/
│   ├── agent.py              # psutil live telemetry collector
│   └── exporter.py           # JSON structured export
├── sec_module/
│   ├── classifier.py         # RandomForest IDS engine
│   ├── feature_extractor.py  # Log -> feature vector pipeline
│   └── datasets/             # NSL-KDD, CICIDS2017
├── ops_module/
│   ├── predictor.py          # Gradient time-series engine
│   └── alerting.py           # Webhook / Discord dispatcher
├── dashboard/
│   ├── main.py               # FastAPI REST backend
│   └── app.py                # Streamlit frontend
├── phase1_basics/
│   └── *.py                  # Core Python foundation modules
├── Dockerfile
├── docker-compose.yml
└── README.md
```
 
---
 
## Quick Start
 
```bash
# 1. Clone the repository
git clone https://github.com/deekshiths/devsecops-monitor.git
cd devsecops-monitor
 
# 2. Build and start all services (single command)
docker-compose up --build
 
# 3. Open the dashboard
# Streamlit  ->  http://localhost:8501
# FastAPI     ->  http://localhost:8000/docs
```
 
---
 
## Pipeline Flow
 
```
1. dev_module   ->  Collect CPU / RAM / Disk / Network metrics
2. sec_module   ->  Classify traffic logs (NORMAL / ATTACK)
3. ops_module   ->  Compute gradients -> Risk Score -> TTF estimate
4. Alerting     ->  Webhook / Discord notification on CRITICAL threshold
5. Dashboard    ->  FastAPI + Streamlit live visualization
```
 
---
 
<div align="center">
  
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>
