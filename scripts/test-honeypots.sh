#!/bin/bash
# Test script to verify honeypot functionality

echo "🧪 Honeypot Test Script"
echo "======================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test SSH honeypot
echo "Testing SSH Honeypot (port 222)..."
if nc -zv localhost 222 2>&1 | grep -q "succeeded\|open"; then
    echo -e "${GREEN}✓ SSH honeypot is accessible${NC}"
    echo "  Try: ssh -p 222 root@localhost"
else
    echo -e "${RED}✗ SSH honeypot is not accessible${NC}"
fi
echo ""

# Test FTP honeypot
echo "Testing FTP Honeypot (port 211)..."
if nc -zv localhost 211 2>&1 | grep -q "succeeded\|open"; then
    echo -e "${GREEN}✓ FTP honeypot is accessible${NC}"
    echo "  Try: ftp localhost 211"
else
    echo -e "${RED}✗ FTP honeypot is not accessible${NC}"
fi
echo ""

# Test Web honeypot
echo "Testing Web Honeypot (port 80)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Web honeypot is responding (HTTP $HTTP_CODE)${NC}"
    echo "  Try: curl http://localhost"
    echo "       curl http://localhost/admin"
    echo "       curl http://localhost/.env"
else
    echo -e "${RED}✗ Web honeypot returned HTTP $HTTP_CODE${NC}"
fi
echo ""

# Test Grafana
echo "Testing Grafana Dashboard..."
GRAFANA_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)
if [[ "$GRAFANA_CODE" =~ ^(200|302)$ ]]; then
    echo -e "${GREEN}✓ Grafana is accessible (HTTP $GRAFANA_CODE)${NC}"
    echo "  URL: http://localhost:3000"
    echo "  Username: admin"
    echo "  Password: honeypot123"
else
    echo -e "${RED}✗ Grafana returned HTTP $GRAFANA_CODE${NC}"
fi
echo ""

# Test Log Server
echo "Testing Log Server..."
LOG_SERVER_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null)
if [[ "$LOG_SERVER_CODE" =~ ^(200|404)$ ]]; then
    echo -e "${GREEN}✓ Log server is responding (HTTP $LOG_SERVER_CODE)${NC}"
    echo "  URL: http://localhost:8080"
else
    echo -e "${RED}✗ Log server returned HTTP $LOG_SERVER_CODE${NC}"
fi
echo ""

# Generate test traffic
echo "🚀 Generate Test Traffic"
echo "------------------------"
echo ""
if confirm "Generate test traffic to honeypots?"; then
    echo "Generating test attacks..."
    
    # Test SSH
    echo "  Testing SSH (will fail authentication - expected)..."
    sshpass -p 'testpass' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 222 testuser@localhost exit 2>/dev/null &
    
    # Test FTP
    echo "  Testing FTP login attempts..."
    for i in {1..3}; do
        (echo "USER admin$i"; echo "PASS admin123"; echo "QUIT") | nc -w 2 localhost 211 > /dev/null 2>&1 &
    done
    
    # Test Web
    echo "  Testing Web endpoints..."
    curl -s http://localhost/ > /dev/null
    curl -s http://localhost/admin > /dev/null
    curl -s http://localhost/.env > /dev/null
    curl -s http://localhost/wp-admin/ > /dev/null
    curl -s -X POST http://localhost/login -d "username=admin&password=admin123" > /dev/null
    
    echo "  Test traffic generated!"
    echo "  Wait 30-40 seconds for FTP logs to parse, then check Grafana dashboards."
fi

echo ""
echo "✅ Testing complete!"
echo ""
echo "Check logs with: ./scripts/analyze-logs.sh"
echo ""

# Helper function
confirm() {
    read -p "$1 (yes/no): " -r
    [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]
}
