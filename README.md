# AlertOps (Automated Incident Response System)

This project provides a complete monitoring solution using Prometheus, Grafana, and Windows Exporter. It includes a sample web application that exposes metrics for monitoring.

## Components

- **Web Application**: A Flask application that exposes metrics for monitoring
- **Prometheus**: Collects and stores metrics from the web application and Windows Exporter
- **Grafana**: Visualizes metrics from Prometheus
- **Alertmanager**: Handles alerts from Prometheus
- **Windows Exporter**: Exposes Windows system metrics to Prometheus

## Project Documentation and Media

### Videos
- [System Demo Video](demo/video.mkv) - Live demonstration of the monitoring system

### Screenshots
- [Dashboard Overview](demo/grafana%20dashboard.png) - Main monitoring dashboard
- [Alert Configuration](demo/prometheus%20alerts.png) - Alert setup in Prometheus
- [Alert Occurance](demo/alertmanager.png) - Alert occur in Alertmanager
- [Web Application Interface](demo/web%20app.png) - Sample web application 
- [windows log](demo/windows%20exporter.png) - windows log in windows exporter
- [SMS Alerts](demo/sms%20alert.png) - SMS alerts using Twilio

### Flowcharts
- [System Architecture](flowchart.png) - High-level system design

## Prerequisites

- Docker and Docker Compose
- Windows Exporter installed and running on port 9182

## Installation

### 1. Install Windows Exporter

1. Download the latest Windows Exporter from [GitHub](https://github.com/prometheus-community/windows_exporter/releases)
2. Run the installer as Administrator
3. Make sure it's configured to listen on port 9182
4. Verify the service is running by visiting http://localhost:9182/metrics

### 2. Build and Run the Monitoring Stack

#### Using PowerShell (Windows)

```powershell
.\build-and-run.ps1
```

#### Using Docker Compose Directly

```bash
# Build the images
docker-compose build

# Start the containers
docker-compose up -d
```

## Accessing the Services

- **Web Application**: http://localhost:8080
- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **Grafana**: http://localhost:3001 (username: admin, password: your_grafana_password_here)

## Grafana Setup

1. Log in to Grafana with username `admin` and password `your_grafana_password_here`
2. Add Prometheus as a data source:
   - Go to Configuration > Data Sources
   - Click "Add data source"
   - Select "Prometheus"
   - Set the URL to `http://prometheus:9090`
   - Click "Save & Test"
3. Import the dashboard:
   - Go to Dashboards > Import
   - Select the "System Monitoring Dashboard"

## Monitoring Metrics

### Web Application Metrics

- `http_requests_total`: Total number of HTTP requests
- `http_request_duration_seconds`: HTTP request latency
- `http_errors_total`: Total number of HTTP errors

### Windows System Metrics

- CPU Usage
- Memory Usage
- Disk Usage
- Network Traffic
- System Load

## Troubleshooting

### Windows Exporter Issues

If Prometheus cannot connect to the Windows Exporter:

1. Verify the Windows Exporter service is running:
   - Open Services (Win+R, type "services.msc")
   - Look for "windows_exporter" service
   - Make sure it's running
   - If not, right-click and select "Start"

2. Check Windows Firewall:
   - Open Windows Defender Firewall (Win+R, type "wf.msc")
   - Click "Inbound Rules" on the left
   - Click "New Rule..." on the right
   - Select "Port"
   - Select "TCP" and enter "9182"
   - Allow the connection
   - Apply to all profiles
   - Name it "Windows Exporter"

3. Test the metrics endpoint:
   - Open your web browser
   - Go to http://localhost:9182/metrics
   - You should see metrics data

### Docker Issues

If you encounter issues with Docker:

1. Make sure Docker is running
2. Try restarting Docker
3. Check Docker logs:
   ```
   docker-compose logs
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 