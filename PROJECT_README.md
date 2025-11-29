# Docker-Based Honeypot System - Final Project

## 📦 Complete Package Contents

This is the complete, production-ready Docker-based honeypot deployment system.

## 📋 Project Structure

```
final-project/
├── docker-compose.yml          # Main orchestration file
├── deploy.sh                   # Automated deployment script
├── README.md                   # Comprehensive documentation
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT_SUCCESS.md      # Post-deployment guide
├── .gitignore                 # Git ignore rules
│
├── config/                    # Configuration files
│   ├── cowrie/               # SSH honeypot config
│   ├── dionaea/              # Multi-protocol honeypot config
│   ├── loki/                 # Log aggregation config
│   ├── promtail/             # Log shipping config
│   ├── prometheus/           # Metrics collection config
│   └── grafana/              # Dashboard provisioning
│       ├── datasources/      # Auto-configured data sources
│       └── dashboards/       # Dashboard provisioning config
│
├── dashboards/               # Pre-built Grafana dashboards
│   ├── honeypot-overview.json    # Attack visualization dashboard
│   └── honeypot-metrics.json     # System metrics dashboard
│
├── scripts/                  # Utility scripts
│   ├── analyze-logs.sh       # Log analysis and statistics
│   ├── export-logs.sh        # Archive and export logs
│   ├── cleanup.sh            # Cleanup and reset script
│   └── test-honeypots.sh     # Testing and validation
│
├── ssh-honeypot/             # Custom SSH honeypot
│   ├── Dockerfile            # Container build file
│   ├── ssh_honeypot.py       # Python SSH honeypot
│   └── ssh_host_rsa_key      # SSH host key
│
└── web-honeypot/             # Custom web honeypot
    ├── Dockerfile            # Container build file
    └── app.py                # Flask web honeypot
```

## 🚀 Deployment

### Quick Deploy (3 Steps)

```bash
cd final-project
./deploy.sh
# Visit http://localhost:3000 (admin/honeypot123)
```

### Manual Deploy

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## 🍯 Deployed Honeypots

### 1. SSH Honeypot (Port 2222)
- Custom Python-based SSH honeypot
- Logs authentication attempts
- Captures command execution
- JSON structured logging

**Test:**
```bash
ssh -p 2222 admin@localhost
```

### 2. Dionaea Multi-Protocol (Multiple Ports)
- FTP (21), Telnet (23), HTTP (8081), HTTPS (8443)
- MySQL (3306), PostgreSQL (5432), MSSQL (1433)
- SMB (445), EPMAP (135)
- Captures malware binaries and exploits

**Test:**
```bash
telnet localhost 21
telnet localhost 3306
curl http://localhost:8081
```

### 3. Web Honeypot (Port 8888)
- Fake admin login portal
- Common vulnerable endpoints (/admin, /.env, /wp-admin, etc.)
- Full HTTP request logging
- User-agent and credential capture

**Test:**
```bash
curl http://localhost:8888
curl http://localhost:8888/admin
curl http://localhost:8888/.env
```

## 📊 Monitoring & Visualization

### Grafana Dashboards
- **URL:** http://localhost:3000
- **Login:** admin / honeypot123
- **Dashboards:**
  - Honeypot Attack Overview - Real-time attack visualization
  - Honeypot System Metrics - Resource usage and performance

### Prometheus Metrics
- **URL:** http://localhost:9090
- System and container metrics
- Custom honeypot metrics

### Loki Log Aggregation
- **URL:** http://localhost:3100
- Centralized log collection
- Label-based querying

## 🔧 Utility Scripts

### Analyze Logs
```bash
./scripts/analyze-logs.sh
```
Shows statistics on:
- Total attacks by honeypot
- Top attacking IPs
- Most used credentials
- Protocol distribution

### Export Logs
```bash
./scripts/export-logs.sh
```
Creates timestamped archive of all logs

### Test Honeypots
```bash
./scripts/test-honeypots.sh
```
Validates all services and generates test traffic

### Cleanup
```bash
./scripts/cleanup.sh
```
Safely removes containers, logs, and data

## 📝 Log Locations

All logs are stored in the `logs/` directory (auto-created):

```
logs/
├── ssh-honeypot/
│   └── ssh_honeypot.json     # SSH attack logs
├── dionaea/
│   └── dionaea*.log          # Multi-protocol logs
└── web-honeypot/
    ├── honeypot.json         # Web attack logs
    ├── access.log            # HTTP access logs
    └── error.log             # Error logs
```

