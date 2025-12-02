# Honeypot Project - Instructor Presentation Guide

**Semester Project Demonstration**  
*Comprehensive guide for presenting the honeypot security monitoring system*

---

## Project Overview

### What This Project Does
- Deploys multiple honeypots (SSH, FTP, Web) to attract and log cyber attacks
- Captures attacker credentials, commands, and reconnaissance activities
- Provides real-time visualization through Grafana dashboards
- Demonstrates modern containerized security monitoring architecture

### Key Features
✅ **Multiple Attack Vectors**: SSH (port 222), FTP (port 211), Web (port 80)  
✅ **Real-time Monitoring**: Live dashboards with 5-second refresh  
✅ **Structured Logging**: JSON format for easy analysis  
✅ **Containerized Deployment**: Docker Compose for easy setup  
✅ **Lightweight Architecture**: Only 4 containers, ~500MB RAM  

---

## Pre-Presentation Checklist

### Day Before Presentation
- [ ] Test all services: `docker compose ps`
- [ ] Verify Grafana access: http://localhost:3000
- [ ] Run test attacks to populate dashboards
- [ ] Take screenshots of populated dashboards
- [ ] Review all documentation files
- [ ] Prepare backup presentation slides

### 1 Hour Before Presentation
- [ ] Start all services: `./deploy.sh`
- [ ] Clear old logs (optional): `rm logs/*/*.json`
- [ ] Run attack simulations: see `ATTACK_SIMULATION.md`
- [ ] Open Grafana in browser
- [ ] Open terminal windows for live demos
- [ ] Test internet connection (if doing live demos)

### Equipment Needed
- Laptop with Docker installed
- Projector/screen connection
- Backup: Screenshots of dashboards
- Backup: Pre-recorded demo video (optional)
- Printed documentation (optional)

---

## Presentation Structure (15-20 minutes)

### 1. Introduction (2 minutes)
**Script:**
> "Today I'm presenting a honeypot security monitoring system. Honeypots are decoy systems designed to attract attackers and study their behavior. This project deploys three different honeypots - SSH, FTP, and Web - captures all attack attempts, and visualizes them in real-time dashboards."

**Show:**
- Architecture diagram from `ARCHITECTURE.md`
- Mention: 4 containers, 3 honeypots, 1 dashboard

---

### 2. Architecture Explanation (3 minutes)

**Script:**
> "The system uses Docker containers for isolation. Each honeypot runs independently, logs attacks to JSON files, and Grafana reads these files directly to create visualizations. This simplified architecture eliminates the need for complex log aggregation systems."

**Show:**
- `docker compose ps` - All services running
- File structure: `tree -L 2`
- Brief walkthrough of docker-compose.yml

**Key Points:**
- Containerized for portability
- Each honeypot simulates a real service
- JSON logging for structured data
- Grafana for visualization

---

### 3. Live Demonstration - SSH Attacks (4 minutes)

**Script:**
> "Let me demonstrate how the SSH honeypot captures attacks. I'll attempt to login with common credentials that attackers typically use."

**Terminal 1 - Monitor logs:**
```bash
# Show this on screen
tail -f logs/ssh-honeypot/ssh_honeypot.json
```

**Terminal 2 - Attack simulation:**
```bash
# Try several logins
ssh -p 222 admin@localhost
# Password: admin

ssh -p 222 root@localhost  
# Password: password

ssh -p 222 ubuntu@localhost
# Password: 123456
```

**Explain what's happening:**
- Each attempt is logged immediately
- Captures username, password, IP, timestamp
- Authentication always fails but data is captured

**Show in Grafana:**
- Open SSH Honeypot Dashboard
- Point out:
  - Total attacks counter
  - Unique IPs
  - Top usernames table
  - Top passwords chart
  - Recent login attempts

---

### 4. Live Demonstration - Web Attacks (3 minutes)

**Script:**
> "The web honeypot simulates a vulnerable web application. It logs all HTTP requests, including attempts to find admin panels, configuration files, and other sensitive endpoints."

**Terminal - Attack simulation:**
```bash
# Common attack patterns
curl http://localhost/admin
curl http://localhost/.env
curl http://localhost/phpMyAdmin/
curl http://localhost/.git/config

# Login attempt
curl -X POST http://localhost/login \
  -d "username=admin&password=admin123"
```

**Show in Grafana:**
- Open Web Honeypot Dashboard
- Point out:
  - Total HTTP requests
  - Unique attacker IPs
  - Top paths accessed (bar chart)
  - Login attempts table
  - HTTP methods distribution

**Highlight:**
- Shows what attackers are looking for
- Common CMS and framework paths
- Sensitive file discovery attempts

---

### 5. Combined Dashboard (2 minutes)

