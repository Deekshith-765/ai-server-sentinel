"""Dashboard: Streamlit Frontend
Interactive web dashboard for the Intelligent Monitoring System."""

import streamlit as st
import requests
import pandas as pd
import time

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Intelligent Monitoring System", layout="wide")
st.title("🖥️ Intelligent Monitoring System Dashboard")
st.markdown("Real-time system health, security AI, and predictive failure monitoring.")

tab1, tab2, tab3 = st.tabs(["📊 System Health", "🛡️ Security Logs", "🔮 Failure Prediction"])

with tab1:
    st.header("System Metrics")
    try:
        history = requests.get(f"{API_BASE}/api/metrics/history", timeout=5).json()
        if isinstance(history, list) and history:
            df = pd.DataFrame(history)
            cols = st.columns(4)
            latest = history[-1]
            cols[0].metric("CPU", f'{latest.get("cpu_percent", "N/A")}%')
            cols[1].metric("Memory", f'{latest.get("memory_percent", "N/A")}%')
            cols[2].metric("Disk", f'{latest.get("disk_percent", "N/A")}%')
            cols[3].metric("Network Sent", f'{latest.get("net_sent_mb", "N/A")} MB')
            st.line_chart(df.select_dtypes(include="number"))
        else:
            st.info("No metrics available yet. Start the Dev Module to collect data.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API backend. Run `uvicorn dashboard.app:app` first.")

with tab2:
    st.header("AI Security Classifier")
    st.markdown("Upload a log file or paste a log line to classify it as Normal or Attack.")
    log_input = st.text_area("Paste a log line:", height=80)
    if st.button("Classify") and log_input:
        st.success("This is a demo - connect the Sec Module for live predictions.")
        if "ERROR" in log_input or "Failed password" in log_input:
            st.error("🔴 Classification: **ATTACK**")
        else:
            st.success("🟢 Classification: **NORMAL**")

with tab3:
    st.header("Predictive Failure Analysis")
    try:
        pred = requests.get(f"{API_BASE}/api/predictions/latest", timeout=5).json()
        if "risk_level" in pred:
            risk = pred["risk_level"]
            score = pred.get("risk_score", 0)
            color = "red" if risk == "CRITICAL" else "orange" if risk == "WARNING" else "green"
            st.markdown(f"### Risk Level: <span style='color:{color}'>{risk}</span>", unsafe_allow_html=True)
            st.metric("Risk Score", f"{score:.2f}")
            if pred.get("time_to_failure_min"):
                st.warning(f"⏱ Estimated time to failure: {pred['time_to_failure_min']} minutes")
            if pred.get("triggers"):
                st.markdown("**Triggers:**")
                for t in pred["triggers"]:
                    st.markdown(f"- {t}")
        else:
            st.info("No predictions yet. Run the Ops Module to start analysis.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API backend.")

if st.button("🔄 Refresh All Data"):
    st.rerun()
