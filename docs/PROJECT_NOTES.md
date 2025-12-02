# Comprehensive Honeypot Project Notes

This document provides detailed notes on the simplified honeypot stack, including architecture, implementation, operations, analysis workflows, common Q&A, improvements roadmap, and appendix references. It is intended for engineers, students, and analysts using this repository.

---

## 1. Overview

- Purpose: Observe attacker behavior across SSH, FTP, and Web vectors, with minimal operational overhead.
- Design principle: Fewer moving parts, direct JSON logging, easy visualization.
- Services: SSH honeypot (Paramiko), FTP honeypot (Dionaea), Web honeypot (Flask), Grafana for dashboards.
- Ports: SSH `222`, FTP `211`, Web `80`, Grafana `3000`.
- Logs: JSON/NDJSON outputs under `./logs/` mounted into containers.

---

## 2. Architecture

- Flow: Attacker → Honeypots → JSON logs → Grafana dashboards.
- Network: Bridge `honeypot-net` (`172.25.0.0/16`), isolated containers, selective port exposure.
- Volumes:
  - SSH: `./logs/ssh-honeypot:/app/logs`
  - FTP: `./logs/dionaea:/opt/dionaea/var/log`
  - Web: `./logs/web-honeypot:/app/logs`
  - Grafana: Reads `./logs` and uses persistent `grafana-data` volume.
- Simplification: Removed Loki/Promtail/Prometheus and metrics exporters; Grafana reads JSON directly.

---

## 3. Implementation Details

### 3.1 Docker Compose (`docker-compose.yml`)
- Defines services, ports, volumes, environment, and network.
- Key images: `dinotools/dionaea`, `grafana/grafana:10.2.2`, custom builds for SSH and Web.
- Labels: Used to annotate honeypot types and monitoring components.

### 3.2 SSH Honeypot (`ssh-honeypot/ssh_honeypot.py`)
- Tech: Python 3.11 + Paramiko.
- Behavior: Logs connection, password/publickey auth attempts, and typed commands.
- Output: NDJSON-style entries to `ssh_honeypot.json`.
- Port: `222`. Host key loaded from `/app/ssh_host_rsa_key`.
- Command emulation: `ls`, `cat` (permission denied), `whoami`, `pwd`, `exit`.

### 3.3 Web Honeypot (`web-honeypot/app.py`)
- Tech: Python 3.11 + Flask + Gunicorn (via Dockerfile).
- Behavior: Logs all HTTP requests, fake admin portal, common attack surface paths (`/.env`, `/phpMyAdmin/`, `/wp-admin/`, `/.git/config`).
- Output: NDJSON-style entries to `honeypot.json`.
- Port: `80`. Returns JSON or HTML fake responses.

### 3.4 FTP Honeypot (Dionaea)
- Image: `dinotools/dionaea:latest` with FTP only (external `211` mapped to container `21`).
- Logs: Written under `./logs/dionaea/` in Dionaea’s native formats.

### 3.5 Grafana
- Plugin: `marcusolsson-json-datasource` to read local JSON.
- Provisioning: Datasources and dashboards from `config/grafana/*` and `dashboards/*`.
- Credentials: `admin / honeypot123` (must be changed in production).

### 3.6 Log Server (`log-server/convert_logs.py`)
- Purpose: Optional helper to convert NDJSON to normalized JSON arrays over HTTP (`:8080`).
- Reads files from `/logs` (mounted read-only) and normalizes keys.

---

## 4. Deployment & Operations

### 4.1 Prerequisites
- Linux host with Docker and Docker Compose.
- Available ports: `222`, `211`, `80`, `3000`.
- Disk space: ~10 GB; Memory: ~500 MB.

### 4.2 Quick Deploy
- Script: `./deploy.sh` performs port checks, builds custom images, and starts services.

### 4.3 Manual Commands
- Start: `docker compose up -d`
- Stop: `docker compose down`
- Logs: `docker compose logs -f`
- Status: `docker compose ps`
- Rebuild: `docker compose build && docker compose up -d`

### 4.4 Access
- SSH: `ssh -p 222 user@localhost`
- FTP: `ftp localhost 211`
- Web: `http://localhost`
- Grafana: `http://localhost:3000` (admin / honeypot123)

