# 📂 Final Project - Quick Navigation

## 🎯 START HERE

**New to this project?** Read in this order:
1. [`PROJECT_README.md`](PROJECT_README.md) - Start here for overview
2. [`QUICKSTART.md`](QUICKSTART.md) - Fast deployment guide
3. [`DEPLOYMENT_SUCCESS.md`](DEPLOYMENT_SUCCESS.md) - After deployment

## 🚀 Quick Deploy

```bash
./deploy.sh
```

Then visit: http://localhost:3000 (admin/honeypot123)

## 📋 File Index

### 📖 Documentation
- **[PROJECT_README.md](PROJECT_README.md)** - Main project documentation (START HERE)
- **[README.md](README.md)** - Complete technical guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference
- **[DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md)** - Post-deployment guide
- **[MANIFEST.txt](MANIFEST.txt)** - Package contents list

### ⚙️ Core Files
- **[docker-compose.yml](docker-compose.yml)** - Main orchestration
- **[deploy.sh](deploy.sh)** - Automated deployment
- **[.gitignore](.gitignore)** - Git ignore rules

### 🍯 Honeypots
- **[ssh-honeypot/](ssh-honeypot/)** - Custom SSH honeypot
  - `Dockerfile` - Container build
  - `ssh_honeypot.py` - Python implementation
  - `ssh_host_rsa_key` - SSH host key
  
- **[web-honeypot/](web-honeypot/)** - Custom web honeypot
  - `Dockerfile` - Container build
  - `app.py` - Flask application

### 🔧 Configuration
- **[config/](config/)** - All configuration files
  - `dionaea/` - Multi-protocol honeypot
  - `loki/` - Log aggregation
  - `promtail/` - Log shipping
  - `prometheus/` - Metrics collection
  - `grafana/` - Dashboard provisioning

### 📊 Dashboards
- **[dashboards/](dashboards/)** - Grafana dashboards
  - `honeypot-overview.json` - Attack visualization
  - `honeypot-metrics.json` - System metrics

### 🔨 Utilities
- **[scripts/](scripts/)** - Helper scripts
  - `analyze-logs.sh` - Log analysis
  - `export-logs.sh` - Log archiving
  - `cleanup.sh` - System cleanup
  - `test-honeypots.sh` - Testing suite

## 🎓 Common Tasks

### Deploy
```bash
./deploy.sh
```

### View Logs
```bash
docker compose logs -f
```

### Analyze Attacks
```bash
./scripts/analyze-logs.sh
```

### Test Honeypots
```bash
./scripts/test-honeypots.sh
```

### Stop Everything
```bash
docker compose down
```

### Cleanup
```bash
./scripts/cleanup.sh
```

## 🍯 Honeypot Ports

| Service | Port | Test Command |
|---------|------|--------------|
| SSH | 2222 | `ssh -p 2222 admin@localhost` |
| FTP | 21 | `telnet localhost 21` |
| Telnet | 23 | `telnet localhost 23` |
| HTTP | 8081 | `curl http://localhost:8081` |
| HTTPS | 8443 | `curl -k https://localhost:8443` |
| MySQL | 3306 | `telnet localhost 3306` |
| PostgreSQL | 5432 | `telnet localhost 5432` |
| Web | 8888 | `curl http://localhost:8888` |

## 📊 Monitoring URLs

- **Grafana:** http://localhost:3000 (admin/honeypot123)
- **Prometheus:** http://localhost:9090
- **Loki:** http://localhost:3100

## 🔐 Security Checklist

Before deploying:
- [ ] Network isolation configured
- [ ] Firewall rules in place
- [ ] Authorization obtained
- [ ] Default password will be changed
- [ ] Monitoring plan established

## 📞 Troubleshooting

**Services not starting?**
```bash
docker compose logs
```

**No data in Grafana?**
- Wait 2-3 minutes
- Run: `./scripts/test-honeypots.sh`

**Permission errors?**
```bash
sudo chown -R 10001:10001 data/loki
sudo chown -R 472:472 data/grafana
docker compose restart
```

## 📦 What's Included

- ✅ 3 honeypots (SSH, Web, Multi-protocol)
- ✅ 6 monitoring services (Grafana, Prometheus, Loki, etc.)
- ✅ 2 pre-built dashboards
- ✅ 4 utility scripts
- ✅ 5 documentation files
- ✅ Complete configuration
- ✅ Automated deployment

## 🎯 Success Criteria

After deployment:
- ✅ All containers running
- ✅ Grafana accessible
- ✅ Honeypots responding
- ✅ Logs being collected
- ✅ Dashboards showing data

---

**Ready? Start with [PROJECT_README.md](PROJECT_README.md) or run `./deploy.sh`**
