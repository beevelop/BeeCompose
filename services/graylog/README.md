# Graylog

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Graylog is a leading centralized log management solution for capturing, storing, and analyzing machine data in real-time. It provides powerful search, dashboards, and alerting capabilities.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Generate password secret and hash
GRAYLOG_PASSWORD_SECRET=$(openssl rand -base64 32)
GRAYLOG_ROOT_PASSWORD_SHA2=$(echo -n "Swordfish" | sha256sum | cut -d" " -f1)

# 2. Create environment file
cat > .env.graylog << EOF
COMPOSE_PROJECT_NAME=graylog
SERVICE_DOMAIN=graylog.example.com
GRAYLOG_PASSWORD_SECRET=${GRAYLOG_PASSWORD_SECRET}
GRAYLOG_ROOT_PASSWORD_SHA2=${GRAYLOG_ROOT_PASSWORD_SHA2}
EOF

# 3. Deploy
bc graylog up

# 4. Check status
bc graylog ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Generate password secret and hash
GRAYLOG_PASSWORD_SECRET=$(openssl rand -base64 32)
GRAYLOG_ROOT_PASSWORD_SHA2=$(echo -n "Swordfish" | sha256sum | cut -d" " -f1)

# 2. Create environment file
cat > .env.graylog << EOF
COMPOSE_PROJECT_NAME=graylog
SERVICE_DOMAIN=graylog.example.com
GRAYLOG_PASSWORD_SECRET=${GRAYLOG_PASSWORD_SECRET}
GRAYLOG_ROOT_PASSWORD_SHA2=${GRAYLOG_ROOT_PASSWORD_SHA2}
EOF

# 3. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/graylog:latest --env-file .env.graylog up -d --pull always

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/graylog:latest --env-file .env.graylog ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))
- Minimum 4GB RAM recommended (Elasticsearch requires significant memory)

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| MongoDB | graylog-mongodb | Configuration and metadata storage |
| Elasticsearch | graylog-elasticsearch | Search and indexing engine |

**Note:** Elasticsearch requires `vm.max_map_count=262144`. See Troubleshooting section.

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| graylog | graylog/graylog:6.3 | Log management web interface and API |
| graylog-elasticsearch | docker.elastic.co/elasticsearch/elasticsearch:7.17.29 | Search and indexing engine |
| graylog-mongodb | mongo:8.0 | Configuration and metadata storage |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Traefik routing | `graylog.example.com` |
| `GRAYLOG_PASSWORD_SECRET` | Secret for password encryption (min 16 chars) | Generate with `openssl rand -base64 32` |
| `GRAYLOG_ROOT_PASSWORD_SHA2` | SHA256 hash of admin password | Generate with `echo -n "password" \| sha256sum` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `graylog` |
| `GRAYLOG_TRANSPORT_EMAIL_ENABLED` | Enable email alerts | `false` |
| `GRAYLOG_TRANSPORT_EMAIL_HOSTNAME` | SMTP server hostname | - |
| `GRAYLOG_TRANSPORT_EMAIL_AUTH_USERNAME` | SMTP username | - |
| `GRAYLOG_TRANSPORT_EMAIL_AUTH_PASSWORD` | SMTP password | - |

## Volumes

| Volume | Purpose |
|--------|---------|
| `mongo_data` | MongoDB configuration database |
| `es_data` | Elasticsearch indices and data |
| `graylog_journal` | Graylog message journal |

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 514 | TCP/UDP | Syslog input |
| 5555 | TCP/UDP | Raw/plaintext input |
| 12201 | TCP/UDP | GELF (Graylog Extended Log Format) input |

## Post-Deployment

1. **Access the UI**: Navigate to `https://graylog.example.com`
2. **Login**: Username is `admin`, password is the plaintext you hashed for `GRAYLOG_ROOT_PASSWORD_SHA2`
3. **Create Inputs**: Go to System → Inputs to configure log sources:
   - **Syslog UDP/TCP** on port 514 for syslog messages
   - **GELF UDP/TCP** on port 12201 for structured logs
   - **Raw/Plaintext UDP/TCP** on port 5555 for plain text
4. **Configure Docker logging**: Send container logs to Graylog:
   ```json
   {
     "log-driver": "gelf",
     "log-opts": {
       "gelf-address": "udp://graylog.example.com:12201"
     }
   }
   ```
5. **Create Streams**: Organize logs by source or type
6. **Set up Alerts**: Configure conditions and notifications

## Common Operations

### Using bc CLI

```bash
bc graylog logs -f     # View logs
bc graylog restart     # Restart
bc graylog down        # Stop
bc graylog update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/graylog:latest --env-file .env.graylog"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

## Sending Logs to Graylog

### From Docker containers
```bash
docker run --log-driver=gelf --log-opt gelf-address=udp://graylog.example.com:12201 nginx
```

### From syslog
```bash
# Forward system logs
echo "*.* @graylog.example.com:514" >> /etc/rsyslog.conf
systemctl restart rsyslog
```

### From applications (GELF)
```bash
# Example using curl
echo '{"version":"1.1","host":"myapp","short_message":"Test message","level":6}' | \
  nc -u graylog.example.com 12201
```

## Troubleshooting

### Elasticsearch fails to start
Ensure sufficient memory and correct vm.max_map_count:
```bash
sudo sysctl -w vm.max_map_count=262144
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
```

### Cannot login to web interface
Verify your password hash is correct:
```bash
echo -n "your_password" | sha256sum | cut -d" " -f1
```

### Inputs not receiving logs
Check firewall rules allow traffic on ports 514, 5555, and 12201 (both TCP and UDP).

### Container not healthy
Check logs with `dc logs graylog` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.graylog.org/)
- [Docker Hub](https://hub.docker.com/r/graylog/graylog)
- [GitHub](https://github.com/Graylog2/graylog2-server)
