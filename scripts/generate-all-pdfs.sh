#!/usr/bin/env zsh
# Generate PDFs from all markdown documentation files
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$ROOT_DIR/docs"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "❌ pandoc is not installed. Install it with:"
  echo "  sudo apt update && sudo apt install -y pandoc texlive-latex-extra texlive-fonts-recommended"
  exit 1
fi

echo "📄 Generating PDFs from markdown documentation..."
echo ""

# Array of markdown files to convert
MD_FILES=(
  "PROJECT_NOTES.md"
  "ARCHITECTURE.md"
  "ATTACK_SIMULATION.md"
  "PRESENTATION_GUIDE.md"
  "PROJECT_SUMMARY.md"
  "QUICK_REFERENCE.md"
  "QUICK_START_CARD.md"
)

SUCCESS_COUNT=0
FAIL_COUNT=0

for md_file in "${MD_FILES[@]}"; do
  INPUT="$DOCS_DIR/$md_file"
  OUTPUT="$DOCS_DIR/${md_file%.md}.pdf"
  
  if [ ! -f "$INPUT" ]; then
    echo "⚠️  Skipping $md_file (not found)"
    continue
  fi
  
  echo "🔄 Converting $md_file..."
  
  if pandoc "$INPUT" \
    --from markdown \
    --pdf-engine=xelatex \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V toc=true \
    --toc \
    --number-sections \
    -o "$OUTPUT" 2>/dev/null; then
    echo "✅ Generated: ${OUTPUT##*/}"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  else
    echo "❌ Failed: $md_file"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
  echo ""
done

echo "================================"
echo "📊 PDF Generation Summary"
echo "================================"
echo "✅ Successful: $SUCCESS_COUNT"
echo "❌ Failed: $FAIL_COUNT"
echo ""

if [ $SUCCESS_COUNT -gt 0 ]; then
  echo "📁 PDFs saved in: $DOCS_DIR/"
  ls -lh "$DOCS_DIR"/*.pdf 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
fi

echo ""
echo "✨ Done!"
