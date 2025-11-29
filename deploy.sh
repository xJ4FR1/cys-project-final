#!/bin/bash
# Honeypot Deployment Script
# Automates the setup and deployment of the honeypot stack

set -e

echo "🍯 Honeypot Deployment Script"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
echo -e "${GREEN}✓ Docker Compose found: $(docker compose version)${NC}"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Running as root. This is not recommended.${NC}"
    echo ""
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs/{cowrie,heralding,web-honeypot}
mkdir -p data/{cowrie/{etc,var},heralding,loki,prometheus,grafana}
chmod -R 755 logs data

# Security warnings
echo ""
echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║                  SECURITY WARNING                          ║${NC}"
echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}⚠️  This honeypot deployment will expose vulnerable services.${NC}"
echo -e "${YELLOW}⚠️  DO NOT expose these ports directly to the internet.${NC}"
echo -e "${YELLOW}⚠️  Use proper network segmentation (DMZ, VLAN, etc.).${NC}"
echo -e "${YELLOW}⚠️  Implement firewall rules to restrict access.${NC}"
echo ""
read -p "Do you understand the risks and want to continue? (yes/no): " -r
echo ""
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Check for port conflicts
echo "🔍 Checking for port conflicts..."
PORTS=(2222 2223 21 8080 25 23 110 5432 3306 8888 3000 9090 3100)
CONFLICTS=0

for PORT in "${PORTS[@]}"; do
    if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
        echo -e "${RED}❌ Port $PORT is already in use${NC}"
        CONFLICTS=$((CONFLICTS + 1))
    fi
done

if [ $CONFLICTS -gt 0 ]; then
    echo -e "${RED}Found $CONFLICTS port conflict(s). Please stop conflicting services or modify docker-compose.yml${NC}"
    read -p "Continue anyway? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✓ Port check complete${NC}"
echo ""

# Pull Docker images
echo "📥 Pulling Docker images..."
docker compose pull

# Build custom web honeypot
echo "🔨 Building web honeypot..."
docker compose build web-honeypot

# Start services
echo "🚀 Starting honeypot stack..."
docker compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."
docker compose ps

# Test endpoints
echo ""
echo "🧪 Testing endpoints..."

# Test Grafana
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|302"; then
    echo -e "${GREEN}✓ Grafana is running (http://localhost:3000)${NC}"
else
    echo -e "${RED}❌ Grafana is not responding${NC}"
fi

# Test Prometheus
if curl -s -o /dev/null -w "%{http_code}" http://localhost:9090 | grep -q "200"; then
    echo -e "${GREEN}✓ Prometheus is running (http://localhost:9090)${NC}"
else
    echo -e "${RED}❌ Prometheus is not responding${NC}"
fi

# Test Loki
if curl -s http://localhost:3100/ready | grep -q "ready"; then
    echo -e "${GREEN}✓ Loki is running (http://localhost:3100)${NC}"
else
    echo -e "${RED}❌ Loki is not responding${NC}"
fi

# Test Web Honeypot
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8888 | grep -q "200"; then
    echo -e "${GREEN}✓ Web Honeypot is running (http://localhost:8888)${NC}"
else
    echo -e "${RED}❌ Web Honeypot is not responding${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            🎉 Deployment Complete!                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📊 Access Grafana Dashboard:"
echo -e "   URL: ${BLUE}http://localhost:3000${NC}"
echo -e "   Username: ${YELLOW}admin${NC}"
echo -e "   Password: ${YELLOW}honeypot123${NC}"
echo ""
echo "🍯 Honeypot Ports:"
echo "   SSH (Cowrie):        2222, 2223"
echo "   FTP (Heralding):     21"
echo "   HTTP (Heralding):    8080"
echo "   Web Honeypot:        8888"
echo "   SMTP:                25"
echo "   Telnet:              23"
echo "   POP3:                110"
echo "   PostgreSQL:          5432"
echo "   MySQL:               3306"
echo ""
echo "📈 Monitoring:"
echo "   Grafana:             http://localhost:3000"
echo "   Prometheus:          http://localhost:9090"
echo "   Loki:                http://localhost:3100"
echo ""
echo "📝 Useful commands:"
echo "   View logs:           docker compose logs -f"
echo "   Stop services:       docker compose down"
echo "   Restart services:    docker compose restart"
echo "   Check status:        docker compose ps"
echo ""
echo -e "${YELLOW}⚠️  Remember to change the default Grafana password!${NC}"
echo ""
