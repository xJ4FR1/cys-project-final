#!/usr/bin/env python3
import json
import sys

def fix_target_order(target):
    """Reorder target properties to match working dashboard"""
    ordered = {
        "cacheDurationSeconds": 30,
        "datasource": target.get("datasource"),
        "fields": target.get("fields", []),
        "method": "GET",
        "queryParams": "",
        "refId": target.get("refId", "A"),
        "urlPath": target.get("urlPath")
    }
    return ordered

def fix_ssh_dashboard():
    with open('dashboards/ssh-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Panel 2: Total SSH Attacks (stat - count all events)
    dashboard['panels'][0]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event", "type": "string"}
    ]
    dashboard['panels'][0]['targets'][0] = fix_target_order(dashboard['panels'][0]['targets'][0])
    
    # Panel 3: Unique Attacker IPs (stat)
    dashboard['panels'][1]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "IP", "type": "string"}
    ]
    
    # Panel 4: Unique Usernames (stat)
    dashboard['panels'][2]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username", "type": "string"}
    ]
    
    # Panel 5: Unique Passwords (stat)
    dashboard['panels'][3]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].password", "name": "Password", "type": "string"}
    ]
    
    # Panel 6: Recent Login Attempts (table)
    dashboard['panels'][4]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP", "type": "string"},
        {"jsonPath": "$[*].username", "name": "Username", "type": "string"},
        {"jsonPath": "$[*].password", "name": "Password", "type": "string"}
    ]
    
    # Panel 7: Commands Executed (table) - filter for command events
    dashboard['panels'][5]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].command", "name": "Command", "type": "string"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP", "type": "string"}
    ]
    
    # Panel 8: Top Usernames (piechart)
    dashboard['panels'][6]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username", "type": "string"}
    ]
    
    # Panel 9: Top Passwords (piechart)
    dashboard['panels'][7]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].password", "name": "Password", "type": "string"}
    ]
    
    # Panel 10: Top Attacker IPs (piechart)
    dashboard['panels'][8]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP", "type": "string"}
    ]
    
    with open('dashboards/ssh-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed SSH attacks dashboard")

def fix_web_dashboard():
    with open('dashboards/web-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Panel 2: Total HTTP Requests (stat)
    dashboard['panels'][0]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path", "type": "string"}
    ]
    
    # Panel 3: Unique Attacker IPs (stat)
    dashboard['panels'][1]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "IP", "type": "string"}
    ]
    
    # Panel 4: Unique Paths (stat)
    dashboard['panels'][2]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path", "type": "string"}
    ]
    
    # Panel 5: Unique User Agents (stat)
    dashboard['panels'][3]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].user_agent", "name": "User Agent", "type": "string"}
    ]
    
    # Panel 6: Recent HTTP Requests (table)
    dashboard['panels'][4]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP", "type": "string"},
        {"jsonPath": "$[*].method", "name": "Method", "type": "string"},
        {"jsonPath": "$[*].path", "name": "Path", "type": "string"},
        {"jsonPath": "$[*].user_agent", "name": "User Agent", "type": "string"}
    ]
    
    # Panel 7: Top Paths (barchart)
    dashboard['panels'][5]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path", "type": "string"}
    ]
    
    # Panel 8: HTTP Methods (barchart)
    dashboard['panels'][6]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].method", "name": "Method", "type": "string"}
    ]
    
    # Panel 9: Login Attempts (table)
    dashboard['panels'][7]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP", "type": "string"},
        {"jsonPath": "$[*].username", "name": "Username", "type": "string"},
        {"jsonPath": "$[*].password", "name": "Password", "type": "string"}
    ]
    
    with open('dashboards/web-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed Web attacks dashboard")

def fix_ftp_dashboard():
    with open('dashboards/ftp-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Panel 2: Total FTP Events (stat)
    dashboard['panels'][0]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event", "type": "string"}
    ]
    
    # Panel 3: Event Types (piechart)
    dashboard['panels'][1]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event Type", "type": "string"}
    ]
    
    # Panel 4: Login Attempts (table)
    dashboard['panels'][2]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username", "type": "string"},
        {"jsonPath": "$[*].password", "name": "Password", "type": "string"}
    ]
    
    # Panel 5: Commands Over Time (timeseries)
    dashboard['panels'][3]['targets'][0]['fields'] = [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].command", "name": "Command", "type": "string"}
    ]
    
    with open('dashboards/ftp-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed FTP attacks dashboard")

if __name__ == '__main__':
    try:
        fix_ssh_dashboard()
        fix_web_dashboard()
        fix_ftp_dashboard()
        print("\n✓ All dashboards fixed with correct JSON paths!")
        print("Restart Grafana to load the changes: docker restart honeypot-grafana")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
