# Cloudflare Tunnel (cloudflared)

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Secure tunnel connector that routes traffic from Cloudflare's edge network to your services without exposing ports to the public internet. Enables zero-trust access via Cloudflare WARP and Access policies.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Overview

Cloudflare Tunnel creates an encrypted outbound-only connection from your infrastructure to Cloudflare's network. This eliminates the need to expose ports 80/443 to the internet, providing:

- **Zero-trust security**: Services hidden from public internet
- **DDoS protection**: Cloudflare absorbs attacks at the edge
- **Access control**: Require WARP client or identity verification
- **No firewall rules**: Outbound-only connections, no port forwarding needed

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLOUDFLARE EDGE                             │
├─────────────────────────────────────────────────────────────────┤
│  Public Hostnames (configured in Dashboard)                     │
│     │                                                           │
│     ├─► Access Policy: "Allow All" ──► Public Services          │
│     │                                                           │
│     └─► Access Policy: "WARP Only" ──► Protected Services       │
│                    (requires enrolled device)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ Encrypted Tunnel
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                      DOCKER HOST                                │
│                                                                 │
│   ┌─────────────┐  http://traefik:80  ┌──────────────────────┐ │
│   │ cloudflared │────────────────────►│      Traefik         │ │
│   │  container  │                     │ (label discovery)    │ │
│   └─────────────┘                     └──────────┬───────────┘ │
│                                                  │              │
│         ┌────────────────────────────────────────┤              │
│         ▼                ▼                       ▼              │
│    ┌─────────┐    ┌───────────┐           ┌───────────┐        │
│    │ GitLab  │    │ Metabase  │    ...    │  Service  │        │
│    └─────────┘    └───────────┘           └───────────┘        │
│                                                                 │
│    Network: traefik_default                                     │
└────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Step 1: Create Tunnel in Cloudflare Dashboard

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com)
2. Navigate to **Networks** → **Connectors**
3. Click **Create a connector** → **Cloudflared**
4. Name your tunnel (e.g., `beecompose-production`)
5. Copy the **tunnel token** from the install command

### Step 2: Configure Published Application Routes

In the connector configuration, add **Published application routes**:

| Public Hostname | Service | Notes |
|-----------------|---------|-------|
| `*.example.com` | `http://traefik:80` | Wildcard routes all to Traefik |

Or configure per-service for granular Access policies:

| Public Hostname | Service | Access Policy |
|-----------------|---------|---------------|
| `gitlab.example.com` | `http://traefik:80` | Allow All |
| `admin.example.com` | `http://traefik:80` | Require WARP |
| `*.example.com` | `http://traefik:80` | Bypass (catch-all) |

### Step 3: Deploy cloudflared

#### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.cloudflared << 'EOF'
COMPOSE_PROJECT_NAME=cloudflared
CF_TUNNEL_TOKEN=eyJhIjoiYWJjZGVmMTIzNDU2Nzg5MCIsInQiOiJ5b3VyLXR1bm5lbC1pZCIsInMiOiJ5b3VyLXNlY3JldCJ9
EOF

# 2. Deploy
bc cloudflared up

# 3. Check status
bc cloudflared ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

#### Manual Deployment

```bash
# 1. Create environment file
cat > .env.cloudflared << 'EOF'
COMPOSE_PROJECT_NAME=cloudflared
CF_TUNNEL_TOKEN=eyJhIjoiYWJjZGVmMTIzNDU2Nzg5MCIsInQiOiJ5b3VyLXR1bm5lbC1pZCIsInMiOiJ5b3VyLXNlY3JldCJ9
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/cloudflared:latest --env-file .env.cloudflared up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/cloudflared:latest --env-file .env.cloudflared ps
```

### Step 4: Enable Tunnel-Only Mode for Traefik (Optional)

For maximum security, disable direct port exposure on Traefik:

```bash
cd ../traefik

# Deploy with tunnel-only override
docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Cloudflare account with Zero Trust (free tier available)
- Domain with DNS managed by Cloudflare
- [Traefik](../traefik/) deployed and running

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `CF_TUNNEL_TOKEN` | Tunnel token from Cloudflare Dashboard | `eyJhIjoiYWJj...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `cloudflared` |
| `CLOUDFLARED_VERSION` | cloudflared image version | `2026.6.1` |

## Deployment Modes

### Mode 1: Standard (Public + Tunnel)

Both direct internet access and tunnel access work. Good for migration or redundancy.

```bash
# Traefik: normal deployment
cd services/traefik
docker compose up -d

# Cloudflared: add tunnel access
cd ../cloudflared
docker compose up -d
```

