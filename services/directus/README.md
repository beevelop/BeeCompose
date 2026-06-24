# Directus

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Directus is an open-source data platform that wraps any SQL database with a real-time GraphQL+REST API, intuitive admin app, and customizable data studio.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.directus << 'EOF'
COMPOSE_PROJECT_NAME=directus
SERVICE_DOMAIN=directus.example.com
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Swordfish
DB_PASS=Swordfish
DB_ROOT_PASS=Swordfish
EOF

# 2. Deploy
bc directus up

# 3. Check status
bc directus ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.directus << 'EOF'
COMPOSE_PROJECT_NAME=directus
SERVICE_DOMAIN=directus.example.com
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Swordfish
DB_PASS=Swordfish
DB_ROOT_PASS=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/directus:latest --env-file .env.directus up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/directus:latest --env-file .env.directus ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| MySQL | directus-mysql | Data storage |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| directus | directus/directus:12.0.2 | Headless CMS / Data Platform |
| directus-mysql | mysql:8.4 | MySQL database backend |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Traefik routing | `directus.example.com` |
| `ADMIN_EMAIL` | Admin user email address | `admin@example.com` |
| `ADMIN_PASSWORD` | Admin user password | `Swordfish` |
| `DB_PASS` | MySQL user password | `Swordfish` |
| `DB_ROOT_PASS` | MySQL root password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `directus` |
| `DB_USER` | MySQL database user | `directus` |
| `DB_NAME` | MySQL database name | `directus` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `directus_uploads` | User uploaded files and assets |
| `directus_extensions` | Custom extensions and hooks |
| `mysql_data` | MySQL database persistence |

## Post-Deployment

1. **Access the Admin Panel**: Navigate to `https://directus.example.com`
2. **Login**: Use the `ADMIN_EMAIL` and `ADMIN_PASSWORD` credentials
3. **Create Collections**: Start building your data model through the admin interface
4. **Configure Roles**: Set up roles and permissions for API access
5. **Generate API Token**: Create static tokens for external integrations

## Common Operations

### Using bc CLI

```bash
bc directus logs -f     # View logs
bc directus restart     # Restart
bc directus down        # Stop
bc directus update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/directus:latest --env-file .env.directus"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

## Troubleshooting

### Database connection failed
Ensure the MySQL container is healthy before Directus starts. Check MySQL logs:
```bash
dc logs directus-mysql
```

### Admin login not working
Verify `ADMIN_EMAIL` and `ADMIN_PASSWORD` are correctly set. These are only used during initial setup.

### Container not healthy
Check logs with `dc logs directus` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.directus.io/)
- [Docker Hub](https://hub.docker.com/r/directus/directus)
- [GitHub](https://github.com/directus/directus)