---

## 5. Logging & Analysis

### 5.1 File Locations
- SSH: `logs/ssh-honeypot/ssh_honeypot.json`
- Web: `logs/web-honeypot/honeypot.json`
- FTP: `logs/dionaea/`

### 5.2 Quick `jq` Examples
- Count SSH attempts: `cat logs/ssh-honeypot/ssh_honeypot.json | jq -s 'length'`
- Top usernames: `jq -r '.username' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head`
- Top passwords: `jq -r '.password' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head`
- HTTP paths: `jq -r '.path' logs/web-honeypot/honeypot.json | sort | uniq -c | sort -rn | head`

### 5.3 Grafana Dashboards
- Dashboard JSON exists in `dashboards/`. Ensure provisioning references are correct in `config/grafana/dashboards`.
- The JSON datasource should point to files or the log server endpoints.

### 5.4 Sample Attack Scenarios
- Brute-force SSH against common usernames.
- Web probing for `.env`, `/phpMyAdmin/`, `/.git/config`, `/wp-admin/`.
- FTP anonymous login attempts and directory listings.

---

## 6. Security Considerations

- Never expose directly to the public internet without filtering and segmentation.
- Change Grafana default credentials immediately for non-lab use.
- Isolate containers with firewall rules; monitor egress traffic.
- Regularly rotate SSH host keys and review filesystem mounts.
- Ensure logs do not contain sensitive environment secrets.

---

## 7. Q&A (Common Questions)

- Q: Why port 222 for SSH instead of 22?
  - A: Avoid conflicts with host SSH while remaining believable to attackers scanning non-standard ports.

- Q: How does Grafana read logs without Loki/Promtail?
  - A: Via the `marcusolsson-json-datasource` plugin that accesses local JSON files (bind-mounted) or the optional log server.

- Q: Can I add alerts?
  - A: Yes, Grafana alerting can work with some datasources; for file-based JSON, consider a lightweight sidecar that scans logs and emits webhooks or Prometheus metrics.

- Q: Where are the dashboards?
  - A: In `dashboards/` with provisioning in `config/grafana/dashboards/`.

- Q: Is FTP safe to run?
  - A: Use it only in a lab network. Dionaea exposes intentionally vulnerable surfaces; segment and filter traffic appropriately.

- Q: How to parse Dionaea logs?
  - A: Use Python with `glob` and parse its log files (e.g., JSON or text). Consider enhancing `log-server` to support Dionaea formats.

---

## 8. Improvements Roadmap

- Logging:
  - Add NDJSON-to-array normalization in Grafana via log-server endpoints for large datasets.
  - Include per-service log rotation and compression.

- Detection & Enrichment:
  - GeoIP enrichment for `src_ip` fields in SSH/Web logs.
  - ASN/Cloud provider tagging (e.g., using `ipinfo` or `maxminddb`).

- Visualization:
  - Add panels for top IPs, usernames, passwords, HTTP paths, and time-series attack rates.
  - Create per-protocol dashboards with drill-down.

- Safety:
  - Egress controls to prevent outbound connections from compromised containers.
  - Runtime user remapping to non-root where possible.

- Scale & Extensibility:
  - Optional Loki/Promtail reintroduction when multi-host scaling is required.
  - Add mail/SMTP or Telnet honeypots via Dionaea modules.

---

## 9. Troubleshooting

- Ports in use: Use `ss -tuln` or `netstat -tuln` to check; change mappings in `docker-compose.yml` if necessary.
- Grafana plugin not loading: Verify `GF_INSTALL_PLUGINS` includes `marcusolsson-json-datasource`; check container logs.
- Permission issues on `./logs`: Adjust host directory ownership/permissions or run Grafana as root (current config sets `user: "0:0"`).
- Empty dashboards: Ensure log files exist and datasource paths are correct; test with sample entries.

---

## 10. Appendix: File Map

