# TUS (tusd)

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Open protocol and reference server for resumable file uploads. Tusd is the official reference implementation of the tus resumable upload protocol.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.tus << 'EOF'
COMPOSE_PROJECT_NAME=tus
SERVICE_DOMAIN=tus.example.com
EOF

# 2. Deploy
bc tus up

# 3. Check status
bc tus ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.tus << 'EOF'
COMPOSE_PROJECT_NAME=tus
SERVICE_DOMAIN=tus.example.com
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/tus:latest --env-file .env.tus up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/tus:latest --env-file .env.tus ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| tus | tusproject/tusd:v2.10.0 | TUS upload server |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for the TUS server | `tus.example.com` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `tus` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `tus_app_data` | Uploaded file storage |

## Post-Deployment

1. Access the TUS server at `https://tus.example.com`
2. Test uploads using a TUS client library or the official tus-js-client
3. Configure hooks for post-upload processing (optional)

### Testing Upload

```bash
# Test with curl
curl -X POST https://tus.example.com/files \
  -H "Tus-Resumable: 1.0.0" \
  -H "Upload-Length: 100"
```

### Custom Hooks

Mount a hooks directory to `/srv/tusd-hooks` for custom post-upload processing:
- `pre-create` - Before upload starts
- `post-create` - After upload slot created
- `post-finish` - After upload completes
- `post-terminate` - After upload terminated

## Common Operations

### Using bc CLI

```bash
bc tus logs -f     # View logs
bc tus restart     # Restart
bc tus down        # Stop
bc tus update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/tus:latest --env-file .env.tus"

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

### CORS errors
Ensure your application's domain is allowed. You may need to add CORS headers via Traefik middleware.

### Upload fails at specific size
Check available disk space on the volume and server memory limits.

### Container not healthy
Check logs with `dc logs tus` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://tus.io/)
- [Docker Hub](https://hub.docker.com/r/tusproject/tusd)
- [GitHub](https://github.com/tus/tusd)
- [TUS Protocol Specification](https://tus.io/protocols/resumable-upload.html)
