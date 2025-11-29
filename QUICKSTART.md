# Quick Start Guide

## Deploy in 3 Commands

```bash
# 1. Navigate to the honeypot directory
cd /home/kali/Desktop/honeypot

# 2. Run the deployment script
./deploy.sh

# 3. Open Grafana
# Visit http://localhost:3000
# Login: admin / honeypot123
```

## What Gets Deployed

- **3 Honeypots**: SSH, FTP/Multi-Protocol, Web
- **Logging**: Loki + Promtail for centralized logs
- **Metrics**: Prometheus for system monitoring
- **Dashboards**: Grafana with pre-built visualizations

## Useful Commands

```bash
# View all logs
docker compose logs -f

# Check status
docker compose ps

# Analyze captured attacks
./scripts/analyze-logs.sh

# Test honeypots
./scripts/test-honeypots.sh

# Export logs
./scripts/export-logs.sh

# Stop everything
docker compose down

# Full cleanup
./scripts/cleanup.sh
```

## Exposed Ports

| Service | Port | Protocol |
|---------|------|----------|
| SSH Honeypot | 2222 | SSH |
| Telnet Honeypot | 2223 | Telnet |
| FTP Honeypot | 21 | FTP |
| HTTP Honeypot | 8080, 8888 | HTTP |
| SMTP Honeypot | 25 | SMTP |
| Web Admin | 3000 | HTTP (Grafana) |

## Security Checklist

- [ ] Running on isolated network/VLAN
- [ ] Firewall rules configured
- [ ] Changed default Grafana password
- [ ] Not exposed directly to internet
- [ ] Logs being monitored regularly
- [ ] Legal authorization obtained

## Dashboard Access

**Grafana**: http://localhost:3000
- Username: `admin`
- Password: `honeypot123` (change this!)

**Pre-loaded Dashboards**:
1. Honeypot Attack Overview - Attack activity, logs, top IPs
2. Honeypot System Metrics - CPU, memory, network stats

## Troubleshooting

**Services won't start?**
- Check port conflicts: `sudo netstat -tulpn | grep -E '2222|21|8888|3000'`
- View logs: `docker compose logs`

**No data in Grafana?**
- Wait 1-2 minutes after startup
- Generate test traffic: `./scripts/test-honeypots.sh`
- Check Promtail: `docker compose logs promtail`

**Need help?**
- See full documentation in `README.md`
- Check individual container logs
- Verify all containers are running: `docker compose ps`