- `ARCHITECTURE.md`: Visual diagrams and comparisons.
- `IMPLEMENTATION_SUMMARY.md`: Changes and specifications after simplification.
- `EVALUATION.md`: Project evaluation and metrics.
- `QUICK_REFERENCE.md`: Commands and ports cheat sheet.
- `deploy.sh`: Deployment automation script.
- `ssh-honeypot/ssh_honeypot.py`: Custom SSH honeypot.
- `web-honeypot/app.py`: Custom Web honeypot.
- `log-server/convert_logs.py`: NDJSON normalization server.
- `dashboards/*.json`: Grafana dashboards.
- `config/grafana/*`: Provisioning for datasources and dashboards.

---

## 11. Suggested Study Questions (with Answers)

1) Explain the data flow from an attack to visualization.
- Attacker connects to exposed ports → honeypot containers log structured events → logs written to host-mounted directories → Grafana reads JSON via plugin → dashboards visualize patterns over time.

2) Why was Loki/Promtail removed, and what trade-offs does this introduce?
- Removal reduces complexity and resource usage. Trade-offs: loses advanced querying (LogQL), centralized aggregation, and built-in alerting. For single-host labs, direct JSON is sufficient; for distributed setups, consider reintroducing Loki.

3) How does the SSH honeypot ensure no successful authentication while still logging attempts?
- It implements `paramiko.ServerInterface` and returns `AUTH_FAILED` for password/publickey checks but logs the attempts before rejecting.

4) What are best practices for safely operating honeypots?
- Network segmentation, firewalling, monitoring, least privilege, disabling outbound egress, rotating keys, and sanitizing/isolating logs.

5) Propose a method to enrich logs with geolocation.
- Add a sidecar process reading NDJSON lines, calling a GeoIP database (MaxMind) to append `country`, `asn`, `org` fields, and writing enriched outputs to a separate file for Grafana.

6) How would you add alerting for high-rate SSH brute-force attempts without Prometheus?
- A cron or daemon tailing the log, computing rate per minute, and sending webhooks/email via a simple script. Alternatively, push metrics to a lightweight Pushgateway and add a small Prometheus instance.

7) Describe how the Web honeypot simulates common targets.
- Implements routes for `.env`, `phpMyAdmin`, `wp-admin`, `.git/config`, and returns plausible content with 200/403/404 codes, logging all request metadata.

8) What is the role of `log-server/convert_logs.py`?
- Serves NDJSON logs as normalized JSON arrays to ease Grafana/table visualization and comparisons, ensuring all entries share the same set of keys.

---

## 12. References & Further Reading

- Paramiko docs, Flask docs, Grafana JSON datasource plugin, Dionaea honeypot documentation.

---

## 13. Glossary (Easy Definitions)

- Honeypot: A decoy system designed to attract attackers and record their actions safely.
- SSH: Secure Shell; a protocol to remotely access servers via command line.
- FTP: File Transfer Protocol; used to upload/download files to a server.
- HTTP: Web traffic protocol used by browsers and APIs.
- NDJSON: Newline-Delimited JSON; each line is a separate JSON object.
- Grafana: A dashboard tool that visualizes data from various sources.
- Datasource: A configured data input for Grafana (e.g., JSON files).
- Dionaea: A multi-protocol honeypot focused on capturing malware and attacks.
- Paramiko: A Python library for SSH functionality.
- Container: A lightweight, isolated runtime for applications (Docker).
- Bridge Network: A private local network connecting containers.

---

## 14. Quick Visuals (ASCII Diagrams)

Attacks → Logs → Dashboard

```
Internet
   │
   ├── SSH (222) ─┐
   ├── FTP (211) ─┼─► Writes JSON to ./logs
   └── Web (80) ──┘
                     │
                     ▼
                Grafana (3000)
                Reads JSON directly
```

Container Network

```
Host (Kali)
└─ docker bridge: honeypot-net (172.25.0.0/16)
   ├─ honeypot-ssh
   ├─ honeypot-ftp
   ├─ honeypot-web
   └─ honeypot-grafana
```

---

## 15. Hands-on Labs (Step-by-Step)

### Lab A: SSH Brute Force Simulation
Goal: Generate login attempts and command logs.

