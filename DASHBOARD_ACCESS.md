# 🔗 Dashboard Access & Credentials

## 📊 Main Dashboards

### **Grafana** (Primary Dashboard)
- **URL:** http://localhost:3000
- **Username:** `admin`
- **Password:** `honeypot123`
- **Description:** Main visualization platform with pre-built honeypot dashboards

#### Available Dashboards in Grafana:
1. **Honeypot Attack Overview**
   - Real-time attack activity graphs
   - SSH, Dionaea, and Web honeypot logs
   - Top attacking IPs (pie chart)
   - Attacks by protocol distribution
   
2. **Honeypot System Metrics**
   - CPU/Memory/Disk usage gauges
   - Container resource utilization
   - Network I/O statistics
   - Running container count

---

## 📈 Monitoring Services

### **Prometheus** (Metrics Database)
- **URL:** http://localhost:9090
- **Authentication:** None (internal use)
- **Description:** Time-series metrics collection and querying
- **Use:** Advanced metric queries and alerting rules

### **Loki** (Log Aggregation)
- **URL:** http://localhost:3100
- **Authentication:** None (internal use)
- **Description:** Log aggregation system (queried through Grafana)
- **API Endpoint:** http://localhost:3100/loki/api/v1/query_range

---

## 🍯 Honeypot Endpoints

### **SSH Honeypot**
- **Port:** 2222
- **Protocol:** SSH
- **Test:** `ssh -p 2222 admin@localhost`
- **Logs:** `logs/ssh-honeypot/ssh_honeypot.json`

### **Web Honeypot**
- **URL:** http://localhost:8888
- **Protocol:** HTTP
- **Test:** `curl http://localhost:8888`
- **Interesting Paths:**
  - http://localhost:8888/admin
  - http://localhost:8888/.env
  - http://localhost:8888/wp-admin/
  - http://localhost:8888/phpMyAdmin/
- **Logs:** `logs/web-honeypot/honeypot.json`

### **Dionaea Multi-Protocol Honeypot**
- **Ports:**
  - 21 (FTP)
  - 23 (Telnet)
  - 135 (EPMAP)
  - 445 (SMB)
  - 1433 (MSSQL)
  - 3306 (MySQL)
  - 5432 (PostgreSQL)
  - 8081 (HTTP)
  - 8443 (HTTPS)
- **Logs:** `logs/dionaea/`

---

## 🔐 Default Credentials Summary

| Service | URL | Username | Password | Notes |
|---------|-----|----------|----------|-------|
| **Grafana** | http://localhost:3000 | admin | honeypot123 | ⚠️ CHANGE THIS! |
| Prometheus | http://localhost:9090 | - | - | No auth |
| Loki | http://localhost:3100 | - | - | No auth |

---

## 🚨 Security Warnings

### ⚠️ CHANGE DEFAULT PASSWORD
```bash
# Login to Grafana and change password:
# 1. Go to http://localhost:3000
# 2. Login with admin/honeypot123
# 3. Click profile icon → Change Password
```

### ⚠️ DO NOT EXPOSE PUBLICLY
- These services are meant for **internal use only**
- Use firewall rules to restrict access
- Consider using a reverse proxy with authentication for external access

### ⚠️ Network Isolation
```bash
# Recommended: Block Grafana/Prometheus from internet
sudo ufw deny from any to any port 3000
sudo ufw deny from any to any port 9090
sudo ufw deny from any to any port 3100

# Only allow honeypot ports (with caution)
sudo ufw allow 2222/tcp comment "SSH Honeypot"
sudo ufw allow 8888/tcp comment "Web Honeypot"
```

---

## 📱 Quick Access Commands

```bash
# Open Grafana in browser (Linux)
xdg-open http://localhost:3000

# Check all services are running
docker compose ps

# View Grafana logs
docker compose logs -f grafana

# Restart Grafana if needed
docker compose restart grafana

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq .

# Query Loki for SSH attacks
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="ssh-honeypot"}' | jq .
```

---

## 🎯 First Time Setup

1. **Access Grafana:** http://localhost:3000
2. **Login:** admin / honeypot123
3. **Navigate:** Dashboards → Browse
4. **Open:** "Honeypot Attack Overview"
5. **Generate test data:** `./scripts/test-honeypots.sh`
6. **Watch live attacks!** 🎉

---

## 📊 API Endpoints

### Grafana API
```bash
# List all dashboards
curl -u admin:honeypot123 http://localhost:3000/api/search

# Get dashboard by UID
curl -u admin:honeypot123 http://localhost:3000/api/dashboards/uid/honeypot-overview
```

### Prometheus API
```bash
# Query current metrics
curl 'http://localhost:9090/api/v1/query?query=up'

# Query time range
curl 'http://localhost:9090/api/v1/query_range?query=up&start=2023-01-01T00:00:00Z&end=2023-01-01T01:00:00Z&step=15s'
```

### Loki API
```bash
# Query logs
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="ssh-honeypot"}' \
  --data-urlencode 'limit=100'

# Get labels
curl -s "http://localhost:3100/loki/api/v1/labels"
```

---

## 🔧 Troubleshooting Access Issues

### Can't access Grafana?
```bash
# Check if running
docker compose ps grafana

# Check logs
docker compose logs grafana

# Restart
docker compose restart grafana

# Check port binding
netstat -tulpn | grep 3000
```

### Dashboards not showing data?
```bash
# Wait 1-2 minutes after startup
# Check Promtail is collecting logs
docker compose logs promtail

# Generate test traffic
./scripts/test-honeypots.sh

# Verify Loki is receiving data
curl http://localhost:3100/ready
```

### Password not working?
```bash
# Reset Grafana admin password
docker compose exec grafana grafana-cli admin reset-admin-password newpassword123

# Or recreate container
docker compose down
sudo rm -rf data/grafana/*
docker compose up -d
```

---

**Remember:** Always change default credentials in production environments!
