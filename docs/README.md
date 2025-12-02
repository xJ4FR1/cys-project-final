# Documentation Index

All project documentation is organized here in both Markdown (.md) and PDF (.pdf) formats.

---

## 📚 Available Documents

### 1. **PROJECT_SUMMARY.md** / **PROJECT_SUMMARY.pdf**
**Start here!** Complete project overview, status, and quick start guide.
- What's included
- Changes made for presentation
- Quick start commands
- File structure
- Testing checklist

### 2. **QUICK_START_CARD.md** / **QUICK_START_CARD.pdf**
**Use during presentation!** One-page reference card with all demo commands.
- Pre-demo checklist
- Copy-paste commands for SSH, Web, FTP attacks
- Grafana dashboard navigation
- Expected questions & answers
- Troubleshooting quick fixes

### 3. **PRESENTATION_GUIDE.md** / **PRESENTATION_GUIDE.pdf**
**For instructor demo!** Comprehensive 15-minute presentation script.
- Step-by-step demonstration flow
- Talking points for each section
- Live demo commands
- FAQ with detailed answers
- Backup demo plan
- Grading criteria alignment

### 4. **ATTACK_SIMULATION.md** / **ATTACK_SIMULATION.pdf**
**For testing!** Complete attack command reference.
- SSH attack scenarios (manual & automated)
- Web attack patterns (reconnaissance, SQL injection, XSS)
- FTP attack methods
- Automated attack scripts
- Log verification commands
- Real-world attack simulations

### 5. **ARCHITECTURE.md** / **ARCHITECTURE.pdf**
**For understanding!** System architecture with ASCII diagrams.
- Simplified architecture diagram
- Data flow visualization
- Before/After comparison
- Container details
- Network configuration

### 6. **QUICK_REFERENCE.md** / **QUICK_REFERENCE.pdf**
**Command cheat sheet!** Quick command reference.
- Service ports
- Docker commands
- Log locations
- Testing commands
- Analysis with jq

### 7. **PROJECT_NOTES.md** / **PROJECT_NOTES.pdf**
**Detailed technical documentation!** Comprehensive project notes.
- Implementation details
- Deployment & operations
- Logging & analysis
- Security considerations
- Q&A section
- Troubleshooting
- Glossary

---

## 🎯 Recommended Reading Order

### For Presentation Preparation:
1. PROJECT_SUMMARY.md - Understand the project
2. QUICK_START_CARD.md - Memorize demo commands
3. PRESENTATION_GUIDE.md - Practice the script
4. ATTACK_SIMULATION.md - Test all attacks

### For Instructor Review:
1. README.md (in root directory) - Project overview
2. ARCHITECTURE.md - System design
3. PROJECT_SUMMARY.md - Complete details
4. ATTACK_SIMULATION.md - Testing capabilities

### For Technical Deep Dive:
1. PROJECT_NOTES.md - Detailed documentation
2. ARCHITECTURE.md - System architecture
3. Source code files (ssh-honeypot/ssh_honeypot.py, web-honeypot/app.py)

---

## 📄 Viewing the Documents

### Markdown Files (.md)
- View in any text editor
- Preview in VS Code, GitHub, or Markdown viewers
- Easy to edit and update

### PDF Files (.pdf)
- View in any PDF reader
- Print for offline reference
- Share with instructor
- Professional formatting with table of contents

---

## 🔄 Regenerating PDFs

If you make changes to the Markdown files and need to regenerate the PDFs:

```bash
# From project root
./scripts/generate-all-pdfs.sh

# Or from scripts directory
cd scripts
./generate-all-pdfs.sh
```

This will regenerate all PDFs with:
- Table of contents
- Section numbering
- Professional formatting
- Consistent styling

---

## 📊 Documentation Statistics

- **Total Documents**: 7
- **Total Pages**: ~100+ pages (combined PDFs)
- **Total Size**: ~600KB (PDFs)
- **Formats**: Markdown + PDF

---

## 🎓 For Presentation Day

**Print or have open:**
1. QUICK_START_CARD.pdf - Keep visible during demo
2. PRESENTATION_GUIDE.pdf - Reference for talking points
3. PROJECT_SUMMARY.pdf - For questions from instructor

**On screen:**
1. README.md - Project overview
2. Terminal windows with logs
3. Grafana dashboards in browser

---

## 📞 Quick File Purposes

| File | Purpose | When to Use |
|------|---------|-------------|
| PROJECT_SUMMARY | Complete overview | Before presentation |
| QUICK_START_CARD | Demo commands | During presentation |
| PRESENTATION_GUIDE | Full script | Practice & reference |
| ATTACK_SIMULATION | All attack commands | Testing & demo |
| ARCHITECTURE | System diagrams | Explaining design |
| QUICK_REFERENCE | Command cheat sheet | Quick lookups |
| PROJECT_NOTES | Technical details | Deep understanding |

---

## ✨ All documentation is ready for your presentation!

Choose the format that works best for you:
- **Markdown (.md)** - Easy to read and edit
- **PDF (.pdf)** - Professional format for printing/sharing
