# Zabbix

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Enterprise-class open source distributed monitoring solution for networks, servers, virtual machines, and cloud services.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.zabbix << 'EOF'
COMPOSE_PROJECT_NAME=zabbix
SERVICE_DOMAIN=zabbix.example.com
DB_PASS=Swordfish
DB_ROOT_PASS=Swordfish
EOF

# 2. Deploy
bc zabbix up

# 3. Check status
bc zabbix ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.zabbix << 'EOF'
COMPOSE_PROJECT_NAME=zabbix
SERVICE_DOMAIN=zabbix.example.com
DB_PASS=Swordfish
DB_ROOT_PASS=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/zabbix:latest --env-file .env.zabbix up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/zabbix:latest --env-file .env.zabbix ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| MariaDB | zabbix-mariadb | Primary database |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| zabbix-web | zabbix/zabbix-web-nginx-mysql:7.4.11-alpine | Web frontend (Nginx + PHP) |
| zabbix-server | zabbix/zabbix-server-mysql:7.4.11-alpine | Zabbix server daemon |
| zabbix-mariadb | mariadb:12.2 | MariaDB database |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Zabbix web interface | `zabbix.example.com` |
| `DB_PASS` | MariaDB user password | `Swordfish` |
| `DB_ROOT_PASS` | MariaDB root password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `zabbix` |
| `DB_USER` | MariaDB username | `zabbix` |
| `PHP_TZ` | PHP timezone | `Europe/Berlin` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `zabbix_mariadb_data` | MariaDB database files |
| `zabbix_alertscripts` | Custom alert scripts |
| `zabbix_externalscripts` | External check scripts |

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 10051 | TCP | Zabbix server (agent connections) |

## Post-Deployment

1. **Wait for initialization** - Database import takes 1-2 minutes on first start
2. **Access web interface** at `https://zabbix.example.com`
3. **Login with default credentials**:
   - Username: `Admin`
   - Password: `zabbix`
4. **Change the default password immediately**
5. **Configure hosts and monitoring templates**

### Initial Setup Checklist

- [ ] Change default Admin password
- [ ] Configure SMTP for email alerts
- [ ] Add hosts to monitor
- [ ] Apply appropriate templates
- [ ] Set up user groups and permissions
- [ ] Configure custom dashboards

### Agent Configuration

Point Zabbix agents to the server:
```ini
Server=your-server-ip
ServerActive=your-server-ip:10051
```

## Common Operations

### Using bc CLI

```bash
bc zabbix logs -f          # View logs
bc zabbix logs -f zabbix-server  # View server logs specifically
bc zabbix restart          # Restart
bc zabbix down             # Stop
bc zabbix update           # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/zabbix:latest --env-file .env.zabbix"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d

# View server logs specifically
dc logs -f zabbix-server
```

## Troubleshooting

### Database connection timeout on first start
The database import takes time. Wait 2-3 minutes and check:
```bash
dc logs zabbix-mariadb
dc logs zabbix-server
```

### Agents cannot connect
Ensure port 10051 is accessible and firewall rules allow agent connections. Test with:
```bash
telnet your-server-ip 10051
```

### Web interface slow or unresponsive
Check PHP memory limits and database performance:
```bash
dc logs zabbix-web
```

### Container not healthy
Check logs with `dc logs <container>` and ensure all required environment variables are set.

### Timezone issues
Set `PHP_TZ` to your local timezone (e.g., `America/New_York`, `Europe/London`).

## Links

- [Official Documentation](https://www.zabbix.com/documentation/current/)
- [Docker Hub - Server](https://hub.docker.com/r/zabbix/zabbix-server-mysql)
- [Docker Hub - Web](https://hub.docker.com/r/zabbix/zabbix-web-nginx-mysql)
- [GitHub](https://github.com/zabbix/zabbix)
