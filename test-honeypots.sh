#!/bin/bash
# Test script for honeypot services

echo "🧪 Testing Honeypot Services"
echo "=============================="
echo ""

# Test SSH Honeypot (Port 222)
echo "📡 Testing SSH Honeypot (Port 222)..."
echo "Sending 10 SSH login attempts..."
for i in {1..10}; do
    sshpass -p "admin123" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 222 admin@localhost exit 2>/dev/null &
    sshpass -p "password" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 222 root@localhost exit 2>/dev/null &
    sshpass -p "123456" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 222 test@localhost exit 2>/dev/null &
done
sleep 2
echo "✅ SSH tests sent"
echo ""

# Test FTP Honeypot (Port 211)
echo "📁 Testing FTP Honeypot (Port 211)..."
echo "Sending FTP connection attempts..."
for i in {1..5}; do
    curl -s --connect-timeout 2 ftp://anonymous:test@localhost:211/ 2>/dev/null &
    curl -s --connect-timeout 2 ftp://admin:admin@localhost:211/ 2>/dev/null &
done
sleep 2
echo "✅ FTP tests sent"
echo ""

# Test Web Honeypot (Port 80)
echo "🌐 Testing Web Honeypot (Port 80)..."
echo "Sending web requests..."

# GET requests
for i in {1..5}; do
    curl -s http://localhost/ > /dev/null 2>&1
    curl -s http://localhost/admin > /dev/null 2>&1
    curl -s http://localhost/.env > /dev/null 2>&1
    curl -s "http://localhost/admin?id=1' OR '1'='1" > /dev/null 2>&1
done

# POST login attempts
for i in {1..5}; do
    curl -s -X POST http://localhost/login -d "username=admin&password=admin123" > /dev/null 2>&1
    curl -s -X POST http://localhost/login -d "username=root&password=toor" > /dev/null 2>&1
    curl -s -X POST http://localhost/login -d "username=test&password=test123" > /dev/null 2>&1
done

echo "✅ Web tests sent"
echo ""

# Check logs
echo "📊 Checking generated logs..."
echo ""
echo "SSH Honeypot logs:"
if [ -f logs/ssh-honeypot/ssh_honeypot.json ]; then
    wc -l logs/ssh-honeypot/ssh_honeypot.json
    echo "Last 3 SSH attacks:"
    tail -3 logs/ssh-honeypot/ssh_honeypot.json | jq -r '.username + " @ " + .src_ip' 2>/dev/null || tail -3 logs/ssh-honeypot/ssh_honeypot.json
else
    echo "⚠️  No SSH logs found yet"
fi
echo ""

echo "Web Honeypot logs:"
if [ -f logs/web-honeypot/honeypot.json ]; then
    wc -l logs/web-honeypot/honeypot.json
    echo "Last 3 web requests:"
    tail -3 logs/web-honeypot/honeypot.json | jq -r '.method + " " + .path + " from " + .remote_addr' 2>/dev/null || tail -3 logs/web-honeypot/honeypot.json
else
    echo "⚠️  No web logs found yet"
fi
echo ""

echo "✅ Test complete!"
echo ""
echo "📈 View results in Grafana:"
echo "   http://localhost:3000"
echo "   Login: admin / honeypot123"
echo ""
echo "   Dashboard: 'Honeypot Attack Dashboard'"
