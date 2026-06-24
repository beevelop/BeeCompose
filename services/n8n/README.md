# n8n

> **OCI Artifact** - Deploy directly from GitHub Container Registry

n8n is a fair-code workflow automation platform that enables you to connect anything to everything. Build complex automations with a visual editor, integrate 400+ apps, and self-host for full data control.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Generate encryption key (CRITICAL - save this securely!)
openssl rand -base64 32

# 2. Create environment file
cat > .env.n8n << 'EOF'
COMPOSE_PROJECT_NAME=n8n
SERVICE_DOMAIN=n8n.example.com
DB_PASS=your-secure-password
N8N_ENCRYPTION_KEY=your-generated-key-from-step-1
TZ=UTC
EOF

# 3. Deploy
bc n8n up

# 4. Check status
bc n8n ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Generate encryption key (CRITICAL - save this securely!)
openssl rand -base64 32

# 2. Create environment file
cat > .env.n8n << 'EOF'
COMPOSE_PROJECT_NAME=n8n
SERVICE_DOMAIN=n8n.example.com
DB_PASS=your-secure-password
N8N_ENCRYPTION_KEY=your-generated-key-from-step-1
TZ=UTC
EOF

# 3. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/n8n:latest --env-file .env.n8n up -d --pull always

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/n8n:latest --env-file .env.n8n ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | n8n-postgres | Workflow and credential storage |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| n8n | n8nio/n8n | Workflow automation platform |
| n8n-postgres | postgres:16-alpine | PostgreSQL database for n8n data |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for n8n access (used for webhooks) | `n8n.example.com` |
| `DB_PASS` | PostgreSQL password | `Swordfish` |
| `N8N_ENCRYPTION_KEY` | Encryption key for credentials (generate with `openssl rand -base64 32`) | `abc123...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `n8n` |
| `DB_USER` | PostgreSQL username | `n8n` |
| `DB_NAME` | PostgreSQL database name | `n8n` |
| `N8N_VERSION` | n8n image tag | `2.28.1` |
| `POSTGRES_VERSION` | PostgreSQL image tag | `16-alpine` |
| `TZ` | Timezone for workflow scheduling (IANA format) | `UTC` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `n8n_n8n_data` | n8n user data, custom nodes, and settings |
| `n8n_postgres_data` | PostgreSQL database files |

## Security Considerations

### Encryption Key

The `N8N_ENCRYPTION_KEY` is **critical** for securing stored credentials:

- Generate with: `openssl rand -base64 32`
- Store securely (password manager, secrets vault)
- **Loss of this key = loss of all stored credentials**
- All API keys, OAuth tokens, and passwords in n8n are encrypted with this key

### Production Recommendations

1. **Use strong passwords** for database and encryption key
2. **Enable 2FA** in n8n user settings after initial setup
3. **Restrict webhook access** if possible via Traefik middleware
4. **Regular backups** of both volumes (see backup section)
5. **Monitor execution logs** for unauthorized access

## Post-Deployment

1. **Access n8n**: Navigate to `https://n8n.example.com`
2. **Create Owner Account**: Set up your first admin user
3. **Configure Settings**: Adjust timezone, execution limits, etc.
4. **Install Community Nodes**: Add integrations from the n8n community
5. **Create Workflows**: Start building automations with the visual editor
6. **Set Up Webhooks**: Configure triggers for external events

## Common Operations

### Using bc CLI

```bash
bc n8n logs -f        # View logs
bc n8n logs -f n8n    # View n8n logs only
bc n8n restart        # Restart
bc n8n down           # Stop
bc n8n update         # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/n8n:latest --env-file .env.n8n"

# View logs
dc logs -f

# View n8n logs only
dc logs -f n8n

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

## Backup

### Automated Backup (Recommended)

Both volumes should be backed up regularly:

```bash
# Backup n8n data
docker run --rm -v n8n_n8n_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/n8n-data-$(date +%Y%m%d).tar.gz -C /data .

# Backup PostgreSQL
docker exec n8n-postgres pg_dump -U n8n n8n > n8n-db-$(date +%Y%m%d).sql
```

### Restore

```bash
# Restore n8n data
docker run --rm -v n8n_n8n_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/n8n-data-YYYYMMDD.tar.gz -C /data

# Restore PostgreSQL
docker exec -i n8n-postgres psql -U n8n n8n < n8n-db-YYYYMMDD.sql
```

## Troubleshooting

### Webhooks not working

- Ensure `SERVICE_DOMAIN` matches your actual domain
- Verify HTTPS is working via Traefik
- Check that `WEBHOOK_URL` environment variable is set correctly

### Credentials not decrypting

- The `N8N_ENCRYPTION_KEY` must match the key used when credentials were created
- If you lost the key, credentials must be re-entered manually

### Database connection errors

- Check that PostgreSQL container is healthy: `docker ps`
- Verify database credentials match in both services
- Check logs: `dc logs postgres`

### Slow workflow execution

- Increase container resources if needed
- Enable execution data pruning (enabled by default)
- Consider queue mode with Redis for high-volume workloads

### Container not healthy

Check logs with `dc logs n8n` and ensure all required environment variables are set.

## Advanced Configuration

### Queue Mode (High Volume)

For high-volume workloads, n8n supports queue mode with Redis. Add Redis to the compose file:

```yaml
# Add to services section
redis:
  image: redis:7-alpine
  container_name: n8n-redis
  networks:
    - n8n
  restart: unless-stopped

# Add to n8n environment
EXECUTIONS_MODE: queue
QUEUE_BULL_REDIS_HOST: redis
QUEUE_BULL_REDIS_PORT: 6379
```

### External Database

To use an existing PostgreSQL instance, remove the `postgres` service and update environment variables:

```bash
DB_POSTGRESDB_HOST=your-postgres-host
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=your-password
```

## Links

- [Official Documentation](https://docs.n8n.io/)
- [Docker Hub](https://hub.docker.com/r/n8nio/n8n)
- [GitHub](https://github.com/n8n-io/n8n)
- [Community Nodes](https://www.npmjs.com/search?q=n8n-nodes)
- [Workflow Templates](https://n8n.io/workflows/)
