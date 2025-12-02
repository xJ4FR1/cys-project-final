#!/bin/bash
# Export and archive honeypot logs

EXPORT_DIR="exports/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EXPORT_DIR"

echo "📦 Exporting Honeypot Logs"
echo "=========================="
echo ""
echo "Export directory: $EXPORT_DIR"
echo ""

# Copy all logs
echo "📋 Copying log files..."
cp -r logs/* "$EXPORT_DIR/" 2>/dev/null

# Generate statistics for export
if command -v jq &> /dev/null; then
    echo "📊 Generating statistics..."
    
    # SSH statistics
    if [ -f "logs/ssh-honeypot/ssh_honeypot.json" ]; then
        echo "  SSH honeypot statistics..."
        cat logs/ssh-honeypot/ssh_honeypot.json | jq -s '{
            total_events: length,
            unique_ips: [.[].src_ip] | unique | length,
            unique_usernames: [.[].username] | unique | length,
            top_ips: ([.[].src_ip] | group_by(.) | map({ip: .[0], count: length}) | sort_by(.count) | reverse | .[0:5])
        }' > "$EXPORT_DIR/ssh_statistics.json" 2>/dev/null || true
    fi
    
    # Web statistics
    if [ -f "logs/web-honeypot/honeypot.json" ]; then
        echo "  Web honeypot statistics..."
        cat logs/web-honeypot/honeypot.json | jq -s '{
            total_requests: length,
            unique_ips: [.[].remote_addr] | unique | length,
            unique_paths: [.[].path] | unique | length,
            top_paths: ([.[].path] | group_by(.) | map({path: .[0], count: length}) | sort_by(.count) | reverse | .[0:5])
        }' > "$EXPORT_DIR/web_statistics.json" 2>/dev/null || true
    fi
fi

# Create summary report
echo "📊 Generating summary report..."
cat > "$EXPORT_DIR/SUMMARY.txt" << EOF
Honeypot Log Export Summary
===========================
Export Date: $(date)
Export Directory: $EXPORT_DIR

File Count:
$(find "$EXPORT_DIR" -type f | wc -l) files

Total Size:
$(du -sh "$EXPORT_DIR" | cut -f1)

Contents:
$(ls -lh "$EXPORT_DIR")
EOF

# Compress the export
echo "🗜️  Compressing archive..."
ARCHIVE_NAME="honeypot_logs_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$ARCHIVE_NAME" -C exports "$(basename $EXPORT_DIR)"

echo ""
echo "✅ Export complete!"
echo ""
echo "Archive: $ARCHIVE_NAME"
echo "Size: $(du -sh "$ARCHIVE_NAME" | cut -f1)"
echo ""
echo "To extract: tar -xzf $ARCHIVE_NAME"
echo ""
