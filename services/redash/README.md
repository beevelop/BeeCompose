# Redash

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Redash is an open-source data visualization and dashboarding tool that connects to multiple data sources. This stack provides a complete Redash deployment with PostgreSQL, Redis, and Nginx reverse proxy.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.redash << 'EOF'
COMPOSE_PROJECT_NAME=redash
SERVICE_DOMAIN=redash.example.com
REDASH_COOKIE_SECRET=Swordfish32chars0000000000000000
EOF

# 2. Deploy
bc redash up

# 3. Initialize database (first time only)
docker exec redash-server /app/bin/docker-entrypoint create_db

# 4. Check status
bc redash ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.redash << 'EOF'
COMPOSE_PROJECT_NAME=redash
SERVICE_DOMAIN=redash.example.com
REDASH_COOKIE_SECRET=Swordfish32chars0000000000000000
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/redash:latest --env-file .env.redash up -d --pull always

# 3. Initialize database (first time only)
docker exec redash-server /app/bin/docker-entrypoint create_db

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/redash:latest --env-file .env.redash ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | redash-postgres | Primary database |
| Redis | redash-redis | Cache and task queue |
| Nginx | redash-nginx | Reverse proxy |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| redash-nginx | redash/nginx:latest | Nginx reverse proxy |
| redash-server | redash/redash:26.3.0 | Redash web server |
| redash-worker | redash/redash:26.3.0 | Background job scheduler |
| redash-postgres | postgres:17-alpine | PostgreSQL database |
| redash-redis | redis:7-alpine | Redis cache and queue |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Traefik routing | `redash.example.com` |
| `REDASH_COOKIE_SECRET` | Secret key for session cookies (32+ chars) | `Swordfish32chars0000000000000000` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `redash` |
| `REDASH_VERSION` | Redash image version | `26.3.0` |
| `REDASH_NGINX_VERSION` | Nginx image version | `latest` |
| `REDIS_TAG` | Redis image tag | `7-alpine` |
| `POSTGRES_TAG` | PostgreSQL image tag | `17-alpine` |

### Pre-configured

These are set in the docker-compose.yml:

| Variable | Value | Purpose |
|----------|-------|---------|
| `REDASH_REDIS_URL` | `redis://redis:6379/0` | Redis connection |
| `REDASH_DATABASE_URL` | `postgresql://postgres@postgres/postgres` | PostgreSQL connection |
| `REDASH_WEB_WORKERS` | `4` | Number of web workers |
| `WORKERS_COUNT` | `2` | Number of background workers |
| `QUEUES` | `queries,scheduled_queries,celery` | Worker queues |

## Volumes

| Volume | Purpose |
|--------|---------|
| `redash_postgres_data` | PostgreSQL database files |

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 5000 | TCP | Redash API server (internal, use Traefik) |

## Post-Deployment

### Initialize the Database (First Time Only)

```bash
docker exec redash-server /app/bin/docker-entrypoint create_db
```

### Create Admin User

1. Navigate to `https://redash.example.com`
2. Fill in the setup form with your organization name and admin credentials
3. Click "Setup" to create the initial admin account

### Add Data Sources

1. Go to Settings > Data Sources
2. Click "New Data Source"
3. Select your database type (PostgreSQL, MySQL, BigQuery, etc.)
4. Configure connection settings
5. Test and save

### Create Your First Query

1. Click "Create" > "Query"
2. Select a data source
3. Write your SQL query
4. Click "Execute" to run
5. Save and optionally add to a dashboard

## Common Operations

### Using bc CLI

```bash
bc redash logs -f              # View logs
bc redash logs -f redash-server  # View specific container logs
bc redash restart              # Restart
bc redash down                 # Stop
bc redash update               # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/redash:latest --env-file .env.redash"

# View logs
dc logs -f

# View specific container logs
dc logs -f redash-server
dc logs -f redash-worker

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d

# Run database migrations after update
docker exec redash-server /app/bin/docker-entrypoint manage db upgrade
```

## Troubleshooting

### Database not initialized
Run `docker exec redash-server /app/bin/docker-entrypoint create_db` on first deployment.

### Scheduled queries not running
Check the worker container is healthy: `dc logs redash-worker`

### Login issues
Verify `REDASH_COOKIE_SECRET` is set and consistent across restarts. Changing this will invalidate existing sessions.

### Container not healthy
Check logs with `dc logs <container>` and ensure all required environment variables are set.

### Slow queries
Consider increasing `REDASH_WEB_WORKERS` or `WORKERS_COUNT` based on load.

## Links

- [Official Documentation](https://redash.io/help/)
- [Docker Hub - Redash](https://hub.docker.com/r/redash/redash)
- [GitHub](https://github.com/getredash/redash)
