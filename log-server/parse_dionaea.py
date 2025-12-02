#!/usr/bin/env python3
"""
Dionaea FTP Log Parser
Converts Dionaea text logs to JSON format for Grafana visualization
"""
import re
import json
from datetime import datetime
import os
from collections import defaultdict

LOG_FILE = "/logs/dionaea/dionaea/dionaea.log"
OUTPUT_FILE = "/app/ftp_parsed.json"  # Write to app directory (writable)

def parse_dionaea_log_line(line):
    """Parse a single Dionaea log line and extract relevant information"""
    try:
        # Example log format: [02122025 11:53:15] ftp /dionaea/ftp.py:214-debug: b'USER anonymous\r\n'
        
        # Extract timestamp
        timestamp_match = re.search(r'\[(\d{8})\s+(\d{2}:\d{2}:\d{2})\]', line)
        if not timestamp_match:
            return None
        
        date_str = timestamp_match.group(1)
        time_str = timestamp_match.group(2)
        
        # Parse date: MMDDYYYY format
        month = date_str[0:2]
        day = date_str[2:4]
        year = date_str[4:8]
        timestamp = f"{year}-{month}-{day}T{time_str}Z"
        
        # Extract component and message
        component_match = re.search(r'\]\s+(\w+)\s+', line)
        component = component_match.group(1) if component_match else "unknown"
        
        # Check for FTP-specific events
        event_type = "unknown"
        username = None
        password = None
        command = None
        connection_id = None
        src_ip = None
        
        # Extract connection information
        con_match = re.search(r'con\s+(0x[0-9a-f]+)', line)
        if con_match:
            connection_id = con_match.group(1)
        
        # Extract IP address if present
        ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if ip_match:
            src_ip = ip_match.group(1)
        
        if 'ftp' in line.lower():
            event_type = "ftp_activity"
            
            # Extract FTP commands
            if 'USER' in line:
                user_match = re.search(r"USER\s+([^\r\n'\"]+)", line)
                if user_match:
                    username = user_match.group(1).strip()
                    event_type = "ftp_login_attempt"
                    command = "USER"
            
            elif 'PASS' in line:
                pass_match = re.search(r"PASS\s+([^\r\n'\"]+)", line)
                if pass_match:
                    password = pass_match.group(1).strip()
                    event_type = "ftp_login_attempt"
                    command = "PASS"
            
            elif any(cmd in line for cmd in ['LIST', 'RETR', 'STOR', 'DELE', 'MKD', 'RMD']):
                for cmd in ['LIST', 'RETR', 'STOR', 'DELE', 'MKD', 'RMD', 'CWD', 'PWD', 'SYST', 'QUIT']:
                    if cmd in line:
                        command = cmd
                        event_type = "ftp_command"
                        break
        
        elif 'connection' in line.lower():
            if 'accept' in line.lower():
                event_type = "connection_accept"
            elif 'close' in line.lower() or 'disconnect' in line.lower():
                event_type = "connection_close"
            else:
                event_type = "connection"
        
        # Build JSON entry
        entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "component": component,
            "connection_id": connection_id,
            "src_ip": src_ip,
            "raw_message": line.strip()
        }
        
        if username:
            entry["username"] = username
        if password:
            entry["password"] = password
        if command:
            entry["command"] = command
        
        return entry
        
    except Exception as e:
        return None

def parse_dionaea_logs():
    """Parse Dionaea logs and convert to JSON"""
    
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found: {LOG_FILE}")
        return []
    
    entries = []
    connection_map = defaultdict(dict)
    
    print(f"Parsing {LOG_FILE}...")
    
    with open(LOG_FILE, 'r', errors='ignore') as f:
        for line in f:
            # Only process lines with relevant information
            if any(keyword in line.lower() for keyword in ['ftp', 'connection', 'user', 'pass']):
                entry = parse_dionaea_log_line(line)
                if entry and entry['event_type'] != 'unknown':
                    # Track connections to correlate username/password
                    conn_id = entry.get('connection_id')
                    if conn_id:
                        if 'username' in entry:
                            connection_map[conn_id]['username'] = entry['username']
                        if 'password' in entry:
                            connection_map[conn_id]['password'] = entry['password']
                        
                        # Add correlated data
                        entry['username'] = connection_map[conn_id].get('username')
                        entry['password'] = connection_map[conn_id].get('password')
                    
                    entries.append(entry)
    
    print(f"Parsed {len(entries)} FTP-related log entries")
    return entries

def save_json_logs(entries):
    """Save parsed entries as JSON (newline-delimited)"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')
    
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    entries = parse_dionaea_logs()
    if entries:
        save_json_logs(entries)
        print(f"\nSample entry:")
        print(json.dumps(entries[0], indent=2))
    else:
        print("No FTP entries found in logs")
