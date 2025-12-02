#!/usr/bin/env python3
"""
Simple HTTP server that converts NDJSON log files to JSON arrays
Also parses Dionaea text logs on-demand
"""
import os
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class LogHandler(BaseHTTPRequestHandler):
    LOG_DIR = "/logs"
    
    def do_GET(self):
        # Parse the path
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        
        # Special handling for Dionaea FTP logs
        if path == 'dionaea/ftp_parsed.json':
            # Parse Dionaea logs on-demand and serve from app directory
            try:
                subprocess.run(['python3', '/app/parse_dionaea.py'], check=True, capture_output=True)
                file_path = '/app/ftp_parsed.json'
            except:
                self.send_error(500, "Failed to parse Dionaea logs")
                return
        else:
            # Build full file path
            file_path = os.path.join(self.LOG_DIR, path)
            
            # Check if file exists and is a JSON file
            if not os.path.exists(file_path):
                self.send_error(404, "File not found")
                return
        
        if not file_path.endswith('.json'):
            self.send_error(400, "Only JSON files are supported")
            return
        
        try:
            # Read NDJSON file and convert to JSON array
            logs = []
            all_keys = set()
            raw_logs = []
            
            # First pass: collect all unique keys
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            all_keys.update(log_entry.keys())
                            raw_logs.append((i, log_entry))
                        except json.JSONDecodeError:
                            continue
            
            # Second pass: normalize all entries to have the same keys
            for i, log_entry in raw_logs:
                # Add missing keys with None values
                for key in all_keys:
                    if key not in log_entry:
                        log_entry[key] = None
                
                # Add visualization fields
                log_entry['count'] = 1
                log_entry['id'] = i
                logs.append(log_entry)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            # Write JSON array
            self.wfile.write(json.dumps(logs).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), LogHandler)
    print("Log server running on port 8080")
    server.serve_forever()
