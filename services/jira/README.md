# Jira Software

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Atlassian Jira Software is a proprietary issue tracking and project management tool for agile teams.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.jira << 'EOF'
COMPOSE_PROJECT_NAME=jira
SERVICE_DOMAIN=jira.example.com
POSTGRES_PASS=Swordfish
EOF

# 2. Deploy
bc jira up

# 3. Check status
bc jira ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.jira << 'EOF'
COMPOSE_PROJECT_NAME=jira
SERVICE_DOMAIN=jira.example.com
POSTGRES_PASS=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/jira:latest --env-file .env.jira up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/jira:latest --env-file .env.jira ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))
- Minimum 4GB RAM recommended for Jira

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | jira-postgres | Issue tracking data storage |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| jira | atlassian/jira-software | Jira Software application |
| jira-postgres | postgres:17-alpine | PostgreSQL database |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Jira access | `jira.example.com` |
| `POSTGRES_PASS` | PostgreSQL password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `jira` |
| `POSTGRES_USER` | PostgreSQL username | `jira` |
| `POSTGRES_DB` | PostgreSQL database name | `jira` |
| `JVM_MINIMUM_MEMORY` | JVM minimum heap size | `1024m` |
| `JVM_MAXIMUM_MEMORY` | JVM maximum heap size | `2048m` |
| `JIRA_VERSION` | Jira Software image tag | `11.3.7-ubi9-jdk21` |
| `POSTGRES_TAG` | PostgreSQL image tag | `17-alpine` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `jira_app_data` | Jira application data and attachments |
| `jira_postgres_data` | PostgreSQL database files |

## Post-Deployment

1. **Access Jira**: Navigate to `https://jira.example.com`
2. **Setup Wizard**: Complete the initial setup wizard
3. **License**: Enter your Jira Software license key (trial or purchased from Atlassian)
4. **Administrator Account**: Create your first admin user
5. **Initial Configuration**: Configure mail server, LDAP, and other integrations as needed

## Common Operations

### Using bc CLI

```bash
bc jira logs -f     # View logs
bc jira restart     # Restart
bc jira down        # Stop
bc jira update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/jira:latest --env-file .env.jira"

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

### Jira takes a long time to start
Jira has a `start_period` of 180 seconds. This is normal for initial startup as it needs to initialize the database and build indexes.

### Out of memory errors
Increase `JVM_MAXIMUM_MEMORY` in your environment file. Recommended minimum is 2GB for production use.

### Database connection issues
Ensure PostgreSQL container is healthy before Jira starts. Check with `docker logs jira-postgres`.

### Container not healthy
Check logs with `dc logs jira` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://confluence.atlassian.com/jirasoftware)
- [Docker Hub](https://hub.docker.com/r/atlassian/jira-software)
- [Atlassian Support](https://support.atlassian.com/jira-software-cloud/)
