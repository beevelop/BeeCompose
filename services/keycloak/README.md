# Keycloak

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Keycloak is an open-source identity and access management solution providing single sign-on (SSO), user federation, identity brokering, and social login.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.keycloak << 'EOF'
COMPOSE_PROJECT_NAME=keycloak
SERVICE_DOMAIN=keycloak.example.com
POSTGRES_PASS=Swordfish
KEYCLOAK_USER=admin
KEYCLOAK_PASSWORD=Swordfish
EOF

# 2. Deploy
bc keycloak up

# 3. Check status
bc keycloak ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.keycloak << 'EOF'
COMPOSE_PROJECT_NAME=keycloak
SERVICE_DOMAIN=keycloak.example.com
POSTGRES_PASS=Swordfish
KEYCLOAK_USER=admin
KEYCLOAK_PASSWORD=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/keycloak:latest --env-file .env.keycloak up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/keycloak:latest --env-file .env.keycloak ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | keycloak-postgres | Identity data storage |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| keycloak | quay.io/keycloak/keycloak | Keycloak identity server |
| keycloak-postgres | postgres:17 | PostgreSQL database |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Keycloak access | `keycloak.example.com` |
| `POSTGRES_PASS` | PostgreSQL password | `Swordfish` |
| `KEYCLOAK_USER` | Keycloak admin username | `admin` |
| `KEYCLOAK_PASSWORD` | Keycloak admin password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `keycloak` |
| `POSTGRES_DB` | PostgreSQL database name | `keycloak` |
| `POSTGRES_USER` | PostgreSQL username | `keycloak` |
| `KEYCLOAK_VERSION` | Keycloak image tag | `26.6.3` |
| `POSTGRES_VERSION` | PostgreSQL image tag | `17` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `keycloak_postgres_data` | PostgreSQL database files |

## Post-Deployment

1. **Access Admin Console**: Navigate to `https://keycloak.example.com`
2. **Login**: Use the admin credentials configured in `KEYCLOAK_USER` and `KEYCLOAK_PASSWORD`
3. **Create Realm**: Create a new realm for your applications (or use the master realm for testing)
4. **Configure Clients**: Add OAuth2/OIDC clients for your applications
5. **User Federation**: Configure LDAP or other identity providers if needed

## Common Operations

### Using bc CLI

```bash
bc keycloak logs -f     # View logs
bc keycloak restart     # Restart
bc keycloak down        # Stop
bc keycloak update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/keycloak:latest --env-file .env.keycloak"

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

### Keycloak not starting
Keycloak has a `start_period` of 90 seconds. Wait for the container to become healthy. Check logs with `docker logs keycloak`.

### Cannot access admin console
Ensure `KC_PROXY=edge` is set (default in this configuration) when running behind a reverse proxy like Traefik.

### Database connection errors
Verify PostgreSQL is running and healthy: `docker logs keycloak-postgres`

### Container not healthy
Check logs with `dc logs keycloak` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://www.keycloak.org/documentation)
- [Keycloak Guides](https://www.keycloak.org/guides)
- [GitHub](https://github.com/keycloak/keycloak)
