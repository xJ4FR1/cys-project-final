# Quick Reference Card - Simplified Honeypot

## 🚀 Quick Start
```bash
./deploy.sh
```

## 📋 Service Ports

| Service | Port | URL/Connection |
|---------|------|----------------|
| SSH Honeypot | 222 | `ssh -p 222 user@localhost` |
| FTP Honeypot | 211 | `ftp localhost 211` |
| Web Honeypot | 80 | `http://localhost` |
| Grafana | 3000 | `http://localhost:3000` |

## 🔑 Default Credentials

**Grafana Dashboard**
- Username: `admin`
- Password: `honeypot123`
- ⚠️ Change this immediately!

## 📝 Docker Commands

```bash
# Start services
docker compose up -d

# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f ssh-honeypot
docker compose logs -f dionaea
docker compose logs -f web-honeypot
docker compose logs -f grafana

# Stop services
docker compose down

# Restart services
docker compose restart

# Check status
docker compose ps

# Rebuild after changes
docker compose build
docker compose up -d
```

## 📊 Log Locations

```bash
# SSH attacks
./logs/ssh-honeypot/ssh_honeypot.json

# FTP attacks
./logs/dionaea/

# Web attacks
./logs/web-honeypot/honeypot.json

# View live logs
tail -f logs/ssh-honeypot/ssh_honeypot.json
tail -f logs/web-honeypot/honeypot.json
```

## 🧪 Testing Commands

### Test SSH Honeypot
```bash
# Basic connection
ssh -p 222 admin@localhost

# Try common credentials
ssh -p 222 root@localhost
ssh -p 222 admin@localhost
ssh -p 222 user@localhost
```

### Test FTP Honeypot
```bash
# Using standard FTP
ftp localhost 211
# Username: anonymous
# Password: (any)

# Using curl
curl ftp://localhost:211/
curl -u admin:admin ftp://localhost:211/
```

### Test Web Honeypot
```bash
# GET requests
curl http://localhost/
curl http://localhost/admin
curl http://localhost/.env

# POST login attempt
curl -X POST http://localhost/login \
  -d "username=admin&password=test123"

# With custom headers
curl -H "User-Agent: AttackerBot/1.0" http://localhost/

# Simulated SQL injection
curl "http://localhost/admin?id=1' OR '1'='1"
```

## 🔍 Analyzing Logs

### Using jq (JSON processor)
```bash
# Pretty print logs
cat logs/ssh-honeypot/ssh_honeypot.json | jq .

# Count login attempts
cat logs/ssh-honeypot/ssh_honeypot.json | jq -s 'length'

# Extract usernames
cat logs/ssh-honeypot/ssh_honeypot.json | jq -r '.username' | sort | uniq -c

# Extract passwords
cat logs/ssh-honeypot/ssh_honeypot.json | jq -r '.password' | sort | uniq -c

# Filter by IP
cat logs/ssh-honeypot/ssh_honeypot.json | jq 'select(.src_ip=="192.168.1.100")'

# Show only login attempts
cat logs/ssh-honeypot/ssh_honeypot.json | jq 'select(.event_type=="login_attempt")'
```

### Using grep
```bash
# Find specific IP
grep "192.168.1.100" logs/ssh-honeypot/ssh_honeypot.json

# Count events by type
grep "login_attempt" logs/ssh-honeypot/ssh_honeypot.json | wc -l
grep "connection" logs/ssh-honeypot/ssh_honeypot.json | wc -l
```

## 🛠️ Troubleshooting

### Port already in use
```bash
# Check what's using the port
sudo netstat -tulpn | grep :222
sudo netstat -tulpn | grep :211
sudo netstat -tulpn | grep :80

# Kill process using port (replace PID)
sudo kill <PID>
```

### Service not starting
```bash
# Check container logs
docker compose logs ssh-honeypot
docker compose logs dionaea
docker compose logs web-honeypot

# Restart specific service
docker compose restart ssh-honeypot
```

### Grafana not showing data
```bash
# Check if logs exist
ls -lah logs/ssh-honeypot/
ls -lah logs/web-honeypot/

# Check Grafana logs
docker compose logs grafana

# Verify datasource configuration
docker compose exec grafana cat /etc/grafana/provisioning/datasources/datasources.yml
```

### Permission issues
```bash
# Fix log directory permissions
sudo chmod -R 755 logs/
sudo chmod -R 755 data/

# Fix ownership (replace with your user)
sudo chown -R $USER:$USER logs/
sudo chown -R $USER:$USER data/
```

### Grafana permission errors
```bash
# If Grafana fails with permission errors, it's already fixed in docker-compose.yml
# Just restart:
sudo docker compose down
sudo docker compose up -d

# If still failing, see GRAFANA_FIX.md for detailed troubleshooting
```

## 🔄 Updates & Maintenance

### Update Docker images
```bash
docker compose pull
docker compose up -d
```

### Clean up logs
```bash
# Backup first
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Clear logs
rm -f logs/ssh-honeypot/*.json
rm -rf logs/dionaea/*
rm -f logs/web-honeypot/*.json

# Restart to regenerate
docker compose restart
```

### Reset everything
```bash
# Stop and remove containers
docker compose down

# Remove volumes (WARNING: deletes all data)
docker compose down -v

# Clean up logs and data
rm -rf logs/* data/*

# Start fresh
./deploy.sh
```

## 📈 Statistics Commands

### Quick stats
```bash
# Total SSH attempts
cat logs/ssh-honeypot/ssh_honeypot.json | jq -s '. | length'

# Unique IPs (SSH)
cat logs/ssh-honeypot/ssh_honeypot.json | jq -r '.src_ip' | sort -u | wc -l

# Top 10 usernames tried
cat logs/ssh-honeypot/ssh_honeypot.json | jq -r '.username' | sort | uniq -c | sort -rn | head -10

# Top 10 passwords tried
cat logs/ssh-honeypot/ssh_honeypot.json | jq -r '.password' | sort | uniq -c | sort -rn | head -10

# Web requests by method
cat logs/web-honeypot/honeypot.json | jq -r '.method' | sort | uniq -c
```

## 🔐 Security Checklist

- [ ] Changed default Grafana password
- [ ] Configured firewall rules
- [ ] Set up log rotation
- [ ] Configured network segmentation (DMZ/VLAN)
- [ ] Enabled disk space monitoring
- [ ] Documented incident response procedures
- [ ] Tested all honeypot services
- [ ] Verified logs are being written
- [ ] Set up backup schedule for logs

## 📚 Important Files

```
docker-compose.yml          - Service definitions
deploy.sh                   - Deployment script
EVALUATION.md              - Project evaluation
SIMPLIFIED_SETUP.md        - Setup documentation
SIMPLIFICATION_REPORT.md   - Detailed changes
ssh-honeypot/ssh_honeypot.py - SSH honeypot code
web-honeypot/app.py        - Web honeypot code
```

## 🆘 Getting Help

1. Check logs: `docker compose logs -f`
2. Verify services: `docker compose ps`
3. Review documentation: `README.md`, `EVALUATION.md`
4. Check configuration: Review `docker-compose.yml`

---

**Last Updated**: November 30, 2025