## 🔐 Security Warnings

### ⚠️ CRITICAL - READ BEFORE DEPLOYING

1. **Network Isolation Required**
   - Deploy in isolated network/VLAN/DMZ
   - DO NOT expose directly to internet without proper segmentation

2. **Firewall Configuration**
   - Restrict access to monitoring ports (3000, 9090, 3100)
   - Limit honeypot access to controlled networks
   - Block honeypot containers from accessing internal networks

3. **Change Default Credentials**
   ```bash
   # Change Grafana password immediately
   docker exec -it honeypot-grafana grafana-cli admin reset-admin-password NewPassword123
   ```

4. **Legal & Authorization**
   - Ensure you have authorization to run honeypots
   - Check local laws regarding honeypot deployment
   - Document your security research purpose

5. **Monitoring & Maintenance**
   - Check logs regularly
   - Monitor disk usage
   - Update Docker images periodically

## 📚 Documentation Files

- **README.md** - Complete technical documentation
- **QUICKSTART.md** - Fast setup reference
- **DEPLOYMENT_SUCCESS.md** - Post-deployment guide

## 🛠️ System Requirements

- **Docker:** 20.10+
- **Docker Compose:** 2.0+
- **RAM:** 4GB minimum
- **Disk:** 20GB recommended
- **OS:** Linux (tested on Debian/Ubuntu/Kali)

## 📈 What Gets Logged

### SSH Honeypot
```json
{
  "timestamp": "2025-11-29T12:00:00",
  "event_type": "login_attempt",
  "src_ip": "192.168.1.100",
  "username": "admin",
  "password": "password123",
  "auth_method": "password"
}
```

### Web Honeypot
```json
{
  "timestamp": "2025-11-29T12:00:00",
  "remote_addr": "192.168.1.100",
  "method": "POST",
  "path": "/login",
  "user_agent": "Mozilla/5.0...",
  "form_data": {"username": "admin", "password": "admin"}
}
```

### Dionaea
- Connection logs per protocol
- Malware binary captures
- Exploit attempts

## 🔄 Common Operations

### View Live Logs
```bash
docker compose logs -f ssh-honeypot
docker compose logs -f dionaea
docker compose logs -f web-honeypot
```

### Restart Services
```bash
docker compose restart
docker compose restart ssh-honeypot  # Single service
```

### Stop Everything
```bash
docker compose down
```

### Update Images
```bash
docker compose pull
docker compose up -d
```

### Check Resource Usage
```bash
docker stats
```

## 🐛 Troubleshooting

### Services Not Starting
```bash
# Check logs
docker compose logs

# Verify ports aren't in use
sudo netstat -tulpn | grep -E '2222|3000|8888'

# Recreate containers
docker compose down
docker compose up -d --force-recreate
```

### No Data in Grafana
- Wait 2-3 minutes for services to initialize
- Generate test traffic: `./scripts/test-honeypots.sh`
- Check Promtail: `docker compose logs promtail`
- Verify Loki: `curl http://localhost:3100/ready`

### Permission Errors
```bash
# Fix data directory permissions
sudo chown -R 10001:10001 data/loki
sudo chown -R 472:472 data/grafana
sudo chown -R 65534:65534 data/prometheus
docker compose restart
```

## 📞 Support & Resources

- **Cowrie SSH Honeypot:** https://github.com/cowrie/cowrie
- **Dionaea:** https://github.com/DinoTools/dionaea
- **Grafana:** https://grafana.com/docs/
- **Prometheus:** https://prometheus.io/docs/
- **Loki:** https://grafana.com/docs/loki/

## 📄 License

This deployment configuration is provided as-is for security research and educational purposes.

## ✅ Pre-Flight Checklist

Before deploying:
- [ ] Docker and Docker Compose installed
- [ ] At least 4GB RAM available
- [ ] 20GB disk space free
- [ ] Network isolation configured
- [ ] Firewall rules in place
- [ ] Authorization obtained
- [ ] Monitoring plan established

## 🎯 Success Criteria

After deployment, you should have:
- ✅ All 9 containers running
- ✅ Grafana accessible at localhost:3000
- ✅ SSH honeypot responding on port 2222
- ✅ Web honeypot responding on port 8888
- ✅ Dionaea listening on multiple ports
- ✅ Logs being collected in Loki
- ✅ Dashboards showing data in Grafana

---

**Ready to Deploy? Run `./deploy.sh` to get started!**

For questions or issues, review the troubleshooting section or check individual container logs.

**Happy Hunting! 🎯🍯**
