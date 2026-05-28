"""Ops Module: Alert System
Sends notifications via webhook when the predictive system detects a failure risk."""

import json
import requests
from datetime import datetime


class AlertSystem:
    def __init__(self, webhook_url=None, discord_webhook=None):
        self.webhook_url = webhook_url
        self.discord_webhook = discord_webhook
        self.alert_history = []

    def send_alert(self, prediction):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "risk_score": prediction["risk_score"],
            "risk_level": prediction["risk_level"],
            "message": self._format_message(prediction),
            "triggers": prediction.get("triggers", []),
        }
        self.alert_history.append(alert)
        print(f"\nALERT: [{alert['risk_level']}] {alert['message']}")

        if self.webhook_url:
            self._send_webhook(alert)
        if self.discord_webhook:
            self._send_discord(alert)
        return alert

    def _format_message(self, prediction):
        triggers = prediction.get("triggers", [])
        msg = f"System risk level: {prediction['risk_level']} (score: {prediction['risk_score']})"
        if prediction.get("time_to_failure_min"):
            msg += f" | Estimated time to failure: {prediction['time_to_failure_min']} min"
        if triggers:
            msg += f" | Triggers: {'; '.join(triggers)}"
        return msg

    def _send_webhook(self, alert):
        try:
            resp = requests.post(self.webhook_url, json=alert, timeout=10)
            print(f"Webhook sent: {resp.status_code}")
        except Exception as e:
            print(f"Webhook failed: {e}")

    def _send_discord(self, alert):
        color_map = {"CRITICAL": 15158332, "WARNING": 15105570, "NORMAL": 3066993}
        payload = {
            "embeds": [{
                "title": f"🚨 {alert['risk_level']} - System Alert",
                "description": alert["message"],
                "color": color_map.get(alert["risk_level"], 0),
                "fields": [
                    {"name": "Risk Score", "value": str(alert["risk_score"]), "inline": True},
                    {"name": "Time", "value": alert["timestamp"], "inline": True},
                ],
                "timestamp": alert["timestamp"],
            }]
        }
        try:
            resp = requests.post(self.discord_webhook, json=payload, timeout=10)
            print(f"Discord alert sent: {resp.status_code}")
        except Exception as e:
            print(f"Discord alert failed: {e}")


if __name__ == "__main__":
    sample = {
        "risk_score": 0.85,
        "risk_level": "CRITICAL",
        "time_to_failure_min": 3,
        "triggers": ["CPU rising fast (6.2%/interval)", "Memory rising fast (4.1%/interval)"],
    }
    alert_sys = AlertSystem()
    alert_sys.send_alert(sample)
