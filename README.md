# 🍯 Docker-Based Honeypot Deployment

A comprehensive, production-ready honeypot deployment with integrated logging, metrics, and visualization using Docker Compose.

## 📋 Overview

This deployment includes:

### **Honeypots**
- **Cowrie** - SSH/Telnet honeypot (ports 2222, 2223)
- **Dionaea** - Multi-protocol honeypot (FTP, HTTP, SMTP, MySQL, PostgreSQL, SMB, MSSQL)
- **Custom Web Honeypot** - Simulates vulnerable web applications (port 8888)

### **Monitoring Stack**
- **Loki** - Log aggregation system
- **Promtail** - Log shipper
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards and visualization
- **Node Exporter** - System metrics
- **cAdvisor** - Container metrics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ATTACK SURFACE                           │
│  SSH:2222 | FTP:21 | HTTP:8080,8888 | SMTP:25 | etc.      │
└──────────────┬──────────────────────────────────────────────┘
               │
    ┌──────────┴──────────┬──────────────┐
    │                     │              │
┌───▼────┐        ┌──────▼─────┐   ┌───▼─────────┐
│ Cowrie │        │  Dionaea   │   │ Web Honeypot│
│  SSH   │        │Multi-Proto │   │    HTTP     │
└───┬────┘        └──────┬─────┘   └───┬─────────┘
    │                    │              │
    └────────────┬───────┴──────────────┘
                 │ Logs
         ┌───────▼────────┐
         │    Promtail    │
         │  (Log Shipper) │
         └───────┬────────┘
                 │
      ┌──────────┴──────────┬────────────────┐
      │                     │                │
  ┌───▼────┐         ┌─────▼──────┐   ┌────▼──────┐
  │  Loki  │         │ Prometheus │   │  Grafana  │
  │  Logs  │         │  Metrics   │   │Dashboards │
  └────────┘         └────────────┘   └───────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM
- 20GB disk space

### 1. Deploy the Stack

```bash
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

### 2. Access Grafana Dashboards

1. Open your browser to **http://localhost:3000**
2. Login credentials:
   - **Username:** `admin`
   - **Password:** `honeypot123`
3. Navigate to **Dashboards** → **Browse**
4. Open:
   - **Honeypot Attack Overview** - Real-time attack visualization
   - **Honeypot System Metrics** - Resource usage and performance

### 3. Verify Honeypots

Test each honeypot to ensure it's capturing attacks:

```bash
# Test SSH honeypot
ssh -p 2222 root@localhost
# Try password: password123

# Test FTP honeypot (Dionaea)
telnet localhost 21

# Test Web honeypot
curl http://localhost:8888
curl http://localhost:8888/admin
```

## 📊 Dashboards

### Honeypot Attack Overview
- **Attack activity over time** - Time-series graph of all attacks
- **Total attacks (last hour)** - Gauge showing recent activity
- **SSH/FTP/Web logs** - Real-time log streams
- **Top attacking IPs** - Pie chart of most active sources
- **Attacks by protocol** - Distribution of attack vectors

### Honeypot System Metrics
- **CPU/Memory/Disk usage** - System resource gauges
- **Running containers** - Container health status
- **Container resource usage** - Per-container CPU/memory
- **Network I/O** - Traffic rates for each honeypot

## 🔍 Checking Logs

### View Real-Time Logs

```bash
# All services
docker compose logs -f

# Specific honeypot
docker compose logs -f cowrie
docker compose logs -f dionaea
docker compose logs -f web-honeypot

# Monitoring stack
docker compose logs -f grafana
docker compose logs -f loki
docker compose logs -f prometheus
```

### Access Raw Log Files

```bash
# SSH honeypot logs
ls -lah logs/cowrie/
cat logs/cowrie/cowrie.json | jq .

# Multi-protocol honeypot logs
ls -lah logs/dionaea/
tail -f logs/dionaea/dionaea.log

# Web honeypot logs
ls -lah logs/web-honeypot/
cat logs/web-honeypot/honeypot.json | jq .
```

### Query Logs via Loki

```bash
# Query all SSH attacks
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="cowrie"}' | jq .

