#!/usr/bin/env python3
import json
import sys
from collections import OrderedDict

def create_target(datasource_uid, url_path, fields):
    """Create a target with the exact field order from working dashboard"""
    return {
        "cacheDurationSeconds": 30,
        "datasource": {
            "type": "marcusolsson-json-datasource",
            "uid": datasource_uid
        },
        "fields": fields,
        "method": "GET",
        "queryParams": "",
        "refId": "A",
        "urlPath": url_path
    }

def fix_ssh_dashboard():
    with open('dashboards/ssh-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Update all panels with proper target structure
    # Panel 0: Total SSH Attacks
    dashboard['panels'][0]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event"}
    ])
    
    # Panel 1: Unique Attacker IPs
    dashboard['panels'][1]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "IP"}
    ])
    
    # Panel 2: Unique Usernames
    dashboard['panels'][2]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username"}
    ])
    
    # Panel 3: Unique Passwords
    dashboard['panels'][3]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].password", "name": "Password"}
    ])
    
    # Panel 4: Recent Login Attempts (table)
    dashboard['panels'][4]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP"},
        {"jsonPath": "$[*].username", "name": "Username"},
        {"jsonPath": "$[*].password", "name": "Password"}
    ])
    
    # Panel 5: Commands Executed (table)
    dashboard['panels'][5]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].command", "name": "Command"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP"}
    ])
    
    # Panel 6: Top Usernames (piechart)
    dashboard['panels'][6]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username"}
    ])
    
    # Panel 7: Top Passwords (piechart)
    dashboard['panels'][7]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].password", "name": "Password"}
    ])
    
    # Panel 8: Top Attacker IPs (piechart)
    dashboard['panels'][8]['targets'][0] = create_target("ssh-logs", "/ssh-honeypot/ssh_honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP"}
    ])
    
    with open('dashboards/ssh-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed SSH attacks dashboard")

def fix_web_dashboard():
    with open('dashboards/web-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Panel 0: Total HTTP Requests
    dashboard['panels'][0]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path"}
    ])
    
    # Panel 1: Unique Attacker IPs
    dashboard['panels'][1]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "IP"}
    ])
    
    # Panel 2: Unique Paths
    dashboard['panels'][2]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path"}
    ])
    
    # Panel 3: Unique User Agents
    dashboard['panels'][3]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].user_agent", "name": "User Agent"}
    ])
    
    # Panel 4: Recent HTTP Requests (table)
    dashboard['panels'][4]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP"},
        {"jsonPath": "$[*].method", "name": "Method"},
        {"jsonPath": "$[*].path", "name": "Path"},
        {"jsonPath": "$[*].user_agent", "name": "User Agent"}
    ])
    
    # Panel 5: Top Paths (barchart)
    dashboard['panels'][5]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].path", "name": "Path"}
    ])
    
    # Panel 6: HTTP Methods (barchart)
    dashboard['panels'][6]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].method", "name": "Method"}
    ])
    
    # Panel 7: Login Attempts (table)
    dashboard['panels'][7]['targets'][0] = create_target("web-logs", "/web-honeypot/honeypot.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].src_ip", "name": "Source IP"},
        {"jsonPath": "$[*].username", "name": "Username"},
        {"jsonPath": "$[*].password", "name": "Password"}
    ])
    
    with open('dashboards/web-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed Web attacks dashboard")

def fix_ftp_dashboard():
    with open('dashboards/ftp-attacks.json', 'r') as f:
        dashboard = json.load(f)
    
    # Panel 0: Total FTP Events
    dashboard['panels'][0]['targets'][0] = create_target("ftp-logs", "/dionaea/ftp_parsed.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event"}
    ])
    
    # Panel 1: Event Types (piechart)
    dashboard['panels'][1]['targets'][0] = create_target("ftp-logs", "/dionaea/ftp_parsed.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].event_type", "name": "Event Type"}
    ])
    
    # Panel 2: Login Attempts (table)
    dashboard['panels'][2]['targets'][0] = create_target("ftp-logs", "/dionaea/ftp_parsed.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].username", "name": "Username"},
        {"jsonPath": "$[*].password", "name": "Password"}
    ])
    
    # Panel 3: Commands Over Time (timeseries)
    dashboard['panels'][3]['targets'][0] = create_target("ftp-logs", "/dionaea/ftp_parsed.json", [
        {"jsonPath": "$[*].timestamp", "name": "Time", "type": "time"},
        {"jsonPath": "$[*].command", "name": "Command"}
    ])
    
    with open('dashboards/ftp-attacks.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    print("✓ Fixed FTP attacks dashboard")

if __name__ == '__main__':
    try:
        fix_ssh_dashboard()
        fix_web_dashboard()
        fix_ftp_dashboard()
        print("\n✓ All dashboards fixed with correct structure!")
        print("Restart Grafana: docker restart honeypot-grafana")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
