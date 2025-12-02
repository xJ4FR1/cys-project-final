#!/bin/sh
# Periodic Dionaea log parser
# Runs every 30 seconds to parse FTP logs

echo "Starting Dionaea log parser..."

while true; do
    python3 /scripts/parse-dionaea-logs.py
    sleep 30
done
