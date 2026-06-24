# Traefik Tunnel

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Traefik reverse proxy configured for **Cloudflare Tunnel mode only**. No ports are exposed to the host - all traffic flows through Cloudflare Tunnel via cloudflared.

## Why Traefik-Tunnel?

This is a dedicated, security-hardened configuration for Cloudflare Tunnel deployments:

| Feature | traefik (exposed) | traefik-tunnel |
|---------|-------------------|----------------|
| Ports exposed | 80, 443, 8080 | **None** |
| TLS provider | Let's Encrypt | Cloudflare Edge |
| Internet accessible | Yes | No (tunnel only) |
| Requires CloudFlare API | Yes | No |

## Architecture

```
Internet -> Cloudflare Edge (TLS) -> cloudflared -> traefik:80 -> Services
                                          |
                               (Docker internal network only)
```

- **No host ports exposed** - Traefik only listens on Docker's internal network
- **cloudflared** connects to `http://traefik:80` via Docker network
- **TLS terminated at Cloudflare Edge** - No certificate management needed
- **Existing service labels work unchanged** - `websecure` entrypoint maps to port 80

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.traefik-tunnel << 'EOF'
CF_TUNNEL_TOKEN=your_tunnel_token_here
SERVICE_DOMAIN=app.example.com
EOF

# 2. Deploy Traefik (tunnel mode)
bc traefik-tunnel up

# 3. Deploy cloudflared
bc cloudflared up

# 4. Deploy your service (e.g., Metabase)
bc metabase up
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.traefik-tunnel << 'EOF'
CF_TUNNEL_TOKEN=your_tunnel_token_here
SERVICE_DOMAIN=app.example.com
EOF

# 2. Deploy Traefik (tunnel mode)
docker compose -f oci://ghcr.io/beevelop/traefik-tunnel:latest --env-file .env.traefik-tunnel up -d --pull always

# 3. Deploy cloudflared
docker compose -f oci://ghcr.io/beevelop/cloudflared:latest --env-file .env.traefik-tunnel up -d --pull always

# 4. Deploy your service (e.g., Metabase)
docker compose -f oci://ghcr.io/beevelop/metabase:latest --env-file .env.metabase up -d --pull always
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Cloudflare Tunnel configured in Zero Trust Dashboard

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPOSE_PROJECT_NAME` | `traefik` | Docker Compose project name |
| `TRAEFIK_VERSION` | `v3.7` | Traefik image version |
| `TRAEFIK_DOMAIN` | `traefik.example.com` | Domain for dashboard (via tunnel) |
| `TRAEFIK_AUTH` | `admin:$$apr1$$changeme` | Basic auth for dashboard |

### Generating Dashboard Credentials

```bash
docker run --rm httpd:alpine htpasswd -nb admin your_password | sed 's/\$/\$\$/g'
```

## Volumes

| Volume | Purpose |
|--------|---------|
| `traefik_config` | Traefik configuration files |
| `traefik_logs_data` | Access and error logs |

## Cloudflare Tunnel Configuration

In Zero Trust Dashboard (https://one.dash.cloudflare.com) → Networks → Tunnels → Public Hostname:

| Subdomain | Domain | Type | URL |
|-----------|--------|------|-----|
| app | example.com | HTTP | traefik:80 |
| traefik | example.com | HTTP | traefik:80 |

> **Important:** Use `HTTP` type and `traefik:80` as the URL. TLS is handled by Cloudflare Edge, not Traefik.

## Service Labels

Service labels are identical for both traefik modes. TLS is handled at the entrypoint level:

- **Exposed mode:** Let's Encrypt via `certResolver: letsencrypt` at entrypoint
- **Tunnel mode:** No TLS (Cloudflare Edge handles it)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
  - "traefik.docker.network=traefik_default"
```

> **Note:** Do NOT include `tls=true` or `tls.certresolver` labels. TLS configuration is managed at the Traefik entrypoint level, ensuring services work in both exposed and tunnel modes without modification.

## Common Operations

### Using bc CLI

```bash
bc traefik-tunnel logs -f     # View logs
bc traefik-tunnel restart     # Restart
bc traefik-tunnel down        # Stop
bc traefik-tunnel update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias
alias dc="docker compose -f oci://ghcr.io/beevelop/traefik-tunnel:latest --env-file .env.traefik-tunnel"

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

### cloudflared can't reach Traefik

Ensure both services are on the same Docker network (`traefik_default`):

```bash
docker network inspect traefik_default
```

### Services not discovered

Ensure services have `traefik.enable=true` label and are connected to `traefik_default` network.

### Dashboard not accessible

1. Add a public hostname in Cloudflare Tunnel for the dashboard domain
2. Verify `TRAEFIK_AUTH` is properly escaped (double `$$`)

## Comparison with traefik (exposed)

Use **traefik-tunnel** when:
- Deploying behind Cloudflare Tunnel
- You want zero public port exposure
- You don't need direct Let's Encrypt certificates

Use **traefik** (exposed) when:
- You need direct internet access to ports 80/443
- You're using Let's Encrypt with DNS-01 challenge
- You're not using Cloudflare Tunnel

## Links

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [traefik (exposed mode)](../traefik/)
