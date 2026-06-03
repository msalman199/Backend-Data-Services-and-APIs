# 🚨 Alert Rule Implementation 

<div align="center">

# 🛡️ Prometheus Alerting & Alertmanager Implementation

![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Alertmanager](https://img.shields.io/badge/Alertmanager-FF6B35?style=for-the-badge)
![Node Exporter](https://img.shields.io/badge/Node_Exporter-4CAF50?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Ubuntu%2020.04+-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![YAML](https://img.shields.io/badge/YAML-000000?style=for-the-badge&logo=yaml&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### 📊 Configure Monitoring Alerts • Route Notifications • Validate Alerting Pipelines

</div>

---

# 📖 Overview

This lab demonstrates how to implement a complete alerting workflow using:

- 📈 Prometheus Alert Rules
- 🚨 Alertmanager
- 🖥️ Node Exporter
- 🐍 Python Webhook Receiver
- 🔔 Threshold-Based Monitoring

You will learn how to create alerts, route notifications, test failures, and validate monitoring pipelines.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Configure alert rules in Prometheus

✅ Define threshold-based alert conditions

✅ Implement Alertmanager routing

✅ Validate alert firing and resolution

✅ Troubleshoot common alerting issues

---

# 📋 Prerequisites

| Requirement | Description |
|------------|-------------|
| 🖥️ Linux Skills | Basic command line usage |
| 📊 Monitoring Knowledge | Understanding of metrics |
| 📄 YAML | Basic YAML syntax |
| 🌐 Networking | Basic networking concepts |
| 🔍 Monitoring Labs | Previous Prometheus experience |

---

# 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │  Node Exporter  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Prometheus    │
                 │ Alert Rules     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Alertmanager   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Webhook Server  │
                 └─────────────────┘
```

---

# 🛠️ Environment Setup

## 💻 System Requirements

| Resource | Requirement |
|-----------|-------------|
| OS | Ubuntu 20.04+ / CentOS 8+ |
| Memory | 2 GB Minimum |
| Storage | 10 GB Minimum |
| Privileges | sudo/root |

---

# 📦 Install Required Components

## 🔄 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 📥 Install Utilities

```bash
sudo apt install -y wget tar
```

---

## 📈 Install Prometheus

```bash
cd /tmp

wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz

tar xvfz prometheus-2.45.0.linux-amd64.tar.gz

sudo mv prometheus-2.45.0.linux-amd64 /opt/prometheus
```

---

## 🚨 Install Alertmanager

```bash
wget https://github.com/prometheus/alertmanager/releases/download/v0.26.0/alertmanager-0.26.0.linux-amd64.tar.gz

tar xvfz alertmanager-0.26.0.linux-amd64.tar.gz

sudo mv alertmanager-0.26.0.linux-amd64 /opt/alertmanager
```

---

## 🖥️ Install Node Exporter

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz

tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz

sudo mv node_exporter-1.6.1.linux-amd64 /opt/node_exporter
```

---

# 🚀 Task 1: Define Alert Rules

---

## 📁 Step 1: Create Rules Directory

```bash
sudo mkdir -p /opt/prometheus/rules

cd /opt/prometheus/rules
```

---

## 📝 Step 2: Create Alert Rules File

Create:

```bash
sudo nano /opt/prometheus/rules/alerts.yml
```

Add:

```yaml
groups:
  - name: system_alerts
    interval: 30s

    rules:

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 2m

        labels:
          severity: warning

        annotations:
          summary: "High CPU usage detected"
          description: "CPU utilization on {{ $labels.instance }} exceeded 80%."

      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m

        labels:
          severity: critical

        annotations:
          summary: "High Memory Usage"
          description: "Memory usage on {{ $labels.instance }} exceeded 85%."

      - alert: DiskSpaceLow
        expr: (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100 > 90
        for: 1m

        labels:
          severity: critical

        annotations:
          summary: "Disk Space Low"
          description: "Disk usage on {{ $labels.instance }} exceeded 90%."
```

---

## 📌 Alert Rule Explanation

| Alert | Threshold | Duration |
|---------|-----------|-----------|
| CPU | >80% | 2 Minutes |
| Memory | >85% | 5 Minutes |
| Disk | >90% | 1 Minute |

---

## ⚙️ Step 3: Configure Prometheus

Edit:

```bash
sudo nano /opt/prometheus/prometheus.yml
```

Configuration:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093

rule_files:
  - "rules/*.yml"

scrape_configs:

  - job_name: prometheus
    static_configs:
      - targets:
          - localhost:9090

  - job_name: node
    static_configs:
      - targets:
          - localhost:9100
```

---

## 🚨 Step 4: Configure Alertmanager

Create:

```bash
sudo nano /opt/alertmanager/alertmanager.yml
```

Configuration:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by:
    - alertname
    - severity

  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h

  receiver: default-receiver

receivers:
  - name: default-receiver

    webhook_configs:
      - url: http://localhost:5001/webhook
        send_resolved: true

inhibit_rules:
  - source_match:
      severity: critical

    target_match:
      severity: warning

    equal:
      - alertname
      - instance
```

---

## 🐍 Step 5: Create Webhook Receiver

Create:

```bash
nano /tmp/webhook_receiver.py
```

Code:

```python
#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        try:
            alerts = json.loads(post_data.decode())

            print("\n" + "=" * 60)
            print(f"Alert received at {datetime.now()}")
            print("=" * 60)

            for alert in alerts.get('alerts', []):

                status = alert.get('status')
                labels = alert.get('labels', {})
                annotations = alert.get('annotations', {})

                print(f"Status: {status}")
                print(f"Alert: {labels.get('alertname')}")
                print(f"Severity: {labels.get('severity')}")
                print(f"Summary: {annotations.get('summary')}")
                print(f"Description: {annotations.get('description')}")
                print("-" * 60)

        except Exception as e:
            print(f"Error processing alert: {e}")

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':

    server = HTTPServer(
        ('localhost', 5001),
        WebhookHandler
    )

    print("Webhook receiver listening on port 5001...")

    server.serve_forever()
```

Make executable:

```bash
chmod +x /tmp/webhook_receiver.py
```

---

# 🧪 Task 2: Test Alerts

---

## ▶️ Step 1: Start Services

### Terminal 1

```bash
cd /opt/node_exporter

./node_exporter
```

### Terminal 2

```bash
cd /opt/prometheus

./prometheus --config.file=prometheus.yml
```

### Terminal 3

```bash
cd /opt/alertmanager

./alertmanager --config.file=alertmanager.yml
```

### Terminal 4

```bash
python3 /tmp/webhook_receiver.py
```

---

## 🔍 Step 2: Verify Services

### Prometheus

```bash
curl http://localhost:9090/-/healthy
```

### Alertmanager

```bash
curl http://localhost:9093/-/healthy
```

### Node Exporter

```bash
curl http://localhost:9100/metrics | head
```

---

## 📊 Step 3: View Rules

```bash
curl http://localhost:9090/api/v1/rules | python3 -m json.tool
```

Current Alerts:

```bash
curl http://localhost:9090/api/v1/alerts | python3 -m json.tool
```

---

## 🔥 Step 4: Trigger CPU Alert

Create:

```bash
nano /tmp/cpu_stress.sh
```

```bash
#!/bin/bash

echo "Starting CPU stress test..."

for i in {1..4}
do
  yes > /dev/null &
done

sleep 180

pkill yes

echo "CPU stress test completed"
```

Make executable:

```bash
chmod +x /tmp/cpu_stress.sh
```

Run:

```bash
./cpu_stress.sh
```

---

## 👀 Step 5: Monitor Alert Status

Watch alerts:

```bash
watch -n 5 \
'curl -s http://localhost:9090/api/v1/alerts | python3 -m json.tool'
```

Alertmanager:

```bash
curl http://localhost:9093/api/v2/alerts | python3 -m json.tool
```

Observe webhook receiver output.

---

## 🧹 Step 6: Cleanup Stress Test

```bash
pkill yes
```

Verify CPU:

```bash
top -bn1 | grep "Cpu(s)"
```

---

# ✅ Verification

---

## 🔎 Validate Configuration

```bash
cd /opt/prometheus

./promtool check config prometheus.yml
```

Expected:

```text
SUCCESS
```

---

## 🔎 Validate Rules

```bash
./promtool check rules rules/alerts.yml
```

Expected:

```text
SUCCESS
```

---

## 🌐 Verify UI

### Prometheus

```text
http://localhost:9090/alerts
```

### Alertmanager

```text
http://localhost:9093
```

---

## ✔️ Verify Alert Resolution

```bash
curl http://localhost:9090/api/v1/alerts \
| python3 -m json.tool \
| grep state
```

Expected lifecycle:

```text
pending
   ↓
firing
   ↓
resolved
```

---

# 🛠️ Troubleshooting Guide

---

## 🚨 Alerts Not Firing

### Check PromQL

```bash
Prometheus → Graph Tab
```

Verify expressions manually.

### Check Targets

```text
Status → Targets
```

Ensure targets are UP.

---

## 🚨 Alertmanager Not Receiving Alerts

Verify:

```bash
curl http://localhost:9093/-/healthy
```

Check Prometheus logs.

Verify:

```yaml
alerting:
```

section exists.

---

## 🚨 Webhook Not Receiving Alerts

Verify service:

```bash
python3 /tmp/webhook_receiver.py
```

Check:

```bash
netstat -tulpn | grep 5001
```

---

## 🚨 Common PromQL Mistakes

| Problem | Fix |
|-----------|------|
| Counter Metric | Use rate() |
| Wrong Labels | Use by(instance) |
| Typo | Check exact metric name |
| Missing Metrics | Verify exporter |

---

# 🎓 Key Takeaways

✅ Prometheus evaluates alert rules continuously

✅ Alertmanager handles routing and grouping

✅ The `for` clause prevents alert flapping

✅ Webhooks enable custom integrations

✅ Alert testing is essential before production deployment

---

# 🚀 Next Steps

### 📧 Add Email Notifications

### 💬 Integrate Slack Alerts

### ☎️ Configure PagerDuty

### 🔇 Create Silence Rules

### 📈 Build Advanced Multi-Condition Alerts

### 🎯 Integrate Incident Management Platforms

---

# 🧹 Optional Cleanup

```bash
sudo rm -rf /opt/prometheus

sudo rm -rf /opt/alertmanager

sudo rm -rf /opt/node_exporter
```

---

<div align="center">

# 🎉 Lab Completed Successfully

You have implemented a complete Prometheus alerting pipeline with Alertmanager integration, webhook notifications, alert validation, and troubleshooting workflows.

🚀 Happy Monitoring!

</div>
