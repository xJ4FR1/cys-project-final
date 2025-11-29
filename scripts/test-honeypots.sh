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
echo "Testing SSH Honeypot (port 2222)..."
if nc -zv localhost 2222 2>&1 | grep -q "succeeded\|open"; then
    echo -e "${GREEN}✓ SSH honeypot is accessible${NC}"
    echo "  Try: ssh -p 2222 root@localhost"
else
    echo -e "${RED}✗ SSH honeypot is not accessible${NC}"
fi
echo ""

# Test FTP honeypot
echo "Testing FTP Honeypot (port 21)..."
if nc -zv localhost 21 2>&1 | grep -q "succeeded\|open"; then
    echo -e "${GREEN}✓ FTP honeypot is accessible${NC}"
    echo "  Try: ftp localhost 21"
else
    echo -e "${RED}✗ FTP honeypot is not accessible${NC}"
fi
echo ""

# Test Web honeypot
echo "Testing Web Honeypot (port 8888)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Web honeypot is responding (HTTP $HTTP_CODE)${NC}"
    echo "  Try: curl http://localhost:8888"
    echo "       curl http://localhost:8888/admin"
    echo "       curl http://localhost:8888/.env"
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

# Test Prometheus
echo "Testing Prometheus..."
PROM_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/-/healthy 2>/dev/null)
if [ "$PROM_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Prometheus is healthy${NC}"
    echo "  URL: http://localhost:9090"
else
    echo -e "${RED}✗ Prometheus health check failed${NC}"
fi
echo ""

# Test Loki
echo "Testing Loki..."
LOKI_STATUS=$(curl -s http://localhost:3100/ready 2>/dev/null)
if echo "$LOKI_STATUS" | grep -q "ready"; then
    echo -e "${GREEN}✓ Loki is ready${NC}"
    echo "  URL: http://localhost:3100"
else
    echo -e "${RED}✗ Loki is not ready${NC}"
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
    sshpass -p 'testpass' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2222 testuser@localhost exit 2>/dev/null &
    
    # Test Web
    echo "  Testing Web endpoints..."
    curl -s http://localhost:8888/ > /dev/null
    curl -s http://localhost:8888/admin > /dev/null
    curl -s http://localhost:8888/.env > /dev/null
    curl -s http://localhost:8888/wp-admin/ > /dev/null
    curl -s -X POST http://localhost:8888/login -d "username=admin&password=admin123" > /dev/null
    
    echo "  Test traffic generated!"
    echo "  Wait 30 seconds, then check Grafana dashboards."
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