Commands:
```zsh
ssh -p 222 admin@localhost || true
ssh -p 222 root@localhost || true
ssh -p 222 user@localhost || true
```
Then type a few commands:
```zsh
# After it prompts, try:
ls
whoami
pwd
exit
```
Verify logs:
```zsh
tail -f logs/ssh-honeypot/ssh_honeypot.json | head -n 20
```

Expected: Entries with `event_type` of `login_attempt`, `connection`, and `command`.

### Lab B: Web Probing
Goal: Generate HTTP request logs and explore common endpoints.

Commands:
```zsh
curl http://localhost/
curl -X POST http://localhost/login -d "username=admin&password=pass123"
curl http://localhost/.env
curl http://localhost/phpMyAdmin/
curl http://localhost/.git/config
```
Verify logs:
```zsh
tail -f logs/web-honeypot/honeypot.json | head -n 20
```

Expected: JSON entries with `path`, `method`, `headers`, `form_data`.

### Lab C: FTP Attempts
Goal: Record FTP login attempts.

Commands:
```zsh
ftp localhost 211 <<'EOF'
anonymous
test
ls
quit
EOF
```
Verify logs:
```zsh
ls -la logs/dionaea/
```

Expected: New files written by Dionaea indicating connections and attempts.

---

## 16. Expanded Q&A and Tips

- Q: How can I avoid filling disk space with logs?
  - A: Enable log rotation (e.g., `logrotate`) and compress old files; consider daily archives.

- Q: Can attackers pivot from honeypots to other systems?
  - A: Minimize risk via strict firewalling, disable egress, and isolate networks; treat containers as untrusted.

- Q: Why run Grafana as root here?
  - A: To avoid common read-permission issues with bind-mounted logs. For production, prefer explicit permissions over root.

- Q: How to anonymize sensitive data?
  - A: Post-process logs to remove IPs or hash usernames/passwords when sharing externally.

Checklist (safe operation):
- Change default credentials.
- Restrict inbound to lab ranges.
- Disable outbound traffic.
- Monitor resource usage.
- Review logs regularly.

---

## 17. Grafana Quick Guide

Datasource setup (JSON plugin):
- Ensure plugin is installed via `GF_INSTALL_PLUGINS=marcusolsson-json-datasource`.
- In Grafana: Configuration → Data sources → Add JSON.
- URL options:
  - File path via local server (e.g., `http://honeypot-log-server:8080/ssh-honeypot/ssh_honeypot.json`).
  - Or direct file path if supported by your setup.

Example panels to create:
- Top SSH usernames (table): Group by `.username`, count.
- Top SSH passwords (table): Group by `.password`, count.
- HTTP paths hit (bar chart): Group by `.path`, count.
- Attack rate over time (time series): Count per minute using timestamps.

Troubleshooting:
- Empty panels: Verify datasource URL and that the file contains data.
- Permission denied: Check mount paths and container user.
- Mixed fields: Normalize NDJSON to arrays via `log-server`.

---

## 18. Ready-Made Commands (Copy/Paste)

Environment checks:
```zsh
docker compose ps
docker compose logs -f
ss -tuln | grep -E ':222|:211|:80|:3000'
```

Log analysis snippets:
```zsh
jq -r '.src_ip' logs/ssh-honeypot/ssh_honeypot.json | sort | uniq -c | sort -rn | head
jq -r '.path' logs/web-honeypot/honeypot.json | sort | uniq -c | sort -rn | head
```

---

## 19. Future Enhancements (Detailed)

- GeoIP Enrichment:
  - Add a Python service reading NDJSON and annotating entries with `country`, `city`, `asn` via MaxMind DB.
- Lightweight Alerting:
  - A daemon computing per-minute rates and sending webhook alerts when thresholds are exceeded.
- Better Log Modeling:
  - Define a schema per honeypot and validate entries to reduce parsing errors.
- Data Retention:
  - Move old logs to `logs/archive/YYYY-MM-DD/` with compression and index files.

---

## 20. Quick Recap (Beginner-Friendly)

- You run three fake services (SSH, FTP, Web) to attract attackers.
- All activities are saved into simple JSON log files.
- Grafana reads those files and shows charts and tables.
- This stack is small and easy to run on one machine.
- Keep it isolated and monitored to stay safe.