**Script:**
> "The combined overview dashboard shows all attack vectors in one place, allowing security analysts to see the big picture of attack activity."

**Show in Grafana:**
- Open Honeypot Overview Dashboard
- Point out:
  - Attack counters for each honeypot
  - Timeline showing all attacks
  - Recent attacks from all sources
  - Links to detailed dashboards

---

### 6. Data Analysis (3 minutes)

**Script:**
> "The system logs everything in JSON format, which makes it easy to analyze with standard command-line tools."

**Terminal - Live analysis:**
```bash
# Count total SSH attacks
jq -s 'length' logs/ssh-honeypot/ssh_honeypot.json

# Top 5 usernames attempted
jq -r '.username' logs/ssh-honeypot/ssh_honeypot.json | \
  sort | uniq -c | sort -rn | head -5

# Top 5 passwords tried
jq -r '.password' logs/ssh-honeypot/ssh_honeypot.json | \
  sort | uniq -c | sort -rn | head -5

# Most accessed web paths
jq -r '.path' logs/web-honeypot/honeypot.json | \
  sort | uniq -c | sort -rn | head -5
```

**Explain:**
- JSON format enables powerful analysis
- Can be imported into other tools
- Easy to automate reporting

---

### 7. Security Considerations (2 minutes)

**Script:**
> "While honeypots are powerful security tools, they must be deployed carefully to avoid becoming security risks themselves."

**Key Points:**
- ⚠️ Never expose directly to internet without proper segmentation
- ⚠️ Honeypots should be isolated from production networks
- ⚠️ Regular monitoring for unusual activity
- ⚠️ Firewall rules to control access
- ⚠️ Change default Grafana credentials

**Show:**
- Security section in README.md
- Docker network isolation
- Port mappings in docker-compose.yml

---

### 8. Conclusion & Q&A (1-2 minutes)

**Summary Points:**
- Deployed functional honeypot system with 3 attack vectors
- Real-time monitoring and visualization
- Captures valuable threat intelligence
- Containerized for easy deployment
- Lightweight and resource-efficient

**Technical Skills Demonstrated:**
- Docker containerization
- Python development (SSH and Web honeypots)
- Network security concepts
- Data visualization with Grafana
- Log analysis and JSON processing
- System architecture design

**Potential Questions & Answers:**
See FAQ section below

---

## FAQ - Anticipated Questions

### Technical Questions

**Q: Why port 222 instead of 22 for SSH?**
> A: Port 22 might be used by the host system's SSH service. Port 222 is non-standard but still commonly scanned by attackers, making it realistic while avoiding conflicts.

**Q: How does Grafana read the logs without Loki?**
> A: We use the marcusolsson-json-datasource plugin that reads JSON files directly from the filesystem. This simplifies the architecture but is suitable for single-host deployments.

**Q: Can the honeypots be exploited?**
> A: The honeypots are isolated in Docker containers with limited capabilities. The SSH and Web honeypots are custom Python code that doesn't execute attacker commands. However, defense-in-depth with network segmentation is still recommended.

**Q: How do you prevent the honeypots from being used to attack others?**
> A: The containers have no outbound internet access by default. We also don't execute attacker-provided commands, only log them.

**Q: What's the resource usage?**
> A: The entire stack uses approximately 500MB RAM and minimal CPU. It's very lightweight compared to traditional security monitoring solutions.

### Conceptual Questions

**Q: What's the value of honeypot data?**
> A: Honeypots provide early warning of attacks, reveal attacker TTPs (Tactics, Techniques, Procedures), help identify common vulnerabilities being exploited, and can track emerging threats.

**Q: How is this different from an IDS/IPS?**
> A: IDS/IPS monitors real production traffic for threats. Honeypots have no legitimate users - all traffic is inherently suspicious. They complement each other.

**Q: Could this be deployed in a real enterprise?**
> A: Yes, but it would need enhancements: proper network segmentation, integration with SIEM, alerting system, automated threat intelligence, and compliance with policies.

**Q: What would you improve?**
> A: See IMPROVEMENTS section below.

---

## Backup Demo (If Live Demo Fails)

### Show Pre-populated Data
- Navigate to logs directory
- Show JSON files with captured data
- Run jq analysis commands on existing data
- Show screenshots of dashboards

### Explain What Would Happen
- Walk through attack simulation document
- Explain expected behavior
- Show code that handles attacks

---

## Advanced Topics (If Time Permits)

### 1. Automated Attack Simulation
```bash
# Show the script
cat scripts/test-honeypots.sh

# Explain what it does
# Run it if time allows
./scripts/test-honeypots.sh
```

### 2. Log Analysis Examples
Show advanced queries:
```bash
# Group attacks by hour
jq -r '.timestamp[:13]' logs/ssh-honeypot/ssh_honeypot.json | \
  sort | uniq -c

# Find username/password pairs
jq -r '[.username, .password] | @tsv' \
  logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c
```

