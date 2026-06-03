# 📚 Log Pipeline Building

<div align="center">

# 🔄 ELK Stack Log Pipeline Building 

![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge\&logo=elasticsearch\&logoColor=white)
![Logstash](https://img.shields.io/badge/Logstash-000000?style=for-the-badge\&logo=elastic\&logoColor=white)
![Filebeat](https://img.shields.io/badge/Filebeat-005571?style=for-the-badge\&logo=elastic\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu_20.04+-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)

### 📊 Collect • Process • Store • Search Logs Centrally

</div>

---

# 📖 Overview

In modern cloud-native environments, applications generate thousands of logs every minute.

Managing logs individually on each server becomes difficult as infrastructure grows.

This lab demonstrates how to build a centralized logging pipeline using:

* 📥 Filebeat (Log Collection)
* 🔄 Logstash (Log Processing)
* 📦 Elasticsearch (Log Storage & Search)

Together these components form the famous **ELK Stack + Beats** architecture.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Install and configure Filebeat

✅ Configure Logstash pipelines

✅ Deploy Elasticsearch

✅ Forward application logs

✅ Verify end-to-end log ingestion

✅ Search and retrieve centralized logs

---

# 📋 Prerequisites

| Requirement     | Description                     |
| --------------- | ------------------------------- |
| 🖥 Linux Skills | Basic command-line usage        |
| ⚙ Services      | Understanding of Linux services |
| 📄 Text Files   | File editing familiarity        |
| 🌐 Networking   | Basic localhost and ports       |
| 🔑 Privileges   | Root or sudo access             |

---

# 🏗️ Architecture

```text
 ┌──────────────────┐
 │ Application Logs │
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │     Filebeat     │
 │ Log Collection   │
 └────────┬─────────┘
          │ Port 5044
          ▼
 ┌──────────────────┐
 │    Logstash      │
 │ Parsing & Filter │
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │ Elasticsearch    │
 │ Storage & Search │
 └──────────────────┘
```

---

# 🖥 Environment Setup

## System Requirements

| Resource | Requirement               |
| -------- | ------------------------- |
| OS       | Ubuntu 20.04+ / CentOS 8+ |
| RAM      | Minimum 4GB               |
| Storage  | 20GB Free                 |
| Network  | Internet Connectivity     |

---

# 🚀 Task 1: Install and Configure ELK Stack

---

# ☕ Step 1.1: Install Java

Elasticsearch and Logstash require Java.

```bash
sudo apt update

sudo apt install -y openjdk-11-jdk

java -version
```

Expected:

```text
openjdk version "11.x"
```

---

# 📦 Step 1.2: Install Elasticsearch

## Import GPG Key

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```

---

## Add Repository

```bash
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" \
| sudo tee /etc/apt/sources.list.d/elastic-8.x.list
```

---

## Install Package

```bash
sudo apt update

sudo apt install -y elasticsearch
```

---

## Configure Elasticsearch

```bash
sudo tee /etc/elasticsearch/elasticsearch.yml > /dev/null <<EOF
cluster.name: log-pipeline-cluster
node.name: node-1

path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

network.host: localhost
http.port: 9200

discovery.type: single-node

xpack.security.enabled: false
EOF
```

---

## Start Service

```bash
sudo systemctl daemon-reload

sudo systemctl enable elasticsearch

sudo systemctl start elasticsearch
```

Wait:

```bash
sleep 30
```

---

## Verify Elasticsearch

```bash
curl -X GET "localhost:9200/"
```

Expected:

```json
{
  "cluster_name": "log-pipeline-cluster"
}
```

---

# 🔄 Step 1.3: Install Logstash

```bash
sudo apt install -y logstash
```

---

## Create Pipeline

```bash
sudo tee /etc/logstash/conf.d/pipeline.conf > /dev/null <<'EOF'

input {
  beats {
    port => 5044
  }
}

filter {

  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{LOGLEVEL:log_level} - %{GREEDYDATA:log_message}"
    }
  }

  date {
    match => [ "timestamp", "yyyy-MM-dd HH:mm:ss,SSS" ]
  }
}

