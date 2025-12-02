#!/bin/bash
# Automated Attack Simulation Script
# Generates realistic attack traffic for honeypot testing

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           🎯 Honeypot Attack Simulation                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
SSH_PORT=222
FTP_PORT=211
WEB_PORT=80
TARGET="localhost"
DELAY=1  # Delay between attacks in seconds

# Check if services are running
check_service() {
    local port=$1
    local name=$2
    
    if nc -zv $TARGET $port 2>&1 | grep -q "succeeded\|open"; then
        echo -e "${GREEN}✓${NC} $name is accessible on port $port"
        return 0
    else
        echo -e "${RED}✗${NC} $name is NOT accessible on port $port"
        return 1
    fi
}

echo "📡 Checking honeypot availability..."
echo ""

SSH_AVAILABLE=0
FTP_AVAILABLE=0
WEB_AVAILABLE=0

check_service $SSH_PORT "SSH Honeypot" && SSH_AVAILABLE=1 || true
check_service $FTP_PORT "FTP Honeypot" && FTP_AVAILABLE=1 || true
check_service $WEB_PORT "Web Honeypot" && WEB_AVAILABLE=1 || true

echo ""

if [ $SSH_AVAILABLE -eq 0 ] && [ $FTP_AVAILABLE -eq 0 ] && [ $WEB_AVAILABLE -eq 0 ]; then
    echo -e "${RED}❌ No honeypots are accessible. Please start the services first:${NC}"
    echo "   docker compose up -d"
    exit 1
fi

# SSH Attack Simulation
simulate_ssh_attacks() {
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  🔐 SSH Brute Force Attack Simulation                    ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Common username/password combinations
    declare -a USERNAMES=("root" "admin" "user" "test")
    declare -a PASSWORDS=("password" "123456" "admin" "root")
    
    local attack_count=0
    local max_attacks=12
    
    echo "Launching SSH brute force attacks..."
    echo ""
    
    for username in "${USERNAMES[@]}"; do
        for password in "${PASSWORDS[@]}"; do
            if [ $attack_count -ge $max_attacks ]; then
                break 2
            fi
            
            echo -e "  ${BLUE}→${NC} Attempting: $username:$password"
            
            # Try SSH connection (will fail, but will be logged)
            timeout 3 sshpass -p "$password" ssh -o StrictHostKeyChecking=no \
                -o UserKnownHostsFile=/dev/null \
                -o ConnectTimeout=2 \
                -p $SSH_PORT \
                "$username@$TARGET" exit 2>/dev/null || true
            
            attack_count=$((attack_count + 1))
            sleep $DELAY
        done
    done
    
    echo ""
    echo -e "${GREEN}✓${NC} Completed $attack_count SSH attack attempts"
    echo ""
}

# FTP Attack Simulation
simulate_ftp_attacks() {
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  📁 FTP Attack Simulation                                 ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    declare -a FTP_USERS=("anonymous" "ftp" "admin")
    declare -a FTP_PASS=("anonymous" "ftp" "admin")
    
    local attack_count=0
    local max_attacks=6
    
    echo "Launching FTP connection attempts..."
    echo ""
    
    for user in "${FTP_USERS[@]}"; do
        if [ $attack_count -ge $max_attacks ]; then
            break
        fi
        
        for pass in "${FTP_PASS[@]}"; do
            if [ $attack_count -ge $max_attacks ]; then
                break
            fi
            
            echo -e "  ${BLUE}→${NC} FTP attempt: $user:$pass"
            
            # Try FTP connection
            timeout 3 ftp -n $TARGET $FTP_PORT <<EOF 2>/dev/null || true
user $user $pass
ls
quit
EOF
            
            attack_count=$((attack_count + 1))
            sleep $DELAY
        done
    done
    
    echo ""
    echo -e "${GREEN}✓${NC} Completed $attack_count FTP attack attempts"
    echo ""
}

