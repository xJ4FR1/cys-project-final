#!/usr/bin/env zsh
# Legacy script - redirects to generate-all-pdfs.sh
# This script is kept for backward compatibility

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "ℹ️  This script has been replaced by generate-all-pdfs.sh"
echo "🔄 Running the new script..."
echo ""

exec "$SCRIPT_DIR/generate-all-pdfs.sh"
