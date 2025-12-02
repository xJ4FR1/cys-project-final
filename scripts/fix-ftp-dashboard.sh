#!/bin/bash
# Clean up stale dashboard data and restart services

echo "Cleaning up FTP dashboard data..."
rm -f logs/dionaea/ftp_parsed.json

echo "Restarting services..."
docker compose restart dionaea-parser
docker compose restart log-server  
docker compose restart grafana

echo "Waiting for services to stabilize..."
sleep 10

echo "✓ Cleanup complete. FTP dashboard should now work correctly."
echo "  Access Grafana at http://localhost:3000"
