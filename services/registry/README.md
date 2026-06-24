# Registry

> **OCI Artifact** - Deploy directly from GitHub Container Registry

A private Docker registry for storing and distributing container images within your infrastructure.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.registry << 'EOF'
COMPOSE_PROJECT_NAME=registry
SERVICE_DOMAIN=registry.example.com
REGISTRY_VERSION=3.1.1
EOF

# 2. Deploy
bc registry up

# 3. Check status
bc registry ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.registry << 'EOF'
COMPOSE_PROJECT_NAME=registry
SERVICE_DOMAIN=registry.example.com
REGISTRY_VERSION=3.1.1
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/registry:latest --env-file .env.registry up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/registry:latest --env-file .env.registry ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| registry | registry:3.1.1 | Docker Registry v2 API server |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for the registry | `registry.example.com` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `registry` |
| `REGISTRY_VERSION` | Registry image version | `3.1.1` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `registry_data` | Container image layers and manifests |
| `registry_auth` | htpasswd authentication file |

## Post-Deployment

### Create Authentication Credentials

The registry uses htpasswd authentication. Create credentials before pushing images:

```bash
# Install htpasswd (if not available)
# apt-get install apache2-utils

# Create htpasswd file
docker exec -it registry sh -c "htpasswd -Bbn myuser Swordfish > /auth/htpasswd"

# Or add additional users
docker exec -it registry sh -c "htpasswd -Bb /auth/htpasswd anotheruser Swordfish"
```

### Test the Registry

```bash
# Login to the registry
docker login registry.example.com -u myuser

# Tag and push an image
docker tag alpine:latest registry.example.com/alpine:latest
docker push registry.example.com/alpine:latest

# Pull the image
docker pull registry.example.com/alpine:latest
```

## Common Operations

### Using bc CLI

```bash
bc registry logs -f     # View logs
bc registry restart     # Restart
bc registry down        # Stop
bc registry update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/registry:latest --env-file .env.registry"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

### Garbage Collection

Remove unreferenced blobs to reclaim disk space:

```bash
docker exec -it registry bin/registry garbage-collect /etc/docker/registry/config.yml
```

## Troubleshooting

### Authentication Failed

Ensure the htpasswd file exists and has correct permissions:

```bash
docker exec -it registry cat /auth/htpasswd
```

### Push Denied / Unauthorized

Verify you're logged in and the user exists in htpasswd:

```bash
docker login registry.example.com
```

### Container not healthy

Check logs with `dc logs registry` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.docker.com/registry/)
- [Docker Hub](https://hub.docker.com/_/registry)
- [GitHub](https://github.com/distribution/distribution)
