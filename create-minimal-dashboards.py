#!/usr/bin/env python3
import json

# Load working dashboard as template
with open('dashboards/honeypot-attacks.json', 'r') as f:
    template = json.load(f)

# ============================================
# SSH Dashboard - Minimal (2 graphs, 2 tables)
# ============================================

ssh_dashboard = {
    "annotations": template["annotations"],
    "editable": True,
    "gnetId": None,
    "graphTooltip": 0,
    "id": None,
    "links": [],
    "panels": [],
    "schemaVersion": 27,
    "style": "dark",
    "tags": ["honeypot", "ssh"],
    "templating": {"list": []},
    "time": {"from": "now-6h", "to": "now"},
    "timepicker": {},
    "timezone": "",
    "title": "SSH Honeypot Dashboard",
    "uid": "ssh-honeypot",
    "version": 0
}

# Copy timeseries panel (SSH Attack Timeline) from working dashboard
ssh_timeline = json.loads(json.dumps(template['panels'][0]))  # Deep copy
ssh_timeline['id'] = 1
ssh_timeline['title'] = "SSH Events Over Time"
ssh_timeline['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 0}
ssh_timeline['targets'][0]['datasource']['uid'] = 'ssh-logs'
ssh_timeline['targets'][0]['urlPath'] = '/ssh-honeypot/ssh_honeypot.json'

# Copy gauge panel for total count
ssh_gauge = json.loads(json.dumps(template['panels'][2]))  # Deep copy
ssh_gauge['id'] = 2
ssh_gauge['title'] = "Total SSH Attacks"
ssh_gauge['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 0}
ssh_gauge['targets'][0]['datasource']['uid'] = 'ssh-logs'
ssh_gauge['targets'][0]['urlPath'] = '/ssh-honeypot/ssh_honeypot.json'

# Copy piechart for event types
ssh_pie = json.loads(json.dumps(template['panels'][4]))  # Deep copy
ssh_pie['id'] = 3
ssh_pie['title'] = "SSH Event Types"
ssh_pie['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 8}
ssh_pie['targets'][0]['datasource']['uid'] = 'ssh-logs'
ssh_pie['targets'][0]['urlPath'] = '/ssh-honeypot/ssh_honeypot.json'

# Copy table panel (SSH Attack Log)
ssh_table = json.loads(json.dumps(template['panels'][6]))  # Deep copy
ssh_table['id'] = 4
ssh_table['title'] = "SSH Attack Log"
ssh_table['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 8}
ssh_table['targets'][0]['datasource']['uid'] = 'ssh-logs'
ssh_table['targets'][0]['urlPath'] = '/ssh-honeypot/ssh_honeypot.json'

ssh_dashboard['panels'] = [ssh_timeline, ssh_gauge, ssh_pie, ssh_table]

with open('dashboards/ssh-attacks.json', 'w') as f:
    json.dump(ssh_dashboard, f, indent=2)
print("✓ Created minimal SSH dashboard (2 graphs, 2 tables)")

# ============================================
# Web Dashboard - Minimal (2 graphs, 2 tables)
# ============================================

web_dashboard = {
    "annotations": template["annotations"],
    "editable": True,
    "gnetId": None,
    "graphTooltip": 0,
    "id": None,
    "links": [],
    "panels": [],
    "schemaVersion": 27,
    "style": "dark",
    "tags": ["honeypot", "web"],
    "templating": {"list": []},
    "time": {"from": "now-6h", "to": "now"},
    "timepicker": {},
    "timezone": "",
    "title": "Web Honeypot Dashboard",
    "uid": "web-honeypot",
    "version": 0
}

# Copy timeseries panel (Web Request Timeline)
web_timeline = json.loads(json.dumps(template['panels'][1]))  # Deep copy
web_timeline['id'] = 1
web_timeline['title'] = "Web Requests Over Time"
web_timeline['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 0}
# Already uses web-logs datasource

# Copy gauge panel for total count
web_gauge = json.loads(json.dumps(template['panels'][3]))  # Deep copy
web_gauge['id'] = 2
web_gauge['title'] = "Total Web Requests"
web_gauge['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 0}
# Already uses web-logs datasource

# Copy piechart for HTTP methods
web_pie = json.loads(json.dumps(template['panels'][5]))  # Deep copy
web_pie['id'] = 3
web_pie['title'] = "HTTP Methods Distribution"
web_pie['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 8}
# Already uses web-logs datasource

# Copy table panel (Web Attack Log)
web_table = json.loads(json.dumps(template['panels'][7]))  # Deep copy
web_table['id'] = 4
web_table['title'] = "Web Attack Log"
web_table['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 8}
# Already uses web-logs datasource

web_dashboard['panels'] = [web_timeline, web_gauge, web_pie, web_table]

with open('dashboards/web-attacks.json', 'w') as f:
    json.dump(web_dashboard, f, indent=2)
print("✓ Created minimal Web dashboard (2 graphs, 2 tables)")

# ============================================
# FTP Dashboard - Minimal (2 graphs, 2 tables)
# ============================================

ftp_dashboard = {
    "annotations": template["annotations"],
    "editable": True,
    "gnetId": None,
    "graphTooltip": 0,
    "id": None,
    "links": [],
    "panels": [],
    "schemaVersion": 27,
    "style": "dark",
    "tags": ["honeypot", "ftp"],
    "templating": {"list": []},
    "time": {"from": "now-6h", "to": "now"},
    "timepicker": {},
    "timezone": "",
    "title": "FTP Honeypot Dashboard",
    "uid": "ftp-honeypot",
    "version": 0
}

# Copy and adapt timeseries panel
ftp_timeline = json.loads(json.dumps(template['panels'][0]))  # Deep copy
ftp_timeline['id'] = 1
ftp_timeline['title'] = "FTP Events Over Time"
ftp_timeline['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 0}
ftp_timeline['targets'][0]['datasource']['uid'] = 'ftp-logs'
ftp_timeline['targets'][0]['urlPath'] = '/dionaea/ftp_parsed.json'

# Copy and adapt gauge panel
ftp_gauge = json.loads(json.dumps(template['panels'][2]))  # Deep copy
ftp_gauge['id'] = 2
ftp_gauge['title'] = "Total FTP Events"
ftp_gauge['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 0}
ftp_gauge['targets'][0]['datasource']['uid'] = 'ftp-logs'
ftp_gauge['targets'][0]['urlPath'] = '/dionaea/ftp_parsed.json'

# Copy and adapt piechart panel
ftp_pie = json.loads(json.dumps(template['panels'][4]))  # Deep copy
ftp_pie['id'] = 3
ftp_pie['title'] = "FTP Event Types"
ftp_pie['gridPos'] = {"h": 8, "w": 12, "x": 0, "y": 8}
ftp_pie['targets'][0]['datasource']['uid'] = 'ftp-logs'
ftp_pie['targets'][0]['urlPath'] = '/dionaea/ftp_parsed.json'

# Copy and adapt table panel
ftp_table = json.loads(json.dumps(template['panels'][6]))  # Deep copy
ftp_table['id'] = 4
ftp_table['title'] = "FTP Activity Log"
ftp_table['gridPos'] = {"h": 8, "w": 12, "x": 12, "y": 8}
ftp_table['targets'][0]['datasource']['uid'] = 'ftp-logs'
ftp_table['targets'][0]['urlPath'] = '/dionaea/ftp_parsed.json'

ftp_dashboard['panels'] = [ftp_timeline, ftp_gauge, ftp_pie, ftp_table]

with open('dashboards/ftp-attacks.json', 'w') as f:
    json.dump(ftp_dashboard, f, indent=2)
print("✓ Created minimal FTP dashboard (2 graphs, 2 tables)")

print("\n✓ All minimal dashboards created!")
print("✓ Each dashboard has: 1 timeseries graph, 1 gauge, 1 piechart, 1 table")
print("\nRestart Grafana: docker restart honeypot-grafana")
