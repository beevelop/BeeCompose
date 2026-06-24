# Rundeck

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Job scheduler and runbook automation platform for managing ad-hoc and routine operational tasks across your infrastructure.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.rundeck << 'EOF'
COMPOSE_PROJECT_NAME=rundeck
SERVICE_DOMAIN=rundeck.example.com
RUNDECK_ADMIN_PASSWORD=Swordfish
EOF

# 2. Deploy
bc rundeck up

# 3. Check status
bc rundeck ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.rundeck << 'EOF'
COMPOSE_PROJECT_NAME=rundeck
SERVICE_DOMAIN=rundeck.example.com
RUNDECK_ADMIN_PASSWORD=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/rundeck:latest --env-file .env.rundeck up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/rundeck:latest --env-file .env.rundeck ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| rundeck | jordan/rundeck:5.20.1 | Rundeck server with embedded MySQL |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Rundeck | `rundeck.example.com` |
| `RUNDECK_ADMIN_PASSWORD` | Admin user password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `rundeck` |
| `RUNDECK_VERSION` | Rundeck image version | `5.20.1` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `rundeck_config` | Rundeck configuration files |
| `rundeck_var` | Rundeck variable data |
| `rundeck_plugins` | Custom plugins |
| `rundeck_logs` | Log files |
| `rundeck_ssh` | SSH keys for remote execution |
| `rundeck_mysql` | Embedded MySQL database |
| `rundeck_app_logs` | Application logs |
| `rundeck_storage` | Key storage and resources |

## Post-Deployment

### Initial Login

1. Navigate to `https://rundeck.example.com`
2. Login with:
   - Username: `admin`
   - Password: Your `RUNDECK_ADMIN_PASSWORD` value

### Create Your First Project

1. Click "New Project"
2. Enter a project name and description
3. Configure node sources (local or SSH)
4. Start creating jobs

### SSH Key Setup

To run commands on remote nodes, add SSH keys:

```bash
# Copy your SSH key into the container
docker cp ~/.ssh/id_rsa rundeck:/var/lib/rundeck/.ssh/id_rsa

# Fix permissions
docker exec rundeck chown rundeck:rundeck /var/lib/rundeck/.ssh/id_rsa
docker exec rundeck chmod 600 /var/lib/rundeck/.ssh/id_rsa
```

### Configure SMTP

Add the following to `rundeck-config.properties` (inside `rundeck_config` volume):

```properties
grails.mail.host=smtp.example.com
grails.mail.port=25
grails.mail.username=noreply@example.com
grails.mail.password=Swordfish
```

### Adding Nodes

Add nodes via XML (`resources.xml`):

```xml
<node name="foo.example.com" 
    description="foo" tags="production" 
    osFamily="unix" osName="Linux"
    hostname="foo.example.com" username="bee" 
    />
```

Or via YAML (`resources.yaml`):

```yaml
foo.example.com:
  nodename: foo.example.com
  hostname: foo.example.com
  osFamily: unix
  osArch: amd64
  osName: Linux
  username: bee
  tags: 'production'
```

## Common Operations

### Using bc CLI

```bash
bc rundeck logs -f     # View logs
bc rundeck restart     # Restart
bc rundeck down        # Stop
bc rundeck update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/rundeck:latest --env-file .env.rundeck"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

### Export Jobs

```bash
docker exec rundeck rd jobs list -p MyProject --format yaml > jobs-backup.yaml
```

### Import Jobs

```bash
docker cp jobs.yaml rundeck:/tmp/jobs.yaml
docker exec rundeck rd jobs load -p MyProject -f /tmp/jobs.yaml
```

## Troubleshooting

### Slow Startup

Rundeck has a long startup time (up to 2 minutes). The healthcheck is configured with `start_period: 120s` to accommodate this.

### Version Not Updating After Upgrade

If upgrading the version doesn't take effect after restart, remove and recreate the container:

```bash
dc down
dc up -d
```

### Cannot Connect to Remote Nodes

1. Verify SSH keys are properly configured
2. Check that target hosts are in the project's node sources
3. Test SSH manually from the container:

```bash
docker exec -it rundeck ssh user@target-host
```

### Container not healthy

Check logs with `dc logs rundeck` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.rundeck.com/)
- [Docker Hub](https://hub.docker.com/r/jordan/rundeck)
- [GitHub](https://github.com/rundeck/rundeck)
