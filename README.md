# BeeCompose

**Production-ready Docker Compose stacks, published as OCI artifacts.**

BeeCompose provides curated Docker Compose configurations for 30+ self-hosted services. Each service is published as an OCI artifact to GitHub Container Registry, enabling one-command deployment without cloning repositories.

> **Note:** This README appears on all package pages because GitHub Container Registry
> doesn't support per-package READMEs. For detailed documentation, see the service-specific
> README linked in the table below.

## Select a Service to Deploy

Click on a service name to view its detailed README with configuration options, environment variables, and deployment instructions.

| Service | Description | OCI Artifact |
|---------|-------------|--------------|
| [bitwarden](services/bitwarden/README.md) | Self-hosted password manager (Vaultwarden) | `ghcr.io/beevelop/bitwarden` |
| [cabot](services/cabot/README.md) | Monitoring and alerting platform | `ghcr.io/beevelop/cabot` |
| [claude-code](services/claude-code/README.md) | Remote Claude Code instance with remote control | `ghcr.io/beevelop/claude-code` |
| [cloudflared](services/cloudflared/README.md) | Cloudflare Tunnel for zero-trust access | `ghcr.io/beevelop/cloudflared` |
| [confluence](services/confluence/README.md) | Atlassian team collaboration and wiki | `ghcr.io/beevelop/confluence` |
| [crowd](services/crowd/README.md) | Atlassian SSO and identity management | `ghcr.io/beevelop/crowd` |
| [dependency-track](services/dependency-track/README.md) | OWASP component analysis platform | `ghcr.io/beevelop/dependency-track` |
| [directus](services/directus/README.md) | Headless CMS and REST/GraphQL API | `ghcr.io/beevelop/directus` |
| [duckling](services/duckling/README.md) | NLP text parser for structured data | `ghcr.io/beevelop/duckling` |
| [gitlab](services/gitlab/README.md) | Complete DevOps platform with CI/CD | `ghcr.io/beevelop/gitlab` |
| [graylog](services/graylog/README.md) | Centralized log management | `ghcr.io/beevelop/graylog` |
| [huginn](services/huginn/README.md) | Self-hosted IFTTT/Zapier alternative | `ghcr.io/beevelop/huginn` |
| [jira](services/jira/README.md) | Atlassian issue tracking and projects | `ghcr.io/beevelop/jira` |
| [keycloak](services/keycloak/README.md) | Identity and access management | `ghcr.io/beevelop/keycloak` |
| [metabase](services/metabase/README.md) | Business intelligence and analytics | `ghcr.io/beevelop/metabase` |
| [minio](services/minio/README.md) | S3-compatible object storage | `ghcr.io/beevelop/minio` |
| [monica](services/monica/README.md) | Personal relationship management | `ghcr.io/beevelop/monica` |
| [mysql](services/mysql/README.md) | MySQL database server | `ghcr.io/beevelop/mysql` |
| [n8n](services/n8n/README.md) | Workflow automation platform | `ghcr.io/beevelop/n8n` |
| [nexus](services/nexus/README.md) | Sonatype artifact repository manager | `ghcr.io/beevelop/nexus` |
| [openvpn](services/openvpn/README.md) | VPN server (UDP and TCP) | `ghcr.io/beevelop/openvpn` |
| [phpmyadmin](services/phpmyadmin/README.md) | MySQL web administration | `ghcr.io/beevelop/phpmyadmin` |
| [redash](services/redash/README.md) | Data visualization and dashboards | `ghcr.io/beevelop/redash` |
| [registry](services/registry/README.md) | Private Docker registry | `ghcr.io/beevelop/registry` |
| [rundeck](services/rundeck/README.md) | Job scheduler and runbook automation | `ghcr.io/beevelop/rundeck` |
| [sentry](services/sentry/README.md) | Error tracking and performance monitoring | `ghcr.io/beevelop/sentry` |
| [shields](services/shields/README.md) | Self-hosted badge generation | `ghcr.io/beevelop/shields` |
| [sonarqube](services/sonarqube/README.md) | Code quality inspection | `ghcr.io/beevelop/sonarqube` |
| [statping](services/statping/README.md) | Status page and uptime monitoring | `ghcr.io/beevelop/statping` |
| [traefik](services/traefik/README.md) | Reverse proxy with automatic HTTPS | `ghcr.io/beevelop/traefik` |
| [traefik-tunnel](services/traefik-tunnel/README.md) | Traefik for Cloudflare Tunnel (no exposed ports) | `ghcr.io/beevelop/traefik-tunnel` |
| [tus](services/tus/README.md) | Resumable file upload server | `ghcr.io/beevelop/tus` |
| [weblate](services/weblate/README.md) | Continuous localization platform | `ghcr.io/beevelop/weblate` |
| [zabbix](services/zabbix/README.md) | Enterprise monitoring solution | `ghcr.io/beevelop/zabbix` |

