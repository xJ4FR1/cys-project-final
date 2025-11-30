# Simplified Honeypot Project

## Overview
This is a streamlined honeypot deployment focused on three core services with minimal monitoring overhead.

## Architecture

### Honeypots (3 Services)
1. **SSH Honeypot** - Port 222
   - Custom Python-based SSH honeypot
   - Logs all authentication attempts
   - Records commands and interactions

2. **FTP Honeypot** - Port 211
   - Dionaea-based FTP honeypot
   - Captures file transfer attempts
   - Logs FTP authentication

3. **Web Honeypot** - Port 80
   - Custom Flask-based web honeypot
   - Simulates admin login portal
   - Logs all HTTP requests and form submissions

### Visualization (1 Service)
- **Grafana** - Port 3000
  - Direct JSON log file reading
  - Pre-configured dashboards
  - No complex log forwarding pipelines
  - Username: `admin` / Password: `honeypot123`

## Removed Components
The following components were removed to simplify the architecture:
- ❌ Loki (log aggregation)
- ❌ Promtail (log shipper)
- ❌ Prometheus (metrics collection)
- ❌ Node Exporter (system metrics)
- ❌ cAdvisor (container metrics)

## Quick Start

```bash
# Deploy all services
./deploy.sh

# Or manually with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Port Configuration

| Service | Port | Protocol | Description |
|---------|------|----------|-------------|
| SSH Honeypot | 222 | TCP | SSH login attempts |
| FTP Honeypot | 211 | TCP | FTP connections |
| Web Honeypot | 80 | TCP | HTTP requests |
| Grafana | 3000 | TCP | Web dashboard |

## Log Files

All honeypots write JSON logs to `./logs/`:
- `./logs/ssh-honeypot/ssh_honeypot.json` - SSH activity
- `./logs/dionaea/` - FTP activity
- `./logs/web-honeypot/honeypot.json` - Web activity

## Testing

```bash
# Test SSH honeypot
ssh -p 222 admin@localhost

# Test FTP honeypot
ftp -p 211 localhost

# Test Web honeypot
curl http://localhost:80
```

## Monitoring

Access Grafana at: http://localhost:3000
- Username: `admin`
- Password: `honeypot123`

Grafana reads logs directly from the filesystem mounted at `/var/log/honeypot` inside the container.

## Benefits of Simplified Architecture

✅ **Reduced Complexity**: Only 4 containers instead of 10
✅ **Lower Resource Usage**: No metrics exporters or log shippers
✅ **Easier Debugging**: Direct log file access
✅ **Faster Startup**: Fewer service dependencies
✅ **Simplified Maintenance**: Less configuration to manage

## Notes

- FTP runs on port 211 instead of standard 21 (Dionaea internally uses port 21, mapped to 211)
- SSH runs on port 222 instead of standard 22
- Web runs on standard port 80
- All services log to local files in JSON format
- Grafana uses the JSON datasource plugin to read logs directly
