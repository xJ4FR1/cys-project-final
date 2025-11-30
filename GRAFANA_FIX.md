# Grafana Permission Fix

## Issue
Grafana container fails with permission errors:
```
GF_PATHS_DATA='/var/lib/grafana' is not writable.
mkdir: can't create directory '/var/lib/grafana/plugins': Permission denied
```

## Root Cause
The Grafana container tries to write to the mounted `./data/grafana` directory but doesn't have proper permissions.

## Solution Applied

### 1. Updated docker-compose.yml
Changed Grafana configuration:
- Added `user: "0:0"` to run container as root
- Changed from bind mount to Docker volume: `grafana-data:/var/lib/grafana`
- Added explicit environment variables for Grafana paths

### 2. Fix Commands

If you're experiencing this issue, follow these steps:

```bash
# Stop all containers
sudo docker compose down

# Remove old Grafana container and data
sudo docker rm -f honeypot-grafana
sudo rm -rf data/grafana

# Pull latest changes
git pull

# Restart services
sudo docker compose up -d

# Verify Grafana is running
sudo docker compose ps
sudo docker logs honeypot-grafana
```

## Alternative Solutions

### Option 1: Fix Permissions (Not Recommended)
```bash
# This requires knowing the Grafana UID (472)
sudo chown -R 472:472 data/grafana
sudo chmod -R 755 data/grafana
```

### Option 2: Use Docker Volume (Recommended - Already Applied)
```yaml
volumes:
  - grafana-data:/var/lib/grafana  # Docker managed volume
```

### Option 3: Run as Root (Applied)
```yaml
user: "0:0"  # Run as root user
```

## Verification

After fixing, verify Grafana is running:

```bash
# Check container status
sudo docker compose ps

# Should show:
# honeypot-grafana   Up X seconds

# Check logs (should not show permission errors)
sudo docker logs honeypot-grafana

# Access Grafana
curl http://localhost:3000
# or open in browser
```

## Access Grafana

Once running:
- URL: http://localhost:3000
- Username: admin
- Password: honeypot123

## Notes

- **Docker Volume vs Bind Mount**: 
  - Bind mount (`./data/grafana`) = host directory, can have permission issues
  - Docker volume (`grafana-data`) = Docker-managed, no permission issues
  
- **Running as Root**: While not ideal for production, it's acceptable for a honeypot since the container is already isolated and the Grafana instance doesn't face the internet directly.

- **Data Persistence**: Docker volumes persist data even when containers are removed. To completely reset:
  ```bash
  sudo docker compose down -v  # Remove volumes
  ```

## Updated Files

1. `docker-compose.yml` - Changed Grafana volume and added user configuration
2. `deploy.sh` - Updated directory creation (no longer creates data/grafana)
3. `GRAFANA_FIX.md` - This troubleshooting guide

## If Still Failing

1. Check Docker version:
   ```bash
   docker --version
   # Should be 20.10+ 
   ```

2. Check SELinux (if on RHEL/CentOS):
   ```bash
   sudo setenforce 0  # Temporarily disable
   ```

3. Check disk space:
   ```bash
   df -h
   ```

4. View detailed logs:
   ```bash
   sudo docker logs honeypot-grafana --tail 100
   ```

5. Check volume:
   ```bash
   sudo docker volume ls | grep grafana
   sudo docker volume inspect cys-project-final_grafana-data
   ```

## Clean Reinstall

If nothing works, do a clean reinstall:

```bash
# Stop everything
sudo docker compose down -v

# Remove all containers
sudo docker ps -aq | xargs sudo docker rm -f

# Remove volumes
sudo docker volume prune -f

# Clean project
cd ~/Desktop/cys-project-final
rm -rf data/ logs/

# Restart
./deploy.sh
```

---

**Fixed**: November 30, 2025
