#!/bin/bash
# Cleanup script for honeypot deployment

echo "🧹 Honeypot Cleanup Script"
echo "=========================="
echo ""

# Function to confirm action
confirm() {
    read -p "$1 (yes/no): " -r
    [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]
}

# Stop containers
if confirm "Stop all honeypot containers?"; then
    echo "⏹️  Stopping containers..."
    docker compose down
    echo "✓ Containers stopped"
    echo ""
fi

# Remove logs
if confirm "Delete all log files? (THIS CANNOT BE UNDONE)"; then
    echo "🗑️  Removing logs..."
    rm -rf logs/*
    echo "✓ Logs deleted"
    echo ""
fi

# Remove data volumes
if confirm "Delete all persistent data? (THIS CANNOT BE UNDONE)"; then
    echo "🗑️  Removing data volumes..."
    rm -rf data/*
    docker compose down -v
    echo "✓ Data deleted"
    echo ""
fi

# Remove Docker images
if confirm "Remove Docker images?"; then
    echo "🗑️  Removing images..."
    docker compose down --rmi all
    echo "✓ Images removed"
    echo ""
fi

# Clean Docker system
if confirm "Run Docker system prune (removes unused data)?"; then
    echo "🗑️  Cleaning Docker system..."
    docker system prune -f
    echo "✓ Docker system cleaned"
    echo ""
fi

echo "✅ Cleanup complete!"
echo ""
echo "To redeploy: ./deploy.sh"
echo ""