# Query specific IP
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="cowrie"} |= "192.168.1.1"' | jq .
```

## 📈 Prometheus Metrics

Access Prometheus UI at **http://localhost:9090**

Example queries:
```promql
# Container CPU usage
sum(rate(container_cpu_usage_seconds_total{name=~"honeypot.*"}[5m])) by (name)

# Container memory usage
sum(container_memory_usage_bytes{name=~"honeypot.*"}) by (name)

# Network traffic
sum(rate(container_network_receive_bytes_total{name=~"honeypot.*"}[5m])) by (name)
```

## 🔧 How Each Container Works

### Cowrie (SSH Honeypot)
- **Purpose:** Emulates an SSH/Telnet server to capture brute-force attacks and shell commands
- **Image:** `cowrie/cowrie:latest` (official)
- **Ports:** 2222 (SSH), 2223 (Telnet)
- **Logs:** JSON format in `logs/cowrie/cowrie.json`
- **Data:** Stores sessions, downloads, and file system state

### Dionaea (Multi-Protocol Honeypot)
- **Purpose:** Captures malware and exploits across multiple network protocols
- **Image:** `dinotools/dionaea:latest` (official)
- **Ports:** 21 (FTP), 8081 (HTTP), 8443 (HTTPS), 23 (Telnet), 3306 (MySQL), 5432 (PostgreSQL), 1433 (MSSQL), 445 (SMB)
- **Logs:** Text format in `logs/dionaea/`
- **Features:** Malware capture, exploit detection, binary downloads

### Web Honeypot
- **Purpose:** Custom Flask application simulating vulnerable web endpoints
- **Image:** Built from `web-honeypot/Dockerfile`
- **Port:** 8888
- **Logs:** JSON format in `logs/web-honeypot/honeypot.json`
- **Features:** 
  - Fake admin login portal
  - Common vulnerable paths (phpMyAdmin, wp-admin, .env, .git)
  - Full HTTP request logging

### Loki (Log Aggregation)
- **Purpose:** Collects and indexes logs from all honeypots
- **Image:** `grafana/loki:2.9.3`
- **Port:** 3100
- **Storage:** Filesystem-based in `data/loki/`
- **Features:** Label-based log queries, efficient compression

### Promtail (Log Shipper)
- **Purpose:** Scrapes log files and pushes to Loki
- **Image:** `grafana/promtail:2.9.3`
- **Sources:** 
  - File logs in `logs/` directory
  - Docker container logs
- **Features:** Label extraction, log parsing, timestamping

### Prometheus (Metrics Collection)
- **Purpose:** Scrapes and stores time-series metrics
- **Image:** `prom/prometheus:v2.48.0`
- **Port:** 9090
- **Storage:** TSDB in `data/prometheus/`
- **Targets:** Node Exporter, cAdvisor, honeypot containers

### Grafana (Visualization)
- **Purpose:** Dashboards for logs and metrics
- **Image:** `grafana/grafana:10.2.2`
- **Port:** 3000
- **Features:** 
  - Pre-configured datasources (Loki, Prometheus)
  - Pre-loaded dashboards
  - Automatic provisioning

## 🛑 Stopping and Cleaning Up

```bash
# Stop all containers
docker compose down

# Stop and remove volumes (deletes all data)
docker compose down -v

# View disk usage
docker system df

