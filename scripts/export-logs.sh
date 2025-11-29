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

# Export from Loki (if available)
if command -v curl &> /dev/null; then
    echo "📥 Exporting from Loki..."
    
    # Export Cowrie logs
    curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
        --data-urlencode 'query={job="cowrie"}' \
        --data-urlencode 'start='$(date -d '7 days ago' +%s)'000000000' \
        --data-urlencode 'end='$(date +%s)'000000000' \
        > "$EXPORT_DIR/cowrie_loki_export.json" 2>/dev/null
    
    # Export Dionaea logs
    curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
        --data-urlencode 'query={job="dionaea"}' \
        --data-urlencode 'start='$(date -d '7 days ago' +%s)'000000000' \
        --data-urlencode 'end='$(date +%s)'000000000' \
        > "$EXPORT_DIR/dionaea_loki_export.json" 2>/dev/null
    
    # Export Web logs
    curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
        --data-urlencode 'query={job="web-honeypot"}' \
        --data-urlencode 'start='$(date -d '7 days ago' +%s)'000000000' \
        --data-urlencode 'end='$(date +%s)'000000000' \
        > "$EXPORT_DIR/web_loki_export.json" 2>/dev/null
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