Traffic can reach services via:
- Direct: `https://service.example.com` → Your IP:443 → Traefik
- Tunnel: `https://service.example.com` → Cloudflare → cloudflared → Traefik

### Mode 2: Tunnel-Only (Recommended for Production)

All traffic forced through Cloudflare Tunnel. Maximum security.

```bash
# Cloudflared: must be running
cd services/cloudflared
docker compose up -d

# Traefik: tunnel-only mode (no public ports)
cd ../traefik
docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d
```

Traffic can only reach services via:
- Tunnel: `https://service.example.com` → Cloudflare → cloudflared → Traefik

## Access Policies

Configure in Cloudflare Zero Trust Dashboard under **Access** → **Applications**.

### Public Services

Allow anyone to access (still protected by Cloudflare WAF/DDoS):

1. Create Application → Self-hosted
2. Application domain: `gitlab.example.com`
3. Policy: **Allow** → **Everyone**

### WARP-Protected Services

Require users to have WARP client connected:

1. Create Application → Self-hosted
2. Application domain: `admin.example.com`
3. Policy: **Allow** → **Emails ending in** `@yourcompany.com`
4. Enable: **Require WARP**

### Identity-Based Access

Require authentication via IdP:

1. Create Application → Self-hosted
2. Application domain: `internal.example.com`
3. Configure IdP integration (Google, Okta, GitHub, etc.)
4. Policy: **Allow** → **Emails** `user@yourcompany.com`

## Common Operations

### Using bc CLI

```bash
bc cloudflared logs -f     # View logs
bc cloudflared restart     # Restart
bc cloudflared down        # Stop
bc cloudflared update      # Pull and recreate
bc cloudflared exec cloudflared cloudflared tunnel info  # Check tunnel status
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/cloudflared:latest --env-file .env.cloudflared"

# View logs
dc logs -f

# Check tunnel status
dc exec cloudflared cloudflared tunnel info

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

## Health Checks

The container includes a built-in health check that verifies tunnel connectivity:

```bash
# Check container health
docker inspect cloudflared --format='{{.State.Health.Status}}'

# View health check logs
docker inspect cloudflared --format='{{range .State.Health.Log}}{{.Output}}{{end}}'
```

## Troubleshooting

### Tunnel not connecting

1. Verify token is correct:
   ```bash
   echo $CF_TUNNEL_TOKEN | base64 -d
   ```

2. Check cloudflared logs:
   ```bash
   dc logs -f cloudflared
   ```

3. Verify tunnel status in Cloudflare Dashboard

### Services not accessible via tunnel

1. Ensure Traefik is running and healthy
2. Verify public hostname points to `http://traefik:80`
3. Check that cloudflared is on `traefik_default` network:
   ```bash
   docker network inspect traefik_default
   ```

### Access policy blocking requests

1. Check Access logs in Cloudflare Dashboard
2. Verify WARP client is connected (if required)
3. Test with policy temporarily set to "Allow Everyone"

### Container not healthy

Check logs and ensure the tunnel token is valid:
```bash
dc logs cloudflared
```

## Security Considerations

### What's Protected

- No public ports exposed (in tunnel-only mode)
- All traffic encrypted between Cloudflare and your server
- DDoS attacks absorbed at Cloudflare edge
- Bot protection and WAF rules apply

### What You Should Configure

- **Access Policies**: Define who can reach each service
- **Device Posture**: Require managed devices, OS versions, etc.
- **Session Duration**: Set appropriate session timeouts
- **Audit Logs**: Monitor access in Cloudflare Dashboard

### Best Practices

1. Use wildcard hostname (`*.example.com`) routing to Traefik
2. Configure Access policies per-application in Cloudflare
3. Require WARP for sensitive internal tools
4. Enable audit logging for compliance
5. Rotate tunnel tokens periodically

## Migration Guide

### From Direct Exposure to Tunnel-Only

1. **Deploy cloudflared** alongside existing Traefik
2. **Configure public hostnames** in Cloudflare Dashboard
3. **Test tunnel access** works for all services
4. **Update DNS** to point to Cloudflare (orange cloud)
5. **Switch Traefik to tunnel-only mode**:
   ```bash
   cd services/traefik
   docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d
   ```
6. **Update firewall** to block ports 80/443 from public

### Rollback

To restore direct access:

```bash
cd services/traefik
docker compose up -d  # Without tunnel override
```

## Links

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Cloudflare Zero Trust](https://developers.cloudflare.com/cloudflare-one/)
- [cloudflared on Docker Hub](https://hub.docker.com/r/cloudflare/cloudflared)
- [Cloudflare WARP Client](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/)
- [Access Policies](https://developers.cloudflare.com/cloudflare-one/policies/access/)