# Clean up everything
docker compose down -v --rmi all
```

## 🔐 Security Warnings

### ⚠️ CRITICAL SECURITY CONSIDERATIONS

1. **DO NOT expose honeypots directly to the internet without proper network segmentation**
   - Honeypots are designed to be attacked
   - Compromised honeypots could be used to attack other systems
   - Use a dedicated VLAN or DMZ

2. **Firewall Rules**
   ```bash
   # Example: Only allow specific networks
   sudo ufw allow from 10.0.0.0/8 to any port 2222
   sudo ufw allow from 10.0.0.0/8 to any port 21
   
   # Block honeypot containers from reaching internal networks
   sudo iptables -A FORWARD -s 172.25.0.0/16 -d 192.168.0.0/16 -j DROP
   ```

3. **Monitoring Access**
   - Change default Grafana password immediately
   - Use a reverse proxy with authentication for Grafana
   - Don't expose Prometheus/Loki ports publicly

4. **Network Isolation**
   ```yaml
   # Recommended: Add to docker-compose.yml
   networks:
     honeypot-net:
       driver: bridge
       internal: true  # Blocks internet access
   ```

5. **Regular Updates**
   ```bash
   # Pull latest images regularly
   docker compose pull
   docker compose up -d
   ```

6. **Log Retention**
   - Logs can grow large quickly
   - Implement log rotation
   - Monitor disk usage: `du -sh logs/`

7. **Legal Considerations**
   - Check local laws about honeypot deployment
   - Ensure you have authorization to run honeypots on your network
   - Document your security research purpose

8. **Resource Limits**
   - The deployment includes resource-intensive monitoring
   - Monitor system load: `docker stats`
   - Consider reducing scrape intervals if system is overloaded

### Recommended Network Setup

```
Internet → Firewall → DMZ (Honeypots) → Isolated Network
                     ↓
              Internal Network (Monitoring) → Grafana
```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker compose logs

# Check port conflicts
sudo netstat -tulpn | grep -E '2222|21|8888|3000|9090'

# Recreate containers
docker compose down
docker compose up -d --force-recreate
```

### No Logs Appearing in Grafana
```bash
# Check Promtail is running
docker compose logs promtail

# Verify Loki is receiving logs
curl http://localhost:3100/ready

# Check log file permissions
ls -la logs/
```

### High Resource Usage
```bash
# Monitor resource usage
docker stats

# Reduce scrape intervals in prometheus.yml
# Reduce log retention in loki-config.yml
```

### Dashboards Not Loading
```bash
# Check Grafana logs
docker compose logs grafana

# Verify datasources
curl -u admin:honeypot123 http://localhost:3000/api/datasources

# Re-import dashboards manually from dashboards/ directory
```

## 📁 Directory Structure

```
honeypot/
├── docker-compose.yml          # Main orchestration file
├── README.md                   # This file
├── config/                     # Configuration files
│   ├── cowrie/
│   │   └── cowrie.cfg         # Cowrie settings
│   ├── dionaea/
│   │   └── dionaea.cfg        # Dionaea settings
│   ├── loki/
│   │   └── loki-config.yml    # Loki configuration
│   ├── promtail/
│   │   └── promtail-config.yml # Log shipping config
│   ├── prometheus/
│   │   └── prometheus.yml     # Metrics scraping config
│   └── grafana/
│       ├── datasources/       # Auto-provisioned datasources
│       └── dashboards/        # Dashboard provisioning
├── dashboards/                 # Pre-built dashboard JSON
│   ├── honeypot-overview.json
│   └── honeypot-metrics.json
├── web-honeypot/              # Custom web honeypot
│   ├── Dockerfile
│   └── app.py
├── logs/                       # All honeypot logs (auto-created)
│   ├── cowrie/
│   ├── dionaea/
│   └── web-honeypot/
└── data/                       # Persistent data (auto-created)
    ├── cowrie/
    ├── loki/
    ├── prometheus/
    └── grafana/
```

## 🔄 Maintenance

### Daily Tasks
- Check Grafana dashboards for unusual activity
- Verify disk space: `df -h`
- Check log sizes: `du -sh logs/*`

### Weekly Tasks
- Review captured credentials and IPs
- Update honeypot configurations if needed
- Backup interesting attack data

### Monthly Tasks
- Pull latest Docker images: `docker compose pull`
- Archive old logs
- Review and adjust firewall rules
- Update passwords

## 📚 Additional Resources

- [Cowrie Documentation](https://github.com/cowrie/cowrie)
- [Dionaea Documentation](https://github.com/DinoTools/dionaea)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 📝 License

This deployment configuration is provided as-is for security research and educational purposes.

## 🤝 Contributing

Feel free to customize configurations and add additional honeypots or monitoring capabilities.

---

**⚠️ Remember: Always deploy honeypots responsibly and in accordance with local laws and organizational policies.**
