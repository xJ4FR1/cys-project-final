#!/usr/bin/env python3
"""
Simple HTTP server that converts NDJSON log files to JSON arrays
"""
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class LogHandler(BaseHTTPRequestHandler):
    LOG_DIR = "/logs"
    
    def do_GET(self):
        # Parse the path
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        
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
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            logs.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            
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