output {

  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }

}
EOF
```

---

## Start Logstash

```bash
sudo systemctl enable logstash

sudo systemctl start logstash
```

Wait:

```bash
sleep 20
```

---

## Verify Logstash

```bash
sudo systemctl status logstash
```

```bash
sudo ss -tuln | grep 5044
```

Expected:

```text
LISTEN 0 128 *:5044
```

---

# 🚀 Task 2: Install and Configure Filebeat

---

# 📥 Step 2.1: Install Filebeat

```bash
sudo apt install -y filebeat
```

Backup original file:

```bash
sudo cp \
/etc/filebeat/filebeat.yml \
/etc/filebeat/filebeat.yml.bak
```

---

# ⚙️ Step 2.2: Configure Filebeat

```bash
sudo tee /etc/filebeat/filebeat.yml > /dev/null <<'EOF'

filebeat.inputs:

- type: log
  enabled: true

  paths:
    - /var/log/syslog
    - /var/log/auth.log
    - /home/*/app.log

  fields:
    log_type: system
    environment: lab

  multiline.pattern: '^[[:space:]]'
  multiline.negate: false
  multiline.match: after

output.logstash:
  hosts: ["localhost:5044"]

logging.level: info

logging.to_files: true

logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7

EOF
```

---

# ▶️ Step 2.3: Start Filebeat

```bash
sudo systemctl enable filebeat

sudo systemctl start filebeat
```

Verify:

```bash
sudo systemctl status filebeat
```

---

# 🧪 Task 3: Generate Test Logs

---

# 📂 Step 3.1: Create Application

```bash
mkdir -p ~/log-app

cd ~/log-app
```

---

## Create Python Log Generator

```python
#!/usr/bin/env python3

import logging
import random
import time

logging.basicConfig(
    filename='/home/ubuntu/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_logs():

    log_messages = [

        ("INFO", "User login successful"),

        ("INFO", "Database connection established"),

        ("WARNING", "High memory usage detected"),

        ("ERROR", "Failed to connect to external API"),

        ("INFO", "Transaction completed successfully")

    ]

    for _ in range(20):

        level, message = random.choice(log_messages)

        if level == "INFO":
            logging.info(message)

        elif level == "WARNING":
            logging.warning(message)

        elif level == "ERROR":
            logging.error(message)

        time.sleep(2)

if __name__ == "__main__":
    generate_logs()
```

Save as:

```bash
log_generator.py
```

Make executable:

```bash
chmod +x log_generator.py
```

---

# ▶️ Step 3.2: Run Log Generator

Install Python:

```bash
sudo apt install -y python3
```

Run:

```bash
python3 ~/log-app/log_generator.py &
```

Watch logs:

```bash
tail -f ~/app.log
```

---

# 🔍 Step 3.3: Verify Log Ingestion

## Filebeat Harvesting

```bash
sudo tail -f /var/log/filebeat/filebeat
```

Look for:

```text
Harvester started
```

---

## Wait for Processing

```bash
sleep 60
```

---

## View Indices

```bash
curl -X GET \
"localhost:9200/_cat/indices?v"
```

Expected:

```text
logs-YYYY.MM.DD
```

---

## Search Logs

```bash
curl -X GET \
"localhost:9200/logs-*/_search?pretty" \
-H 'Content-Type: application/json' \
-d'
{
  "query": {
    "match_all": {}
  },
  "size": 5,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}'