## Quick Start

### Using bc CLI Helper (Recommended)

Install the `bc` CLI helper for the best experience:

```bash
# Install bc CLI
curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash

# Create environment file
cat > .env.metabase << 'EOF'
COMPOSE_PROJECT_NAME=metabase
SERVICE_DOMAIN=metabase.example.com
DB_PASS=your-secure-password
EOF

# Deploy
bc metabase up

# Check status
bc metabase ps

# View logs
bc metabase logs -f

# Stop
bc metabase down
```

The `bc` CLI wraps Docker Compose with opinionated defaults - it always pulls the latest images and automatically uses `.env.<service>` files.

> **Note:** The `bc` CLI is optional. You can always use `docker compose` directly as shown below.

### Deploy from GHCR (Manual)

Deploy any service directly from GitHub Container Registry without cloning the repository:

```bash
# 1. Create your environment file (check service README for required variables)
cat > .env << 'EOF'
COMPOSE_PROJECT_NAME=gitlab
SERVICE_DOMAIN=gitlab.example.com
DB_PASS=your-secure-password
# ... see service README for all options
EOF

# 2. Deploy from OCI artifact
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env up -d

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env ps
```

### Clone and Customize

For customization or development:

```bash
git clone https://github.com/beevelop/beecompose.git
cd beecompose/services/gitlab

# Configure environment
cp .env.example .env.production
# Edit .env.production with your settings

# Deploy
docker compose --env-file .env.production up -d
```

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|-----------------|-------|
| Docker | 25.0+ | Required for OCI artifact support |
| Docker Compose | v2.24+ | Bundled with Docker Desktop |

**Optional:** CloudFlare account for DNS-01 Let's Encrypt challenge (used by Traefik).

> **Note:** OCI artifact deployment (`docker compose -f oci://...`) requires Docker 25.0 or later.
> For older Docker versions, use the "Clone and Customize" method.

## Common Operations

### Using bc CLI (Optional)

The `bc` CLI provides simplified commands for all lifecycle operations:

| Task | bc Command | Manual Equivalent |
|------|------------|-------------------|
| Start service | `bc metabase up` | `docker compose -f oci://ghcr.io/beevelop/metabase:latest --env-file .env.metabase up -d --pull always` |
| Stop service | `bc metabase down` | `docker compose -f oci://... down` |
| View logs | `bc metabase logs -f` | `docker compose -f oci://... logs -f` |
| Check status | `bc metabase ps` | `docker compose -f oci://... ps` |
| Update | `bc metabase update` | `docker compose -f oci://... pull && ... up -d` |

#### bc CLI Installation

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash

# Uninstall
curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash -s -- uninstall
```

#### Pin OCI Version

Create a `.beecompose` file to pin all services to a specific version:

```bash
# Create config
bc init v26.1.6

# Or manually
echo "BEECOMPOSE_VERSION=v26.1.6" > .beecompose
```

Override per-command with `-v`:

```bash
bc -v latest metabase up
```

### Manual Operations

| Task | Command |
|------|---------|
| Start service | `docker compose --env-file .env up -d` |
| Stop service | `docker compose --env-file .env down` |
| View logs | `docker compose --env-file .env logs -f` |
| Check status | `docker compose --env-file .env ps` |
| Update images | `docker compose --env-file .env pull && docker compose --env-file .env up -d` |

### Using OCI Artifacts

When deploying from GHCR, include the OCI URL in each command:

```bash
# Define convenience alias
alias dc="docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env"

# Now use it for all operations
dc up -d
dc logs -f
dc ps
dc down
```

## Architecture

All services are pre-configured for:

- **Traefik v3** reverse proxy with automatic Let's Encrypt SSL (DNS-01 via CloudFlare)
- **Named volumes** for data persistence (no bind mounts for OCI compatibility)
- **Health checks** for container monitoring
- **JSON logging** with size limits (500k max, 50 files)
- **Restart policy** `unless-stopped` for reliability

### Traefik Integration

Deploy Traefik first, then other services automatically connect via the `traefik_default` network:

```bash
# Deploy Traefik
docker compose -f oci://ghcr.io/beevelop/traefik:latest --env-file .env.traefik up -d

# Then deploy other services
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab up -d
```

### Networking Modes

BeeCompose supports two networking modes for Traefik. Choose based on your security requirements and infrastructure setup.

#### Traefik Exposed Mode (Direct Internet Access)

Standard deployment with ports directly exposed to the internet. Traefik handles TLS termination using Let's Encrypt certificates via CloudFlare DNS-01 challenge.

```
Internet -> Traefik:443 (TLS) -> Services
                |
        Let's Encrypt certificates
