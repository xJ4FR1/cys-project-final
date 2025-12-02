#!/usr/bin/env python3
import json

# Load existing dashboards to get panel structures
with open('dashboards/ssh-attacks.json', 'r') as f:
    ssh_dash = json.load(f)
with open('dashboards/web-attacks.json', 'r') as f:
    web_dash = json.load(f)
with open('dashboards/ftp-attacks.json', 'r') as f:
    ftp_dash = json.load(f)

# Create combined overview dashboard
overview = {
    "annotations": ssh_dash["annotations"],
    "editable": True,
    "gnetId": None,
    "graphTooltip": 0,
    "id": None,
    "links": [],
    "panels": [],
    "schemaVersion": 27,
    "style": "dark",
    "tags": ["honeypot", "overview"],
    "templating": {"list": []},
    "time": {"from": "now-6h", "to": "now"},
    "timepicker": {},
    "timezone": "",
    "title": "Honeypot Overview",
    "uid": "honeypot-overview",
    "version": 0
}

# Row 1: Timeseries graphs (all 3 honeypots)
ssh_ts = json.loads(json.dumps(ssh_dash['panels'][0]))  # SSH timeseries
ssh_ts['gridPos'] = {"h": 8, "w": 8, "x": 0, "y": 0}
ssh_ts['title'] = "SSH Events"

web_ts = json.loads(json.dumps(web_dash['panels'][0]))  # Web timeseries
web_ts['gridPos'] = {"h": 8, "w": 8, "x": 8, "y": 0}
web_ts['title'] = "Web Requests"

ftp_ts = json.loads(json.dumps(ftp_dash['panels'][0]))  # FTP timeseries
ftp_ts['gridPos'] = {"h": 8, "w": 8, "x": 16, "y": 0}
ftp_ts['title'] = "FTP Events"

# Row 2: Gauges (all 3 honeypots)
ssh_gauge = json.loads(json.dumps(ssh_dash['panels'][1]))  # SSH gauge
ssh_gauge['gridPos'] = {"h": 6, "w": 8, "x": 0, "y": 8}
ssh_gauge['title'] = "Total SSH"

web_gauge = json.loads(json.dumps(web_dash['panels'][1]))  # Web gauge
web_gauge['gridPos'] = {"h": 6, "w": 8, "x": 8, "y": 8}
web_gauge['title'] = "Total Web"

ftp_gauge = json.loads(json.dumps(ftp_dash['panels'][1]))  # FTP gauge
ftp_gauge['gridPos'] = {"h": 6, "w": 8, "x": 16, "y": 8}
ftp_gauge['title'] = "Total FTP"

# Row 3: Tables (2 tables - SSH and Web only, skip FTP)
ssh_table = json.loads(json.dumps(ssh_dash['panels'][3]))  # SSH table
ssh_table['gridPos'] = {"h": 10, "w": 12, "x": 0, "y": 14}
ssh_table['title'] = "Recent SSH Attacks"

web_table = json.loads(json.dumps(web_dash['panels'][3]))  # Web table
web_table['gridPos'] = {"h": 10, "w": 12, "x": 12, "y": 14}
web_table['title'] = "Recent Web Requests"

overview['panels'] = [
    ssh_ts, web_ts, ftp_ts,  # 3 timeseries graphs
    ssh_gauge, web_gauge, ftp_gauge,  # 3 gauges
    ssh_table, web_table  # 2 tables
]

with open('dashboards/overview.json', 'w') as f:
    json.dump(overview, f, indent=2)

print("✓ Created combined overview dashboard")
print("  - 3 timeseries graphs (SSH, Web, FTP)")
print("  - 3 gauges (SSH, Web, FTP)")
print("  - 2 tables (SSH, Web)")

# Fix FTP dashboard table - remove username/password columns
ftp_table_panel = ftp_dash['panels'][3]  # Table panel
ftp_table_panel['targets'][0]['fields'] = [
    {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
    {"jsonPath": "$[*].event_type", "name": "Event Type"},
    {"jsonPath": "$[*].component", "name": "Component"},
    {"jsonPath": "$[*].command", "name": "Command"}
]

with open('dashboards/ftp-attacks.json', 'w') as f:
    json.dump(ftp_dash, f, indent=2)

print("✓ Fixed FTP dashboard table (removed username/password columns)")
