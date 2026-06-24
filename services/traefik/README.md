# Traefik

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Cloud-native reverse proxy and load balancer with automatic HTTPS via Let's Encrypt and CloudFlare DNS-01 challenge.

**For Cloudflare Tunnel deployments, use [traefik-tunnel](../traefik-tunnel/) instead.**

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.traefik << 'EOF'
COMPOSE_PROJECT_NAME=traefik
TRAEFIK_DOMAIN=traefik.example.com
TRAEFIK_EMAIL=admin@example.com
TRAEFIK_AUTH=admin:$$apr1$$your_hashed_password
CLOUDFLARE_EMAIL=admin@example.com
CLOUDFLARE_API_KEY=your_cloudflare_api_key
EOF

# 2. Deploy
bc traefik up

# 3. Check status
bc traefik ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.traefik << 'EOF'
COMPOSE_PROJECT_NAME=traefik
TRAEFIK_DOMAIN=traefik.example.com
TRAEFIK_EMAIL=admin@example.com
TRAEFIK_AUTH=admin:$$apr1$$your_hashed_password
CLOUDFLARE_EMAIL=admin@example.com
CLOUDFLARE_API_KEY=your_cloudflare_api_key
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/traefik:latest --env-file .env.traefik up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/traefik:latest --env-file .env.traefik ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- CloudFlare account with API access for DNS-01 challenge
- Domain with DNS managed by CloudFlare

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| traefik | traefik:v3.7 | Reverse proxy and load balancer |
| traefik-init | alpine:3.24 | Configuration generator (runs once) |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `CLOUDFLARE_EMAIL` | CloudFlare account email | `admin@example.com` |
| `CLOUDFLARE_API_KEY` | CloudFlare Global API key | `your_api_key` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPOSE_PROJECT_NAME` | `traefik` | Docker Compose project name |
| `TRAEFIK_VERSION` | `v3.7` | Traefik image version |
| `TRAEFIK_DOMAIN` | `traefik.example.com` | Domain for Traefik dashboard |
| `TRAEFIK_EMAIL` | Uses `CLOUDFLARE_EMAIL` | Email for Let's Encrypt notifications |
| `TRAEFIK_AUTH` | `admin:$$apr1$$changeme` | Basic auth for dashboard (htpasswd format) |

### Port Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TRAEFIK_HTTP_PORT` | `80` | HTTP port |
| `TRAEFIK_HTTPS_PORT` | `443` | HTTPS port |
| `TRAEFIK_DASHBOARD_PORT` | `8080` | Dashboard port |

### Generating Dashboard Credentials

```bash
# Using htpasswd (install: apt install apache2-utils)
htpasswd -nb admin your_password | sed 's/\$/\$\$/g'

# Or using Docker (no install needed)
docker run --rm httpd:alpine htpasswd -nb admin your_password | sed 's/\$/\$\$/g'

# Example output (copy this to TRAEFIK_AUTH):
# admin:$$apr1$$xyz123$$abcdefghijklmnop
```

## Volumes

| Volume | Purpose |
|--------|---------|
| `traefik_config` | Traefik configuration files |
| `traefik_acme_data` | Let's Encrypt certificates |
| `traefik_logs_data` | Access and error logs |

## Ports

| Port | Purpose |
|------|---------|
| 80 | HTTP (redirects to HTTPS) |
| 443 | HTTPS |
| 8080 | Traefik dashboard |

## Common Operations

### Using bc CLI

```bash
bc traefik logs -f     # View logs
bc traefik restart     # Restart
bc traefik down        # Stop
bc traefik update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/traefik:latest --env-file .env.traefik"

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

### Certificate not issuing

Check CloudFlare API credentials and ensure the domain's DNS is managed by CloudFlare:
```bash
dc logs traefik | grep -i acme
```

### Dashboard 401 Unauthorized

Verify `TRAEFIK_AUTH` is properly escaped (double `$$` in compose files) and matches htpasswd format.

### Services not discovered

Ensure services have `traefik.enable=true` label and are connected to `traefik_default` network.

## Cloudflare Tunnel

For deployments behind Cloudflare Tunnel (no public port exposure), use [traefik-tunnel](../traefik-tunnel/) instead:

```bash
docker compose -f oci://ghcr.io/beevelop/traefik-tunnel:latest --env-file .env.traefik up -d
```

## Links

- [Official Documentation](https://doc.traefik.io/traefik/)
- [Docker Hub](https://hub.docker.com/_/traefik)
- [GitHub](https://github.com/traefik/traefik)