```

---

# 🔎 Step 3.4: Search Specific Patterns

## ERROR Logs

```bash
curl -X GET \
"localhost:9200/logs-*/_search?pretty" \
-H 'Content-Type: application/json' \
-d'
{
  "query": {
    "match": {
      "message": "ERROR"
    }
  }
}'
```

---

## Count Documents

```bash
curl -X GET \
"localhost:9200/logs-*/_count?pretty"
```

---

# ✅ Verification Checklist

---

## 1️⃣ Service Verification

```bash
sudo systemctl status elasticsearch

sudo systemctl status logstash

sudo systemctl status filebeat
```

All services should show:

```text
active (running)
```

---

## 2️⃣ Port Verification

```bash
sudo ss -tuln | grep -E '9200|5044'
```

Expected:

| Port | Service       |
| ---- | ------------- |
| 9200 | Elasticsearch |
| 5044 | Logstash      |

---

## 3️⃣ Pipeline Verification

Generate test log:

```bash
echo "$(date) - TEST - Pipeline verification log entry $(uuidgen)" \
| sudo tee -a /var/log/syslog
```

Wait:

```bash
sleep 10
```

Search:

```bash
curl -X GET \
"localhost:9200/logs-*/_search?pretty" \
-H 'Content-Type: application/json' \
-d'
{
  "query": {
    "match": {
      "message": "Pipeline verification"
    }
  }
}'
```

---

## 4️⃣ Document Count

```bash
curl -X GET \
"localhost:9200/logs-*/_count?pretty"
```

Expected:

```text
count > 0
```

---

# 🛠 Troubleshooting Guide

---

## ❌ Elasticsearch Won't Start

Check Java:

```bash
java -version
```

View logs:

```bash
sudo journalctl -u elasticsearch -n 50
```

Check memory:

```bash
free -h
```

---

## ❌ Filebeat Not Sending Logs

Validate configuration:

```bash
sudo filebeat test config
```

Test output:

```bash
sudo filebeat test output
```

Check logs:

```bash
sudo tail -f /var/log/filebeat/filebeat
```

---

## ❌ No Logs in Elasticsearch

Check Logstash:

```bash
sudo tail -f \
/var/log/logstash/logstash-plain.log
```

Check registry:

```bash
sudo cat \
/var/lib/filebeat/registry/filebeat/log.json
```

Verify permissions:

```bash
ls -la /var/log/syslog
```

---

## ⚡ Performance Optimization

Reduce workers:

```yaml
pipeline.workers: 2
```

Reduce scan frequency:

```yaml
scan_frequency: 30s
```

Restart services:

```bash
sudo systemctl restart filebeat

sudo systemctl restart logstash
```

---

# 🎯 Key Accomplishments

✅ Installed Elasticsearch

✅ Configured Logstash pipeline

✅ Installed Filebeat agent

✅ Generated application logs

✅ Verified end-to-end log flow

✅ Queried logs from Elasticsearch

---

# 🌍 Real-World Applications

### 📈 Application Monitoring

Track application behavior centrally.

### 🔍 Troubleshooting

Search logs from multiple servers instantly.

### 🛡 Security Monitoring

Detect suspicious events and incidents.

### 📊 Analytics

Perform trend analysis and operational reporting.

---

# 🚀 Next Steps

### 📊 Install Kibana Dashboards

### 🔍 Advanced Grok Parsing

### 🚨 Create Alerting Rules

### ☁️ Multi-Server Filebeat Deployment

### 📈 Build Enterprise Observability Platforms

---

# 🧹 Optional Cleanup

```bash
sudo systemctl stop elasticsearch
sudo systemctl stop logstash
sudo systemctl stop filebeat

sudo apt remove -y elasticsearch
sudo apt remove -y logstash
sudo apt remove -y filebeat
```

---

<div align="center">

# 🎉 Lab Completed Successfully

You have successfully built a centralized logging pipeline using:

📥 Filebeat

🔄 Logstash

📦 Elasticsearch

This architecture serves as the foundation for enterprise-grade observability, monitoring, troubleshooting, and security analytics platforms used in modern production environments.

🚀 Happy Logging!

</div>
