# Sentry

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Self-hosted error tracking and performance monitoring platform for identifying and debugging production issues across your applications.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.sentry << 'EOF'
COMPOSE_PROJECT_NAME=sentry
SERVICE_DOMAIN=sentry.example.com
DB_PASS=Swordfish
EOF

# 2. Create sentry.env configuration
cat > sentry.env << 'EOF'
SENTRY_SYSTEM_SECRET_KEY=your-secret-key-here-generate-with-sentry-config-generate-secret-key
SENTRY_SECRET_KEY=your-secret-key-here-generate-with-sentry-config-generate-secret-key
SENTRY_MEMCACHED_HOST=memcached
SENTRY_REDIS_HOST=redis
SENTRY_POSTGRES_HOST=postgres
SENTRY_DB_NAME=sentry
SENTRY_DB_USER=sentry
SENTRY_DB_PASSWORD=Swordfish
EOF

# 3. Deploy
bc sentry up

# 4. Check status
bc sentry ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.sentry << 'EOF'
COMPOSE_PROJECT_NAME=sentry
SERVICE_DOMAIN=sentry.example.com
DB_PASS=Swordfish
EOF

# 2. Create sentry.env configuration
cat > sentry.env << 'EOF'
SENTRY_SYSTEM_SECRET_KEY=your-secret-key-here-generate-with-sentry-config-generate-secret-key
SENTRY_SECRET_KEY=your-secret-key-here-generate-with-sentry-config-generate-secret-key
SENTRY_MEMCACHED_HOST=memcached
SENTRY_REDIS_HOST=redis
SENTRY_POSTGRES_HOST=postgres
SENTRY_DB_NAME=sentry
SENTRY_DB_USER=sentry
SENTRY_DB_PASSWORD=Swordfish
EOF

# 3. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.sentry up -d --pull always

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.sentry ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))
- Minimum 4GB RAM recommended

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | sentry-postgres | Primary database |
| Redis | sentry-redis | Cache and message broker |
| Memcached | sentry-memcached | Session caching |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| sentry | getsentry/sentry:25.7.0 | Main Sentry web server |
| sentry-celery-worker | getsentry/sentry:25.7.0 | Background task processor |
| sentry-celery-cron | getsentry/sentry:25.7.0 | Scheduled task runner |
| sentry-postgres | postgres:17-alpine | Primary database |
| sentry-redis | redis:7-alpine | Cache and message broker |
| sentry-memcached | memcached:1.6 | Session and result caching |

## Environment Variables

### Required (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Sentry | `sentry.example.com` |
| `DB_PASS` | PostgreSQL password | `Swordfish` |

### Required (sentry.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SENTRY_SYSTEM_SECRET_KEY` | Secret key for encryption (25.x+) | Generate with `sentry config generate-secret-key` |
| `SENTRY_SECRET_KEY` | Secret key legacy fallback (24.x) | Same value as `SENTRY_SYSTEM_SECRET_KEY` |
| `SENTRY_MEMCACHED_HOST` | Memcached hostname | `memcached` |
| `SENTRY_REDIS_HOST` | Redis hostname | `redis` |
| `SENTRY_POSTGRES_HOST` | PostgreSQL hostname | `postgres` |

### Optional (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `sentry` |
| `SENTRY_VERSION` | Sentry image version | `25.7.0` |
| `POSTGRES_TAG` | PostgreSQL image tag | `17-alpine` |
| `REDIS_TAG` | Redis image tag | `7-alpine` |
| `MEMCACHED_TAG` | Memcached image tag | `1.6` |
| `DB_NAME` | PostgreSQL database name | `sentry` |
| `DB_USER` | PostgreSQL username | `sentry` |
| `SENTRY_EVENT_RETENTION_DAYS` | Days to retain events | `90` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `postgres_data` | PostgreSQL database files |
| `redis_data` | Redis persistence |
| `sentry_files` | Uploaded files and attachments |
| `sentry_config` | Sentry configuration |

## Post-Deployment

### Initialize Database

Run the database migrations and create the first superuser:

```bash
# Run migrations
docker exec -it sentry sentry upgrade

# Create admin user (interactive)
docker exec -it sentry sentry createuser --superuser
```

### Generate Secret Key

Generate a secret key and set both `SENTRY_SYSTEM_SECRET_KEY` and `SENTRY_SECRET_KEY` in your `sentry.env`:

```bash
docker run --rm getsentry/sentry:25.7.0 sentry config generate-secret-key
```

Or with OpenSSL:

```bash
openssl rand -hex 32
```

### Configure Email (Optional)

Add to `sentry.env`:

```bash
SENTRY_EMAIL_HOST=smtp.example.com
SENTRY_EMAIL_PORT=587
SENTRY_EMAIL_USER=sentry@example.com
SENTRY_EMAIL_PASSWORD=Swordfish
SENTRY_EMAIL_USE_TLS=true
SENTRY_SERVER_EMAIL=sentry@example.com
```

## Common Operations

### Using bc CLI

```bash
bc sentry logs -f       # View logs
bc sentry logs -f server  # View specific service logs
bc sentry restart       # Restart
bc sentry down          # Stop
bc sentry update        # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.sentry"

# View logs
dc logs -f

# View specific service logs
dc logs -f server
dc logs -f celery-worker

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

### Cleanup Old Data

```bash
docker exec -it sentry sentry cleanup --days 30
```

### Backup

```bash
# Backup PostgreSQL database
docker exec sentry-postgres pg_dump -U sentry sentry > sentry-backup.sql
```

### Upgrade

```bash
# 1. Create a backup first
docker exec sentry-postgres pg_dump -U sentry sentry > sentry-backup.sql

# 2. Update version in .env
# 3. Pull new images and restart
docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.sentry pull
docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.sentry up -d

# 4. Run migrations if needed
docker exec -it sentry sentry upgrade
```

> **⚠️ Upgrading from 24.x:** Rename `SENTRY_SECRET_KEY` to `SENTRY_SYSTEM_SECRET_KEY` in your
> `sentry.env` (keep both during the transition). The 25.x release also introduces
> `SENTRY_EVENT_RETENTION_DAYS` to control how long events are stored (default: 90 days).

## Troubleshooting

### Migration Errors

If migrations fail, check PostgreSQL connectivity:

```bash
docker exec -it sentry-postgres psql -U sentry -c "SELECT 1"
```

### Worker Not Processing Events

Check Celery worker status and logs:

```bash
docker logs sentry-celery-worker
```

### High Memory Usage

Sentry is memory-intensive. Ensure at least 4GB RAM is available. Consider reducing worker concurrency if needed.

### Container not healthy

Check logs with `dc logs server` and ensure all required environment variables are set. The server has a 120-second startup period.

## Links

- [Official Documentation](https://docs.sentry.io/server/)
- [Docker Hub](https://hub.docker.com/r/getsentry/sentry)
- [GitHub](https://github.com/getsentry/sentry)