### 3. Architecture Comparison
- Show original vs. simplified architecture
- Explain why simplification was beneficial
- Discuss scalability considerations

---

## Project Improvements (Future Work)

### Immediate Enhancements
1. **GeoIP Integration**: Add geographic location of attackers
2. **Email Alerts**: Notify on high-rate attacks
3. **Database Storage**: Move from files to TimescaleDB
4. **API Endpoint**: REST API to query attack data

### Advanced Features
1. **Machine Learning**: Anomaly detection on attack patterns
2. **Threat Intelligence**: Integrate with threat feeds
3. **Multi-Host**: Deploy across multiple servers
4. **Deception Tech**: More realistic service emulation

### Production Readiness
1. **Authentication**: Secure Grafana with SSO
2. **Encryption**: TLS for all services
3. **Backup**: Automated log backup and rotation
4. **Compliance**: GDPR-compliant log handling

---

## Files to Reference During Presentation

1. **README.md** - Quick overview and commands
2. **ARCHITECTURE.md** - Visual diagrams
3. **ATTACK_SIMULATION.md** - All attack commands
4. **QUICK_REFERENCE.md** - Command cheat sheet
5. **docker-compose.yml** - Service definitions
6. **docs/PROJECT_NOTES.md** - Comprehensive documentation

---

## Troubleshooting During Presentation

### Services Not Starting
```bash
# Check Docker
docker --version
docker compose version

# Check ports
ss -tuln | grep -E ':222|:211|:80|:3000'

# Restart services
docker compose down
docker compose up -d
```

### Grafana Not Loading
```bash
# Check Grafana logs
docker compose logs grafana

# Verify it's running
curl http://localhost:3000/api/health

# Restart Grafana
docker compose restart grafana
```

### No Data in Dashboards
```bash
# Check if logs exist
ls -lah logs/ssh-honeypot/
ls -lah logs/web-honeypot/

# Run quick attack
ssh -p 222 test@localhost

# Check if logged
tail logs/ssh-honeypot/ssh_honeypot.json
```

---

## Presentation Tips

### Do's
✅ Practice the demo multiple times  
✅ Have backup screenshots ready  
✅ Explain concepts simply  
✅ Show enthusiasm for security  
✅ Engage with the audience  
✅ Time your presentation  

### Don'ts
❌ Rush through important points  
❌ Assume technical knowledge  
❌ Skip error handling  
❌ Read slides verbatim  
❌ Ignore questions  
❌ Go over time limit  

---

## Grading Criteria Alignment

### Technical Implementation (40%)
- ✅ Multiple functional honeypots
- ✅ Proper containerization
- ✅ Data persistence and logging
- ✅ Network configuration
- ✅ Security considerations

### Documentation (30%)
- ✅ Comprehensive README
- ✅ Architecture diagrams
- ✅ Code comments
- ✅ Setup instructions
- ✅ Attack simulation guide

### Demonstration (20%)
- ✅ Live working demo
- ✅ Clear explanation
- ✅ Understanding of concepts
- ✅ Handling questions
- ✅ Professional presentation

### Innovation (10%)
- ✅ Simplified architecture
- ✅ Multiple dashboards
- ✅ Automated deployment
- ✅ Analysis capabilities
- ✅ Practical application

---

## Post-Presentation

### Share with Instructor
1. GitHub repository link
2. This presentation guide
3. Attack simulation results
4. Screenshots of dashboards
5. Any additional documentation

### Demo for Others
- Colleagues/classmates
- Portfolio piece
- Technical blog post
- LinkedIn project

---

## Success Metrics

**By the end of the presentation, the instructor should understand:**
1. What honeypots are and why they're valuable
2. How this system captures and analyzes attacks
3. The technical architecture and design decisions
4. How to deploy and use the system
5. Security considerations and best practices

**You will have succeeded if:**
- All demos work smoothly
- Questions are answered confidently
- Technical depth is demonstrated
- Security knowledge is evident
- Professional presentation delivered

---

## Quick Command Reference for Presentation

```bash
# Start everything
./deploy.sh

# Check status
docker compose ps

# View logs
docker compose logs -f

# Attack SSH
ssh -p 222 admin@localhost

# Attack Web
curl http://localhost/admin

# Attack FTP
ftp localhost 211

# Analyze data
jq -s 'length' logs/ssh-honeypot/ssh_honeypot.json

# Open Grafana
xdg-open http://localhost:3000
```

---

## Contact & Resources

**Project Repository**: [Include your GitHub link]  
**Documentation**: All files in the repository  
**Questions**: Available after presentation

---

**Good luck with your presentation! 🍀**
