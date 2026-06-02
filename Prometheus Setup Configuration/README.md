# 📈 Prometheus Setup & Configuration 

<div align="center">

# 🚀 Prometheus Monitoring Setup & Configuration

### 🔍 Learn How to Deploy, Configure, and Monitor Infrastructure with Prometheus

![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Node Exporter](https://img.shields.io/badge/Node_Exporter-000000?style=for-the-badge&logo=prometheus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Monitoring](https://img.shields.io/badge/Observability-FF6F00?style=for-the-badge&logo=datadog&logoColor=white)

</div>

---

# 📖 Overview

This hands-on lab guides you through the complete installation and configuration of **Prometheus Monitoring System**. You will learn how to deploy Prometheus, configure scrape targets, monitor Linux system metrics using Node Exporter, and create a custom Python application exposing Prometheus metrics.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Install and configure Prometheus on Linux

✅ Configure Prometheus scrape jobs

✅ Understand Prometheus YAML configuration

✅ Monitor system metrics using Node Exporter

✅ Expose custom application metrics

✅ Validate Prometheus configuration

✅ Query collected metrics using PromQL

---

# 📋 Prerequisites

| Requirement | Status |
|------------|---------|
| Basic Linux Command Line Skills | ✅ |
| YAML Syntax Knowledge | ✅ |
| Understanding of System Services | ✅ |
| Networking Basics (HTTP, Ports) | ✅ |

---

# 🖥️ Environment Setup

> ⚠️ Al Nafi provides a bare-metal Linux cloud machine. Click **Start Lab** to provision your environment.

---

## 📦 System Requirements

| Component | Requirement |
|------------|------------|
| Operating System | Ubuntu 20.04+ / CentOS 7+ |
| Access | Sudo Privileges |
| Network | Internet Connectivity |
| Monitoring Server | Prometheus |

---

# 🏗️ Task 1: Install Prometheus

---

# 🔹 Step 1.1 — Download and Extract Prometheus

## 📥 Download Prometheus

```bash
cd /opt

sudo wget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
```

## 📦 Extract Archive

```bash
sudo tar xvfz prometheus-2.47.0.linux-amd64.tar.gz
```

## 📁 Rename Directory

```bash
sudo mv prometheus-2.47.0.linux-amd64 prometheus
```

---

# 🔹 Step 1.2 — Create Prometheus User & Directories

## 👤 Create Dedicated User

```bash
sudo useradd --no-create-home --shell /bin/false prometheus
```

## 📂 Create Directories

```bash
sudo mkdir -p /etc/prometheus

sudo mkdir -p /var/lib/prometheus
```

## 🔐 Assign Ownership

```bash
sudo chown prometheus:prometheus /var/lib/prometheus
```

---

# 🔹 Step 1.3 — Copy Binaries & Configure Permissions

## 📋 Copy Prometheus Binaries

```bash
sudo cp /opt/prometheus/prometheus /usr/local/bin/

sudo cp /opt/prometheus/promtool /usr/local/bin/
```

## 🔒 Set Ownership

```bash
sudo chown prometheus:prometheus /usr/local/bin/prometheus

sudo chown prometheus:prometheus /usr/local/bin/promtool
```

---

# 🔹 Step 1.4 — Create Prometheus Systemd Service

## ⚙️ Create Service File

```bash
sudo nano /etc/systemd/system/prometheus.service
```

### Add Configuration

```ini
[Unit]
Description=Prometheus Monitoring System
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple

ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.console.templates=/opt/prometheus/consoles \
  --web.console.libraries=/opt/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

---

## 📝 Understanding ExecStart Flags

| Flag | Purpose |
|--------|----------|
| --config.file | Prometheus configuration file |
| --storage.tsdb.path | Metrics database location |
| --web.console.templates | Console template location |
| --web.console.libraries | Console libraries location |

### 🎯 Lab Task

Research each flag and document your findings.

---

# 🏗️ Task 2: Configure Prometheus Targets

---

# 🔹 Step 2.1 — Create Base Configuration

## 📄 Create Configuration File

```bash
sudo nano /etc/prometheus/prometheus.yml
```

### Starter Configuration

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 15s

scrape_configs:

  - job_name: 'prometheus'

    static_configs:
      - targets:
          - 'localhost:9090'

        labels:
          environment: 'lab'
```

---

## 🎯 Lab Challenge

✔ Change scrape_interval from 15s → 10s

✔ Add label:

```yaml
environment: 'lab'
```

---

# 🔹 Step 2.2 — Install Node Exporter

## 📥 Download Node Exporter

```bash
cd /opt

sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
```

## 📦 Extract Archive

```bash
sudo tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
```

## 📋 Copy Binary

```bash
sudo cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
```

## 🔐 Set Ownership

```bash
sudo chown prometheus:prometheus /usr/local/bin/node_exporter
```

---

# 🔹 Step 2.3 — Create Node Exporter Service

## ⚙️ Create Service File

```bash
sudo nano /etc/systemd/system/node_exporter.service
```

### Add Configuration

```ini
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple

ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

---

# 🔹 Step 2.4 — Add Node Exporter Target

## Edit Configuration

```bash
sudo nano /etc/prometheus/prometheus.yml
```

### Add Scrape Job

```yaml
  - job_name: 'node_exporter'

    static_configs:
      - targets:
          - 'localhost:9100'

        labels:
          job_type: 'system_metrics'
          environment: 'lab'
```

---

# 🔹 Step 2.5 — Start Services

## Assign Permissions

```bash
sudo chown -R prometheus:prometheus /etc/prometheus
```

## Reload Systemd

```bash
sudo systemctl daemon-reload
```

## Start Node Exporter

```bash
sudo systemctl start node_exporter

sudo systemctl enable node_exporter
```

## Start Prometheus

```bash
sudo systemctl start prometheus

sudo systemctl enable prometheus
```

---

# 🏗️ Task 3: Create Custom Application Metrics

---

# 🔹 Step 3.1 — Install Python Dependencies

## Update Packages

```bash
sudo apt update
```

## Install Pip

```bash
sudo apt install -y python3-pip
```

## Install Prometheus Client

```bash
pip3 install prometheus_client
```

---

# 🔹 Step 3.2 — Create Sample Application

## Create File

```bash
nano ~/sample_app.py
```

### Complete Application

```python
from prometheus_client import start_http_server, Counter, Gauge
import time
import random

requests_counter = Counter(
    'app_requests_total',
    'Total app requests'
)

temperature_gauge = Gauge(
    'app_temperature',
    'Current temperature'
)

def process_request():
    requests_counter.inc()

def update_temperature():
    temperature_gauge.set(
        random.uniform(20, 30)
    )

if __name__ == '__main__':

    start_http_server(8000)

    print("Metrics server started on port 8000")

    while True:
        process_request()
        update_temperature()
        time.sleep(5)
```

---

# 🔹 Step 3.3 — Run Application

```bash
python3 ~/sample_app.py &
```

Expected Output:

```text
Metrics server started on port 8000
```

---

# 🔹 Step 3.4 — Add Application Target

Edit configuration:

```bash
sudo nano /etc/prometheus/prometheus.yml
```

Add:

```yaml
  - job_name: 'sample_app'

    static_configs:
      - targets:
          - 'localhost:8000'

        labels:
          application: 'sample_app'
          environment: 'lab'
```

---

# 🔹 Step 3.5 — Reload Configuration

```bash
sudo systemctl reload prometheus
```

---

# ✅ Verification

---

# 🔍 Step 4.1 — Verify Service Status

```bash
sudo systemctl status prometheus
```

```bash
sudo systemctl status node_exporter
```

### Expected Output

```text
active (running)
```

---

# 🔍 Step 4.2 — Access Prometheus UI

Open Browser:

```text
http://<your-server-ip>:9090
```

Navigate:

```text
Status → Targets
```

### Expected Targets

| Target | Status |
|----------|---------|
| localhost:9090 | UP ✅ |
| localhost:9100 | UP ✅ |
| localhost:8000 | UP ✅ |

---

# 🔍 Step 4.3 — Query Metrics

## Prometheus Self Monitoring

```promql
up{job="prometheus"}
```

---

## Node Exporter Metrics

```promql
node_cpu_seconds_total
```

---

## Custom Counter

```promql
app_requests_total
```

---

## Custom Gauge

```promql
app_temperature
```

---

## 🚀 Advanced Challenge

Calculate request rate over last 5 minutes:

```promql
rate(app_requests_total[5m])
```

---

# 🔍 Step 4.4 — Validate Configuration

```bash
promtool check config /etc/prometheus/prometheus.yml
```

### Expected Output

```text
SUCCESS:
is valid prometheus config file syntax
```

---

# 🛠️ Troubleshooting

---

## ❌ Prometheus Won't Start

### Check Logs

```bash
sudo journalctl -u prometheus -n 50
```

### Validate Configuration

```bash
promtool check config /etc/prometheus/prometheus.yml
```

### Check Permissions

```bash
ls -la /etc/prometheus/
```

---

## ❌ Target Shows DOWN

### Verify Service

```bash
sudo netstat -tlnp
```

### Check Specific Port

```bash
sudo netstat -tlnp | grep <port>
```

### Test Metrics Endpoint

```bash
curl http://localhost:<port>/metrics
```

---

## ❌ Metrics Not Appearing

✔ Wait for scrape interval

✔ Verify target health

✔ Confirm endpoint exports metrics

✔ Check metric names

---

# 🎯 Expected Outcomes

After completing this lab you should have:

✅ Prometheus running on Port 9090

✅ Node Exporter collecting system metrics

✅ Custom Python application exporting metrics

✅ Three active scrape targets

✅ Functional Prometheus Web UI

✅ Valid Prometheus configuration

✅ Ability to query metrics using PromQL

---

# 🧠 Key Concepts Mastered

| Concept | Skill Level |
|----------|------------|
| Prometheus Architecture | ⭐⭐⭐⭐⭐ |
| YAML Configuration | ⭐⭐⭐⭐⭐ |
| Scrape Jobs | ⭐⭐⭐⭐⭐ |
| Node Exporter | ⭐⭐⭐⭐⭐ |
| Custom Metrics | ⭐⭐⭐⭐⭐ |
| PromQL Basics | ⭐⭐⭐⭐⭐ |
| Service Management | ⭐⭐⭐⭐⭐ |

---

# 🎓 Lab Completion

## Congratulations! 🎉

You have successfully:

✅ Installed Prometheus

✅ Configured Prometheus as a systemd service

✅ Added multiple scrape targets

✅ Installed Node Exporter

✅ Created a custom metrics-enabled Python application

✅ Verified metrics collection

✅ Queried metrics using PromQL

---

# 🚀 Next Steps

🔹 Learn Advanced PromQL

🔹 Create Alerting Rules

🔹 Configure Alertmanager

🔹 Integrate Grafana Dashboards

🔹 Explore Service Discovery

🔹 Monitor Kubernetes Clusters

🔹 Build Production Monitoring Solutions

---

# 🌍 Real-World Applications

📊 Infrastructure Monitoring

📈 Performance Analysis

⚡ Capacity Planning

🚨 Incident Detection

🔍 System Observability

☁️ Cloud Monitoring

🏢 Enterprise Monitoring Platforms

---

<div align="center">

# 🚀 Happy Monitoring with Prometheus!

### 📈 Collect • Store • Query • Visualize

⭐ Prometheus is the foundation of modern cloud-native monitoring and observability.

</div>
