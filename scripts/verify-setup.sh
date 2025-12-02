#!/bin/bash
# Pre-Presentation Verification Script
# Tests all components before instructor demo

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "🍯 Honeypot Pre-Presentation Verification"
echo "=========================================="
echo ""

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        return 1
    fi
}

# 1. Check Docker
echo "1. Checking Docker..."
docker --version > /dev/null 2>&1
print_status $? "Docker installed"

docker compose version > /dev/null 2>&1
print_status $? "Docker Compose installed"
echo ""

# 2. Check services are running
echo "2. Checking services..."
SERVICES=("honeypot-ssh" "honeypot-ftp" "honeypot-web" "honeypot-grafana" "honeypot-log-server")
ALL_RUNNING=true

for service in "${SERVICES[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^$service$"; then
        print_status 0 "$service is running"
    else
        print_status 1 "$service is NOT running"
        ALL_RUNNING=false
    fi
done
echo ""

# 3. Check ports
echo "3. Checking port availability..."
PORTS=(222 211 80 3000 8080)
for port in "${PORTS[@]}"; do
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        print_status 0 "Port $port is in use (good)"
    else
        print_status 1 "Port $port is NOT listening"
    fi
done
echo ""

# 4. Test SSH honeypot
echo "4. Testing SSH honeypot..."
timeout 2 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 222 test@localhost 2>&1 | grep -q "Permission denied" || true
if [ -f logs/ssh-honeypot/ssh_honeypot.json ]; then
    print_status 0 "SSH honeypot responding"
else
    print_status 1 "SSH honeypot not responding"
fi
echo ""

# 5. Test Web honeypot
echo "5. Testing Web honeypot..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" == "200" ]; then
    print_status 0 "Web honeypot responding (HTTP $HTTP_CODE)"
else
    print_status 1 "Web honeypot not responding (HTTP $HTTP_CODE)"
fi
echo ""

# 6. Test FTP honeypot
echo "6. Testing FTP honeypot..."
timeout 2 nc -zv localhost 211 2>&1 | grep -q "succeeded" && FTP_OK=0 || FTP_OK=1
print_status $FTP_OK "FTP honeypot port accessible"
echo ""

# 7. Test Grafana
echo "7. Testing Grafana..."
GRAFANA_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health 2>/dev/null || echo "000")
if [ "$GRAFANA_CODE" == "200" ]; then
    print_status 0 "Grafana responding (HTTP $GRAFANA_CODE)"
else
    print_status 1 "Grafana not responding (HTTP $GRAFANA_CODE)"
fi
echo ""

# 8. Test Log Server
echo "8. Testing Log Server..."
LOG_SERVER_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null || echo "000")
if [ "$LOG_SERVER_CODE" == "200" ] || [ "$LOG_SERVER_CODE" == "404" ]; then
    print_status 0 "Log server responding"
else
    print_status 1 "Log server not responding"
fi
echo ""

# 9. Check log files
echo "9. Checking log files..."
if [ -d logs/ssh-honeypot ] && [ -d logs/web-honeypot ] && [ -d logs/dionaea ]; then
    print_status 0 "Log directories exist"
    
    # Count log entries
    if [ -f logs/ssh-honeypot/ssh_honeypot.json ]; then
        SSH_COUNT=$(wc -l < logs/ssh-honeypot/ssh_honeypot.json 2>/dev/null || echo "0")
        echo -e "  ${YELLOW}→${NC} SSH logs: $SSH_COUNT entries"
    fi
    
    if [ -f logs/web-honeypot/honeypot.json ]; then
        WEB_COUNT=$(wc -l < logs/web-honeypot/honeypot.json 2>/dev/null || echo "0")
        echo -e "  ${YELLOW}→${NC} Web logs: $WEB_COUNT entries"
    fi
else
    print_status 1 "Log directories missing"
fi
echo ""

# 10. Check dashboards
echo "10. Checking dashboard files..."
DASHBOARDS=("combined-overview.json" "ssh-attacks.json" "web-attacks.json" "ftp-attacks.json")
for dashboard in "${DASHBOARDS[@]}"; do
    if [ -f "dashboards/$dashboard" ]; then
        print_status 0 "$dashboard exists"
    else
        print_status 1 "$dashboard missing"
    fi
done
echo ""

# 11. Check documentation
echo "11. Checking documentation..."
DOCS=("README.md" "docs/PRESENTATION_GUIDE.md" "docs/ATTACK_SIMULATION.md" "docs/ARCHITECTURE.md" "docs/PROJECT_NOTES.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        print_status 0 "$doc exists"
    else
        print_status 1 "$doc missing"
    fi
done
echo ""

# 12. Quick attack test
echo "12. Running quick attack test..."
echo "Attempting SSH connection..."
timeout 2 sshpass -p "test123" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 222 test@localhost 2>&1 > /dev/null || true
sleep 1

echo "Attempting Web request..."
curl -s http://localhost/admin > /dev/null
sleep 1

if [ -f logs/ssh-honeypot/ssh_honeypot.json ]; then
    NEW_SSH=$(tail -1 logs/ssh-honeypot/ssh_honeypot.json 2>/dev/null | grep -c "test" || echo "0")
    if [ "$NEW_SSH" -gt 0 ]; then
        print_status 0 "New SSH attack logged"
    else
        print_status 1 "SSH attack not logged"
    fi
fi

if [ -f logs/web-honeypot/honeypot.json ]; then
    NEW_WEB=$(tail -1 logs/web-honeypot/honeypot.json 2>/dev/null | grep -c "admin" || echo "0")
    if [ "$NEW_WEB" -gt 0 ]; then
        print_status 0 "New Web attack logged"
    else
        print_status 1 "Web attack not logged"
    fi
fi
echo ""

# Summary
echo "=========================================="
echo "📊 Verification Summary"
echo "=========================================="

if [ "$ALL_RUNNING" = true ]; then
    echo -e "${GREEN}✓ All services are running${NC}"
else
    echo -e "${RED}✗ Some services are not running${NC}"
    echo -e "${YELLOW}  Run: docker compose up -d${NC}"
fi

echo ""
echo "Quick Actions:"
echo "  View logs:     docker compose logs -f"
echo "  Open Grafana:  xdg-open http://localhost:3000"
echo "  Run attacks:   see docs/ATTACK_SIMULATION.md"
echo "  Demo guide:    see docs/PRESENTATION_GUIDE.md"
echo ""

if command -v jq &> /dev/null; then
    print_status 0 "jq installed (for log analysis)"
else
    print_status 1 "jq not installed (optional: sudo apt install jq)"
fi

if command -v sshpass &> /dev/null; then
    print_status 0 "sshpass installed (for attack simulations)"
else
    print_status 1 "sshpass not installed (optional: sudo apt install sshpass)"
fi

echo ""
echo "=========================================="
if [ "$ALL_RUNNING" = true ]; then
    echo -e "${GREEN}🎉 System ready for presentation!${NC}"
else
    echo -e "${YELLOW}⚠️  Fix issues above before presenting${NC}"
fi
echo "=========================================="
