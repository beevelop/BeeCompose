# Weblate

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Web-based continuous localization platform with tight version control integration, quality checks, and translation memory.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.weblate << 'EOF'
COMPOSE_PROJECT_NAME=weblate
SERVICE_DOMAIN=weblate.example.com
DB_NAME=weblate
DB_USER=weblate
DB_PASS=Swordfish
EOF

# 2. Create weblate.env for additional settings
cat > weblate.env << 'EOF'
SECRET_KEY=your_random_secret_key_here
ADMIN_PASSWORD=Swordfish
WEBLATE_ADMIN_NAME=admin
WEBLATE_ADMIN_EMAIL=admin@example.com
WEBLATE_EMAIL=noreply@example.com
REGISTRATION_OPEN=False
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=Swordfish
EMAIL_PORT=465
DATABASE_PORT_5432_TCP_ADDR=postgres
DATABASE_PORT_5432_TCP_PORT=5432
EOF

# 3. Deploy
bc weblate up

# 4. Check status
bc weblate ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.weblate << 'EOF'
COMPOSE_PROJECT_NAME=weblate
SERVICE_DOMAIN=weblate.example.com
DB_NAME=weblate
DB_USER=weblate
DB_PASS=Swordfish
EOF

# 2. Create weblate.env for additional settings
cat > weblate.env << 'EOF'
SECRET_KEY=your_random_secret_key_here
ADMIN_PASSWORD=Swordfish
WEBLATE_ADMIN_NAME=admin
WEBLATE_ADMIN_EMAIL=admin@example.com
WEBLATE_EMAIL=noreply@example.com
REGISTRATION_OPEN=False
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=Swordfish
EMAIL_PORT=465
DATABASE_PORT_5432_TCP_ADDR=postgres
DATABASE_PORT_5432_TCP_PORT=5432
EOF

# 3. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/weblate:latest --env-file .env.weblate up -d --pull always

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/weblate:latest --env-file .env.weblate ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | weblate-postgres | Primary database |
| Redis | weblate-redis | Caching and task queue |
| Memcached | weblate-memcached | Session caching |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| weblate | weblate/weblate:2026.6 | Translation management web application |
| weblate-postgres | postgres:17-alpine | PostgreSQL database |
| weblate-redis | redis:7-alpine | Caching and task queue |
| weblate-memcached | memcached:1.6-alpine | Session caching |

## Environment Variables

### Required (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Weblate | `weblate.example.com` |
| `DB_PASS` | PostgreSQL password | `Swordfish` |

### Optional (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `weblate` |
| `DB_NAME` | PostgreSQL database name | `weblate` |
| `DB_USER` | PostgreSQL username | `weblate` |

### Required (weblate.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (random string) | `Ygv4nrBzLG9J7iFxp...` |
| `ADMIN_PASSWORD` | Initial admin password | `Swordfish` |
| `WEBLATE_ADMIN_EMAIL` | Admin email address | `admin@example.com` |

### Optional (weblate.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `WEBLATE_ADMIN_NAME` | Admin username | `admin` |
| `WEBLATE_EMAIL` | Outgoing email address | `noreply@example.com` |
| `WEBLATE_DEBUG` | Enable debug mode | `0` |
| `WEBLATE_LOCK_DOWN` | Lock down public access | `false` |
| `REGISTRATION_OPEN` | Allow public registration | `True` |
| `EMAIL_HOST` | SMTP server hostname | - |
| `EMAIL_HOST_USER` | SMTP username | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | - |
| `EMAIL_PORT` | SMTP port | `25` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `weblate_postgres_data` | PostgreSQL database files |
| `weblate_app_data` | Weblate data (repos, media, cache) |

## Post-Deployment

1. **Wait for initialization** - First startup takes several minutes (migrations, search index)
2. **Access Weblate** at `https://weblate.example.com`
3. **Login as admin** using credentials from `weblate.env`
4. **Configure projects** and connect version control repositories
5. **Set up notifications** and translation workflows

### Initial Setup Checklist

- [ ] Configure SMTP for email notifications
- [ ] Set up Git/SSH keys for repository access
- [ ] Create translation projects and components
- [ ] Configure quality checks and review workflow
- [ ] Set up backup schedule for data volume

## Common Operations

### Using bc CLI

```bash
bc weblate logs -f     # View logs
bc weblate restart     # Restart
bc weblate down        # Stop
bc weblate update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/weblate:latest --env-file .env.weblate"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d

# Run management command
dc exec weblate weblate migrate
```

## Troubleshooting

### Slow startup
First boot can take 2-5 minutes for database migrations and search index creation. Check progress with:
```bash
dc logs -f weblate
```

### Email not sending
Verify SMTP settings in `weblate.env` and test with:
```bash
dc exec weblate weblate sendtestemail admin@example.com
```

### Git push/pull failures
Ensure SSH keys are properly configured and the Git host is trusted:
```bash
dc exec weblate ssh-keyscan github.com >> /app/data/home/.ssh/known_hosts
```

### Container not healthy
Check logs with `dc logs weblate` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.weblate.org/)
- [Docker Hub](https://hub.docker.com/r/weblate/weblate)
- [GitHub](https://github.com/WeblateOrg/weblate)
