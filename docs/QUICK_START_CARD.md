# QUICK START CARD - For Presentation Day

## 🎯 Before You Start (5 minutes before)

### 1. Verify Everything Works
```bash
cd /home/kali/Desktop/cys-project-final
./scripts/verify-setup.sh
```

### 2. Start Services (if not running)
```bash
./deploy.sh
```

### 3. Open Grafana in Browser
```
URL: http://localhost:3000
Username: admin
Password: honeypot123
```

---

## 🎬 Demo Commands (Copy-Paste Ready)

### SSH Attack Demo
```bash
# Terminal 1 - Monitor logs
tail -f logs/ssh-honeypot/ssh_honeypot.json

# Terminal 2 - Attack
ssh -p 222 admin@localhost
# Password: admin

ssh -p 222 root@localhost
# Password: password

ssh -p 222 ubuntu@localhost
# Password: 123456
```

### Web Attack Demo
```bash
# Common paths
curl http://localhost/admin
curl http://localhost/.env
curl http://localhost/phpmyadmin/

# Login attempt
curl -X POST http://localhost/login -d "username=admin&password=admin123"
```

### FTP Attack Demo
```bash
ftp localhost 211
# Username: anonymous
# Password: (just press Enter)
# Type: quit
```

### Analysis Commands
```bash
# Count SSH attacks
jq -s 'length' logs/ssh-honeypot/ssh_honeypot.json

# Top usernames
jq -r '.username' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head -5

# Top passwords
jq -r '.password' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head -5

# Top web paths
jq -r '.path' logs/web-honeypot/honeypot.json | sort | uniq -c | sort -rn | head -5
```

---

## 📊 Grafana Dashboards to Show

1. **Honeypot Overview** - Start here (shows everything)
2. **SSH Honeypot Dashboard** - Detailed SSH analysis
3. **Web Honeypot Dashboard** - HTTP attack patterns
4. **FTP Honeypot Dashboard** - FTP monitoring

---

## 🗣️ Key Talking Points

### Introduction (30 seconds)
> "This is a honeypot security monitoring system. It deploys fake services to attract attackers, captures their actions, and visualizes attack patterns in real-time."

### Architecture (30 seconds)
> "The system uses 4 Docker containers: 3 honeypots capturing SSH, FTP, and Web attacks, plus Grafana for visualization. Everything logs to JSON files for easy analysis."

### Demonstration (2 minutes per honeypot)
> "Let me show you how it captures attacks. I'll attempt to login with common credentials that attackers use..."

### Analysis (1 minute)
> "All data is logged in JSON format. Using simple command-line tools, we can analyze attack patterns, identify common credentials, and track attacker behavior."

---

## ❓ Expected Questions & Answers

**Q: Can this be used in production?**
> "Yes, with proper network segmentation, firewall rules, and monitoring. It's designed for research and threat intelligence."

**Q: What happens if someone breaks in?**
> "The containers are isolated. Even if compromised, they have no access to other systems. We also don't execute attacker commands."

**Q: How do you prevent it from attacking others?**
> "The honeypots don't execute commands and have no outbound network access."

**Q: Why these specific ports?**
> "Port 222 and 211 avoid conflicts with host services while still being commonly scanned. Port 80 is standard HTTP."

---

## 🔧 Troubleshooting (If Something Goes Wrong)

### Services not running
```bash
docker compose down
docker compose up -d
docker compose ps
```

### Grafana not loading
```bash
docker compose restart grafana
curl http://localhost:3000/api/health
```

### No data in dashboards
```bash
# Run quick attacks
ssh -p 222 test@localhost
curl http://localhost/admin

# Check logs
tail logs/ssh-honeypot/ssh_honeypot.json
```

### Ports in use
```bash
ss -tuln | grep -E ':222|:211|:80|:3000'
# Change ports in docker-compose.yml if needed
```

---

## 📁 Files to Reference

- **For Demo**: `ATTACK_SIMULATION.md`
- **For Talking**: `PRESENTATION_GUIDE.md`
- **For Questions**: `README.md` and `ARCHITECTURE.md`
- **For Code Review**: `ssh-honeypot/ssh_honeypot.py`, `web-honeypot/app.py`

---

## ⏱️ Timing Guide (15-minute presentation)

- 0:00-0:30 → Introduction
- 0:30-1:00 → Architecture overview
- 1:00-6:00 → SSH demo (monitor + attack + dashboard)
- 6:00-10:00 → Web demo (attacks + dashboard)
- 10:00-12:00 → Combined dashboard + analysis
- 12:00-13:00 → Quick command analysis demo
- 13:00-15:00 → Wrap-up + Q&A

---

## ✅ Pre-Demo Checklist

- [ ] All services running (`docker compose ps`)
- [ ] Grafana accessible (http://localhost:3000)
- [ ] Browser tabs open (Grafana dashboards)
- [ ] 2-3 terminal windows ready
- [ ] This quick start card visible
- [ ] Backup screenshots ready
- [ ] Confident and prepared!

---

## 🎓 Success Criteria

By end of demo, instructor should know:
- ✅ What honeypots are
- ✅ How the system works
- ✅ What attacks it captures
- ✅ How to analyze the data
- ✅ Security considerations

---

## 📞 Emergency Backup

If live demo fails:
1. Show pre-populated log files
2. Run analysis commands on existing data
3. Show screenshots of dashboards
4. Walk through architecture diagram
5. Explain what would happen

---

**YOU'VE GOT THIS! 🚀**

*Keep this card visible during your presentation for quick reference*
