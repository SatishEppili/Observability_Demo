# Observability Demo Project

## Overview
This project demonstrates a **complete observability stack** for a sample Python web application. It integrates metrics, logging, and tracing to provide insights into the application’s behavior and performance.

The stack includes:  
- **Prometheus**: Scrapes and stores metrics from the Python application.  
- **Grafana**: Visualizes metrics, logs, and traces using dashboards.  
- **Loki**: Centralized log aggregation system.  
- **Promtail**: Ships logs from the application to Loki.  
- **Jaeger**: Distributed tracing for observing request flows in the application.  

This setup allows developers and DevOps engineers to **monitor, debug, and analyze** applications in a unified observability platform.

---

## Project Structure

observability-demo/
├─ app/
│ ├─ Dockerfile
│ ├─ app.py
│ └─ requirements.txt
├─ prometheus/
│ └─ prometheus.yml
├─ promtail/
│ └─ promtail-config.yml
├─ grafana/
│ └─ dashboards/
│ └─ observability-dashboard.json
└─ docker-compose.yml


- `app/` → Contains the sample Python web application with Prometheus metrics and Jaeger tracing integration.  
- `prometheus/` → Configuration for Prometheus to scrape metrics.  
- `promtail/` → Configuration for shipping logs to Loki.  
- `grafana/` → Pre-configured dashboards to visualize metrics, logs, and traces.  
- `docker-compose.yml` → Defines all services, volumes, and networking for the stack.

---

## Features
1. **Metrics Collection**  
   - The Python app exposes metrics at `/metrics`.  
   - Prometheus scrapes these metrics and stores them for visualization.  

2. **Logging**  
   - Application logs are collected by Promtail and shipped to Loki.  
   - Grafana visualizes logs in real-time.  

3. **Tracing**  
   - Requests through the Python app are traced using Jaeger.  
   - Distributed tracing allows debugging request flow and latency issues.

4. **Unified Dashboard**  
   - Grafana dashboards combine metrics, logs, and traces to provide a full observability view.  

---

## How to Run

1. Clone the repository:
```bash
git clone <repo-url>
cd observability-demo

2. Start all services:

docker compose up -d --build

Access services:

Application: http://localhost:5000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (default credentials: admin/admin)

Loki: http://localhost:3100

Jaeger: http://localhost:16686

Metrics Example

The Python app exposes Prometheus metrics such as:

http_requests_total → total HTTP requests per endpoint

request_latency_seconds → request latency histogram

python_gc_objects_collected_total → garbage collector statistics

Observability Benefits

Monitoring: Keep track of application performance and resource usage.
Debugging: Identify errors and bottlenecks using logs and traces.
Performance Analysis: Detect latency or high CPU/memory usage quickly.
Unified Observability: Metrics, logs, and traces in one view for easier decision-making.

Technologies Used

Python 3.11
Flask
Prometheus
Grafana
Loki & Promtail
Jaeger
Docker & Docker Compose

Future Enhancements

Add alerting using Prometheus Alertmanager.
Secure Grafana with proper credentials and HTTPS.
Integrate automated dashboards provisioning for multi-environment setups.
