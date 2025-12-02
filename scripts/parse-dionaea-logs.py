#!/usr/bin/env python3
"""
Parse Dionaea logs and create JSON output for Grafana
"""
import json
import re
from datetime import datetime
from pathlib import Path

def parse_dionaea_log(log_file):
    """Parse dionaea.log and extract FTP events"""
    events = []
    
    if not Path(log_file).exists():
        return events
    
    # Define standard fields for all events
    def create_event(timestamp, event_type, **kwargs):
        """Create a normalized event with all possible fields"""
        event = {
            'timestamp': timestamp,
            'event_type': event_type,
            'protocol': 'ftp',
            'src_ip': kwargs.get('src_ip', None),
            'src_port': kwargs.get('src_port', None),
            'dst_port': kwargs.get('dst_port', None),
            'username': kwargs.get('username', None),
            'password': kwargs.get('password', None),
            'command': kwargs.get('command', None),
            'message': kwargs.get('message', None),
            'count': kwargs.get('count', 1)
        }
        return event
    
    # Regex patterns for different log types
    connection_pattern = r'\[(\d{2}\w{3}\d{4} \d{2}:\d{2}:\d{2})\] connection\s+(\S+)\s+(\S+)\s+(\d+)\s+<->\s+(\S+)\s+(\d+)'
    
    try:
        with open(log_file, 'r', errors='ignore') as f:
            for line in f:
                # Parse connection lines
                conn_match = re.search(connection_pattern, line)
                if conn_match and 'ftp' in line.lower():
                    timestamp_str = conn_match.group(1)
                    try:
                        # Parse timestamp like "02Dec2025 12:45:30"
                        dt = datetime.strptime(timestamp_str, '%d%b%Y %H:%M:%S')
                        timestamp = dt.isoformat()
                    except:
                        timestamp = datetime.now().isoformat()
                    
                    event = create_event(
                        timestamp=timestamp,
                        event_type='connection',
                        src_ip=conn_match.group(4),
                        src_port=int(conn_match.group(5)),
                        dst_port=int(conn_match.group(6))
                    )
                    events.append(event)
                
                # Parse FTP commands
                elif 'ftp' in line.lower() and ('USER' in line or 'PASS' in line or 'RETR' in line or 'STOR' in line):
                    # Extract timestamp
                    ts_match = re.search(r'\[(\d{2}\w{3}\d{4} \d{2}:\d{2}:\d{2})\]', line)
                    if ts_match:
                        try:
                            dt = datetime.strptime(ts_match.group(1), '%d%b%Y %H:%M:%S')
                            timestamp = dt.isoformat()
                        except:
                            timestamp = datetime.now().isoformat()
                        
                        # Extract command
                        command = None
                        for cmd in ['USER', 'PASS', 'RETR', 'STOR', 'LIST', 'CWD']:
                            if cmd in line:
                                command = cmd
                                break
                        
                        if command:
                            event = create_event(
                                timestamp=timestamp,
                                event_type='ftp_command',
                                command=command
                            )
                            events.append(event)
    
    except Exception as e:
        print(f"Error parsing log: {e}")
    
    # If no events found, create a dummy event to prevent dashboard errors
    if not events:
        events.append(create_event(
            timestamp=datetime.now().isoformat(),
            event_type='no_activity',
            message='No FTP activity detected yet',
            count=0
        ))
    
    return events

if __name__ == '__main__':
    log_file = '/opt/dionaea/var/log/dionaea/dionaea.log'
    output_file = '/logs/dionaea/ftp_parsed.json'
    
    # Parse logs
    events = parse_dionaea_log(log_file)
    
    # Write as NDJSON (newline-delimited JSON)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    
    print(f"Parsed {len(events)} FTP events")