# Web Attack Simulation
simulate_web_attacks() {
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  🕸️  Web Attack Simulation                                ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Vulnerable endpoints to probe
    declare -a WEB_PATHS=(
        "/"
        "/admin"
        "/login"
        "/wp-admin/"
        "/phpmyadmin/"
        "/.env"
        "/.git/config"
        "/api/v1/users"
        "/backup.sql"
        "/config.php"
    )
    
    echo "Launching web reconnaissance and attacks..."
    echo ""
    
    # GET requests
    for path in "${WEB_PATHS[@]}"; do
        echo -e "  ${BLUE}→${NC} GET http://$TARGET:$WEB_PORT$path"
        curl -s -o /dev/null -w "Status: %{http_code}\n" \
            -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
            "http://$TARGET:$WEB_PORT$path" 2>/dev/null | sed 's/^/    /' || true
        sleep $DELAY
    done
    
    echo ""
    echo "Testing credential attacks..."
    
    # Common credential attacks
    declare -a USERS=("admin" "root" "user")
    declare -a PASSWORDS=("admin" "password" "123456")
    
    for user in "${USERS[@]}"; do
        for pass in "${PASSWORDS[@]}"; do
            echo -e "  ${BLUE}→${NC} Login attempt: $user:$pass"
            curl -s -o /dev/null \
                -X POST \
                -H "Content-Type: application/x-www-form-urlencoded" \
                -d "username=$user&password=$pass" \
                "http://$TARGET:$WEB_PORT/login" 2>/dev/null || true
            sleep $DELAY
        done
    done
    
    echo ""
    echo -e "${GREEN}✓${NC} Completed web attack simulation"
    echo ""
}

# Main execution
echo "⚙️  Attack simulation configuration:"
echo "   Target: $TARGET"
echo "   SSH Port: $SSH_PORT"
echo "   FTP Port: $FTP_PORT"
echo "   Web Port: $WEB_PORT"
echo "   Delay between attacks: ${DELAY}s"
echo ""

read -p "Start attack simulation? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Simulation cancelled."
    exit 0
fi

echo ""
START_TIME=$(date +%s)

# Run simulations
if [ $SSH_AVAILABLE -eq 1 ]; then
    if command -v sshpass &> /dev/null; then
        simulate_ssh_attacks
    else
        echo -e "${YELLOW}⚠️  sshpass not installed. Skipping SSH attacks.${NC}"
        echo "   Install with: sudo apt install sshpass"
        echo ""
    fi
else
    echo -e "${YELLOW}⚠️  SSH honeypot not available. Skipping SSH attacks.${NC}"
    echo ""
fi

if [ $FTP_AVAILABLE -eq 1 ]; then
    if command -v ftp &> /dev/null; then
        simulate_ftp_attacks
    else
        echo -e "${YELLOW}⚠️  ftp client not installed. Skipping FTP attacks.${NC}"
        echo "   Install with: sudo apt install ftp"
        echo ""
    fi
else
    echo -e "${YELLOW}⚠️  FTP honeypot not available. Skipping FTP attacks.${NC}"
    echo ""
fi

if [ $WEB_AVAILABLE -eq 1 ]; then
    simulate_web_attacks
else
    echo -e "${YELLOW}⚠️  Web honeypot not available. Skipping Web attacks.${NC}"
    echo ""
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Attack Simulation Complete                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📊 Summary:"
echo "   Duration: ${DURATION}s"
echo "   Target: $TARGET"
echo ""
echo "📈 Next steps:"
echo "   1. Wait 10-15 seconds for logs to flush"
echo "   2. Check Grafana dashboards: http://localhost:3000"
echo "   3. Analyze logs: ./scripts/analyze-logs.sh"
echo "   4. View log files:"
echo "      - SSH: logs/ssh-honeypot/ssh_honeypot.json"
echo "      - Web: logs/web-honeypot/honeypot.json"
echo "      - FTP: logs/dionaea/"
echo ""
