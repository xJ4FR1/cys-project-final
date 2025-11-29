#!/bin/bash
# Log Analysis and Statistics Script
# Provides quick insights into captured attack data

echo "🔍 Honeypot Log Analysis"
echo "========================"
echo ""

# Check if logs directory exists
if [ ! -d "logs" ]; then
    echo "❌ Logs directory not found. Have you started the honeypot?"
    exit 1
fi

# Helper function to check if jq is installed
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "⚠️  jq is not installed. Some features will be limited."
        echo "   Install with: sudo apt install jq"
        return 1
    fi
    return 0
}

HAS_JQ=$(check_jq && echo "yes" || echo "no")

echo "📊 STATISTICS"
echo "-------------"
echo ""

# Cowrie (SSH) statistics
if [ -d "logs/cowrie" ]; then
    echo "🔐 SSH Honeypot (Cowrie):"
    COWRIE_LOGS=$(find logs/cowrie -name "*.json" -type f 2>/dev/null)
    
    if [ -n "$COWRIE_LOGS" ]; then
        TOTAL_EVENTS=$(cat $COWRIE_LOGS 2>/dev/null | wc -l)
        echo "   Total events: $TOTAL_EVENTS"
        
        if [ "$HAS_JQ" = "yes" ] && [ $TOTAL_EVENTS -gt 0 ]; then
            echo "   Top attacking IPs:"
            cat $COWRIE_LOGS 2>/dev/null | jq -r '.src_ip // empty' | sort | uniq -c | sort -rn | head -5 | while read count ip; do
                echo "      $ip: $count attempts"
            done
            
            echo "   Most used usernames:"
            cat $COWRIE_LOGS 2>/dev/null | jq -r '.username // empty' | grep -v '^$' | sort | uniq -c | sort -rn | head -5 | while read count user; do
                echo "      $user: $count attempts"
            done
            
            echo "   Most used passwords:"
            cat $COWRIE_LOGS 2>/dev/null | jq -r '.password // empty' | grep -v '^$' | sort | uniq -c | sort -rn | head -5 | while read count pass; do
                echo "      $pass: $count attempts"
            done
        fi
    else
        echo "   No logs found yet"
    fi
    echo ""
fi

# Dionaea (Multi-protocol) statistics
if [ -d "logs/dionaea" ]; then
    echo "🌐 Multi-Protocol Honeypot (Dionaea):"
    DIONAEA_LOGS=$(find logs/dionaea -name "*.log" -type f 2>/dev/null)
    
    if [ -n "$DIONAEA_LOGS" ]; then
        TOTAL_EVENTS=$(cat $DIONAEA_LOGS 2>/dev/null | wc -l)
        echo "   Total events: $TOTAL_EVENTS"
        
        if [ $TOTAL_EVENTS -gt 0 ]; then
            echo "   Recent connections:"
            tail -n 5 $DIONAEA_LOGS 2>/dev/null | while read line; do
                echo "      $(echo $line | cut -c1-80)..."
            done
            
            echo "   Connection count by log file:"
            for log in $DIONAEA_LOGS; do
                COUNT=$(wc -l < "$log" 2>/dev/null)
                echo "      $(basename $log): $COUNT events"
            done
        fi
    else
        echo "   No logs found yet"
    fi
    echo ""
fi

# Web Honeypot statistics
if [ -d "logs/web-honeypot" ]; then
    echo "🕸️  Web Honeypot:"
    WEB_LOGS=$(find logs/web-honeypot -name "*.json" -type f 2>/dev/null)
    
    if [ -n "$WEB_LOGS" ]; then
        TOTAL_REQUESTS=$(cat $WEB_LOGS 2>/dev/null | wc -l)
        echo "   Total requests: $TOTAL_REQUESTS"
        
        if [ "$HAS_JQ" = "yes" ] && [ $TOTAL_REQUESTS -gt 0 ]; then
            echo "   Top paths requested:"
            cat $WEB_LOGS 2>/dev/null | jq -r '.path // empty' | sort | uniq -c | sort -rn | head -5 | while read count path; do
                echo "      $path: $count requests"
            done
            
            echo "   Top attacking IPs:"
            cat $WEB_LOGS 2>/dev/null | jq -r '.remote_addr // empty' | sort | uniq -c | sort -rn | head -5 | while read count ip; do
                echo "      $ip: $count requests"
            done
            
            echo "   Top User Agents:"
            cat $WEB_LOGS 2>/dev/null | jq -r '.user_agent // empty' | sort | uniq -c | sort -rn | head -3 | while read count agent; do
                agent_short=$(echo "$agent" | cut -c1-60)
                echo "      $agent_short: $count requests"
            done
        fi
    else
        echo "   No logs found yet"
    fi
    echo ""
fi

# Overall statistics
echo "📈 OVERALL STATISTICS"
echo "--------------------"
echo ""

# Disk usage
echo "💾 Disk Usage:"
du -sh logs/ data/ 2>/dev/null | while read size dir; do
    echo "   $dir: $size"
done
echo ""

# Recent activity (last 24 hours)
echo "⏰ Recent Activity (Last 24 Hours):"
RECENT=$(find logs -type f -mtime -1 -name "*.json" -o -name "*.log" 2>/dev/null)
if [ -n "$RECENT" ]; then
    for log in $RECENT; do
        EVENTS=$(wc -l < "$log" 2>/dev/null)
        echo "   $(basename $log): $EVENTS events"
    done
else
    echo "   No recent activity"
fi
echo ""

# Container status
echo "🐳 Container Status:"
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null | grep honeypot
echo ""

# Export options
echo "💾 EXPORT OPTIONS"
echo "----------------"
echo ""
echo "Export all logs to archives:"
echo "   ./scripts/export-logs.sh"
echo ""
echo "View live logs:"
echo "   docker compose logs -f cowrie"
echo "   docker compose logs -f heralding"
echo "   docker compose logs -f web-honeypot"
echo ""
echo "Query Loki directly:"
echo "   curl -G -s \"http://localhost:3100/loki/api/v1/query_range\" \\"
echo "     --data-urlencode 'query={job=\"cowrie\"}' | jq ."
echo ""
