# 📊 Custom Dashboard Creation with Grafana

<div align="center">

# 🚀 Grafana Monitoring Dashboard 

### 🛠️ Build Professional Monitoring Dashboards with Grafana, Prometheus & Node Exporter

![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Node Exporter](https://img.shields.io/badge/Node_Exporter-000000?style=for-the-badge&logo=prometheus&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Monitoring](https://img.shields.io/badge/Monitoring-0052CC?style=for-the-badge&logo=datadog&logoColor=white)

</div>

---

# 📖 Overview

This hands-on lab guides you through installing and configuring **Grafana**, **Prometheus**, and **Node Exporter** to create a powerful real-time monitoring dashboard for Linux systems.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Install and configure Grafana on Linux

✅ Configure Prometheus as a Grafana data source

✅ Create custom monitoring dashboards

✅ Visualize CPU, Memory, Disk, and Network metrics

✅ Build PromQL queries

✅ Export and share dashboards

---

# 📋 Prerequisites

| Requirement | Status |
|------------|---------|
| Basic Linux Command Line Knowledge | ✅ |
| Understanding of CPU, Memory & Disk Metrics | ✅ |
| Basic Networking Concepts | ✅ |
| Web Browser Familiarity | ✅ |
| Monitoring Fundamentals (Lab 1) | ✅ |

---

# 🖥️ Environment Requirements

| Component | Requirement |
|------------|------------|
| OS | Ubuntu 20.04+ |
| RAM | Minimum 2 GB |
| Internet | Required |
| User Access | Sudo Privileges |

---

# ⚙️ Initial System Setup

## 🔄 Update Package Repository

```bash
sudo apt update
```

## 📦 Install Required Dependencies

```bash
sudo apt install -y wget curl software-properties-common
```

---

# 🏗️ Task 1: Install and Configure Grafana

---

# 🔹 Step 1.1 — Install Grafana

## 🔑 Add Grafana GPG Key

```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

## 📁 Add Grafana Repository

```bash
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

## 📥 Install Grafana

```bash
sudo apt update
sudo apt install -y grafana
```

---

# 🔹 Step 1.2 — Start Grafana Service

## 🚀 Enable Service

```bash
sudo systemctl enable grafana-server
```

## ▶️ Start Service

```bash
sudo systemctl start grafana-server
```

## 🔍 Verify Status

```bash
sudo systemctl status grafana-server
```

### ✅ Expected Result

```text
active (running)
```

---

# 🔹 Step 1.3 — Access Grafana Dashboard

🌐 Open Browser:

```text
http://localhost:3000
```

### 🔑 Default Credentials

```text
Username: admin
Password: admin
```

⚠️ Change password when prompted.

---

# 🔹 Step 1.4 — Install Prometheus

## 👤 Create Prometheus User

```bash
sudo useradd --no-create-home --shell /bin/false prometheus
```

## 📂 Create Directories

```bash
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
```

## ⬇️ Download Prometheus

```bash
cd /tmp

wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
```

## 📦 Extract Archive

```bash
tar -xvf prometheus-2.45.0.linux-amd64.tar.gz

cd prometheus-2.45.0.linux-amd64
```

## 📋 Copy Binaries

```bash
sudo cp prometheus /usr/local/bin/
sudo cp promtool /usr/local/bin/
```

## 📁 Copy Configuration Files

```bash
sudo cp -r consoles /etc/prometheus
sudo cp -r console_libraries /etc/prometheus
sudo cp prometheus.yml /etc/prometheus/
```

---

# 🔹 Step 1.5 — Configure Prometheus

Open configuration:

```bash
sudo nano /etc/prometheus/prometheus.yml
```

Paste:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:

  - job_name: 'prometheus'
    static_configs:
      - targets:
          - 'localhost:9090'

  - job_name: 'node_exporter'
    static_configs:
      - targets:
          - 'localhost:9100'
```

💡 This configuration scrapes metrics every 15 seconds.

---

# 🔹 Step 1.6 — Install Node Exporter

## ⬇️ Download Node Exporter

```bash
cd /tmp

wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
```

## 📦 Extract and Install

```bash
tar -xvf node_exporter-1.6.1.linux-amd64.tar.gz

sudo cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
```

---

# 🔹 Step 1.7 — Create Systemd Services

## ⚙️ Node Exporter Service

```bash
sudo nano /etc/systemd/system/node_exporter.service
```

```ini
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

---

## ⚙️ Prometheus Service

```bash
sudo nano /etc/systemd/system/prometheus.service
```

```ini
[Unit]
Description=Prometheus
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple

ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/

[Install]
WantedBy=multi-user.target
```

---

# 🔹 Step 1.8 — Set Permissions & Start Services

## 🔐 Assign Ownership

```bash
sudo chown -R prometheus:prometheus /etc/prometheus

sudo chown -R prometheus:prometheus /var/lib/prometheus
```

## 🔄 Reload Systemd

```bash
sudo systemctl daemon-reload
```

## 🚀 Start Services

```bash
sudo systemctl start node_exporter

sudo systemctl start prometheus
```

## 🔁 Enable Services

```bash
sudo systemctl enable node_exporter

sudo systemctl enable prometheus
```

## 🔍 Verify

```bash
sudo systemctl status node_exporter

sudo systemctl status prometheus
```

---

### ✅ Verification

Open:

```text
http://localhost:9090
```

Navigate:

```text
Status → Targets
```

Ensure all targets show:

```text
UP
```

---

# 📊 Task 2: Configure Grafana Data Source

---

# 🔹 Step 2.1 — Add Prometheus Data Source

### Navigation

```text
Configuration
 └── Data Sources
      └── Add Data Source
```

### Select

```text
Prometheus
```

### Configure

```text
Name: Prometheus

URL: http://localhost:9090
```

Click:

```text
Save & Test
```

### ✅ Expected Result

```text
Data source is working
```

---

# 📈 Step 2.2 — Create Dashboard

```text
+ → Dashboard → Add New Panel
```

---

# 🔥 Step 2.3 — CPU Usage Panel

## PromQL Query

```promql
100 - (
avg by(instance)
(
rate(node_cpu_seconds_total{mode="idle"}[5m])
) * 100
)
```

## Panel Settings

```text
Title: CPU Usage (%)

Visualization:
  • Gauge
  • Time Series

Unit:
  Percent (0-100)
```

---

# 🧠 Step 2.4 — Memory Usage Panel

## PromQL Query

```promql
(
1 -
(
node_memory_MemAvailable_bytes
/
node_memory_MemTotal_bytes
)
) * 100
```

## Configuration

```text
Title: Memory Usage (%)

Visualization:
  Gauge

Thresholds:
  Green  : 0-70
  Yellow : 70-85
  Red    : 85-100
```

---

# 💾 Step 2.5 — Disk Usage Panel

## PromQL Query

```promql
100 -
(
(
node_filesystem_avail_bytes{mountpoint="/"}
/
node_filesystem_size_bytes{mountpoint="/"}
) * 100
)
```

## Configuration

```text
Title: Disk Usage - Root (%)

Visualization:
  Gauge / Stat
```

---

# 🌐 Step 2.6 — Network Traffic Panel

## Query A — Receive Rate

```promql
rate(node_network_receive_bytes_total{device!="lo"}[5m])
```

## Query B — Transmit Rate

```promql
rate(node_network_transmit_bytes_total{device!="lo"}[5m])
```

## Configuration

```text
Title: Network Traffic

Visualization:
  Time Series

Unit:
  bytes/sec
```

---

# 🎨 Step 2.7 — Organize Dashboard Layout

Recommended Layout:

```text
+-------------------+-------------------+
|      CPU          |      Memory       |
+-------------------+-------------------+

+---------------------------------------+
|            Disk Usage                 |
+---------------------------------------+

+---------------------------------------+
|          Network Traffic              |
+---------------------------------------+
```

### 💾 Save Dashboard

```text
Name:
System Monitoring Dashboard
```

---

# ⚙️ Step 2.8 — Dashboard Settings

## General

```text
Tags:
  system
  monitoring

Timezone:
  Local Timezone
```

## Time Options

```text
Default Range:
  Last 15 Minutes

Auto Refresh:
  Every 10 Seconds
```

---

# 🔄 Step 2.9 — Create Dashboard Variable

Navigate:

```text
Dashboard Settings
 └── Variables
      └── Add Variable
```

## Configuration

```text
Name:
instance

Type:
Query

Datasource:
Prometheus

Query:
label_values(node_cpu_seconds_total, instance)

Multi Value:
Enabled

Include All:
Enabled
```

### Update CPU Query

```promql
node_cpu_seconds_total{
instance=~"$instance"
}
```

---

# 📤 Step 2.10 — Export Dashboard

```text
Share
 └── Export
      └── Save to File
```

Save As:

```text
system-dashboard.json
```

---

# ✅ Verification Tasks

---

## 🔍 Verify Grafana

```bash
sudo systemctl status grafana-server | grep "active (running)"
```

```bash
sudo netstat -tlnp | grep 3000
```

---

## 🔍 Verify Prometheus

```bash
curl http://localhost:9090/-/healthy
```

---

## 🔍 Verify Node Exporter

```bash
curl http://localhost:9100/metrics | head -n 5
```

---

## 🔍 Verify Dashboard Data

✔ CPU metrics visible

✔ Memory metrics visible

✔ Disk metrics visible

✔ Network graph updating

✔ No "No Data" errors

---

# 🧪 Generate Test Load

## CPU Stress Test

```bash
yes > /dev/null &
```

Check dashboard for increased CPU usage.

Stop process:

```bash
kill <PID>
```

---

# 🛠️ Troubleshooting

## Grafana Won't Start

```bash
sudo journalctl -u grafana-server -n 50
```

```bash
sudo lsof -i :3000
```

---

## No Data in Panels

```bash
curl http://localhost:9090/api/v1/targets | jq
```

```bash
curl http://localhost:9100/metrics | grep node_cpu
```

---

## Query Errors

✅ Validate in Prometheus UI

```text
http://localhost:9090/graph
```

✅ Verify metric names

✅ Confirm time range

---

## Dashboard Not Saving

✔ Check browser console (F12)

✔ Verify Grafana permissions

✔ Re-login to Grafana

---

# 🎓 Lab Completion

## Congratulations! 🎉

You have successfully:

✅ Installed Grafana

✅ Configured Prometheus

✅ Installed Node Exporter

✅ Built Custom Monitoring Dashboards

✅ Created PromQL Queries

✅ Implemented Dashboard Variables

✅ Exported Dashboard Configurations

---

# 🚀 Skills Acquired

| Skill | Level |
|---------|---------|
| Grafana Administration | ⭐⭐⭐⭐⭐ |
| Prometheus Monitoring | ⭐⭐⭐⭐⭐ |
| Node Exporter Metrics | ⭐⭐⭐⭐⭐ |
| Dashboard Design | ⭐⭐⭐⭐⭐ |
| PromQL Fundamentals | ⭐⭐⭐⭐⭐ |
| Visualization Techniques | ⭐⭐⭐⭐⭐ |

---

# 🌍 Real-World Applications

🔹 DevOps Monitoring

🔹 Infrastructure Observability

🔹 Capacity Planning

🔹 Incident Response

🔹 Performance Optimization

🔹 SLA Reporting

🔹 Production Monitoring

---

# 🎯 Next Steps

✅ Explore Grafana Plugins

✅ Configure Alerting Rules

✅ Monitor Kubernetes Clusters

✅ Integrate MySQL Metrics

✅ Integrate InfluxDB

✅ Create Application Dashboards

✅ Build Enterprise Monitoring Solutions

---

<div align="center">

# 🚀 Happy Monitoring with Grafana!

### 📊 Observe • Analyze • Optimize • Scale

⭐ Build dashboards that provide real-time visibility into your infrastructure.

</div>