```

| Aspect | Details |
|--------|---------|
| Ports exposed | 80, 443, 8080 |
| TLS provider | Let's Encrypt (ACME DNS-01) |
| Requires | CloudFlare API credentials |
| Best for | Direct server access, traditional hosting |

```bash
# Deploy Traefik (exposed mode)
docker compose -f oci://ghcr.io/beevelop/traefik:latest --env-file .env.traefik up -d

# Deploy services
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab up -d
```

See [traefik README](services/traefik/README.md) for configuration details.

#### Traefik Tunnel Mode (Zero-Trust via Cloudflare)

Security-hardened deployment with zero public port exposure. All traffic flows through Cloudflare Tunnel, with TLS terminated at Cloudflare's edge network.

```
Internet -> Cloudflare Edge (TLS) -> cloudflared -> traefik:80 -> Services
                                          |
                              (Docker internal network only)
```

| Aspect | Details |
|--------|---------|
| Ports exposed | **None** |
| TLS provider | Cloudflare Edge |
| Requires | Cloudflare Tunnel token |
| Best for | Zero-trust security, hiding origin IP, NAT/firewall environments |

```bash
# 1. Deploy Traefik (tunnel mode - no exposed ports)
docker compose -f oci://ghcr.io/beevelop/traefik-tunnel:latest --env-file .env.traefik up -d

# 2. Deploy cloudflared (configure tunnel token in .env)
docker compose -f oci://ghcr.io/beevelop/cloudflared:latest --env-file .env.cloudflared up -d

# 3. Deploy services as normal
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab up -d
```

See [traefik-tunnel README](services/traefik-tunnel/README.md) and [cloudflared README](services/cloudflared/README.md) for setup instructions.

#### Mode Comparison

| Feature | Exposed Mode | Tunnel Mode |
|---------|--------------|-------------|
| Host ports | 80, 443, 8080 | None |
| TLS certificates | Let's Encrypt (auto-managed) | Cloudflare Edge (no management) |
| Origin IP visible | Yes | No (hidden behind Cloudflare) |
| CloudFlare API required | Yes | No |
| Tunnel token required | No | Yes |
| Service labels | Identical | Identical |

**Important:** Service labels work unchanged in both modes. Do not include `tls=true` or `tls.certresolver` in service labels - TLS is configured at the Traefik entrypoint level.

## Project Structure

```
beecompose/
├── scripts/
│   ├── bc                        # CLI helper (install system-wide)
│   ├── install.sh                # Installer for bc CLI
│   └── ...
├── services/
│   └── <service>/
│       ├── docker-compose.yml    # Compose configuration
│       ├── README.md             # Service documentation (START HERE)
│       ├── .env                  # Version tags (committed)
│       ├── .env.example          # Example configuration (committed)
│       └── .env.<environ>        # Your secrets (gitignored)
├── docs/
│   ├── BACKUP.md                 # Backup and restore procedures
│   ├── DEPLOYMENT.md             # Deployment guide
│   └── ...
└── .github/
    └── workflows/
        └── publish-oci.yml       # OCI artifact publishing
```

## Documentation

| Document | Description |
|----------|-------------|
| [Deployment Guide](docs/DEPLOYMENT.md) | Complete deployment walkthrough |
| [Backup Guide](docs/BACKUP.md) | Backup and restore procedures |
| [Testing Guide](docs/TESTING.md) | Testing procedures and validation |
| [CI/CD Pipeline](.github/CI-CD.md) | Pipeline architecture and usage |

## CI/CD

The repository includes GitHub Actions pipelines that:

1. **Lint** - Validates all docker-compose.yml files with DCLint
2. **Validate OCI** - Ensures all services are OCI-compatible (no bind mounts)
3. **CVE Scan** - Scans images for vulnerabilities using Trivy
4. **Test** - Validates each service starts correctly
5. **Publish** - Publishes OCI artifacts to GHCR on main branch

## Contributing

Pull requests are welcome! Please:

1. Follow existing docker-compose patterns
2. Include `.env.example` with placeholder values
3. Use named volumes (no bind mounts for OCI compatibility)
4. Include native Docker healthcheck directives
5. Add a comprehensive README.md for your service
6. Run DCLint before submitting

## Notes

- **Placeholder Values:** Examples use `example.com`, `bee` (username), and `Swordfish` (password)
- **OCI artifacts are compose files**, not container images - they define how to deploy services
- **Service READMEs** contain all configuration details - always check them before deploying

## License

[MIT License](LICENSE)
