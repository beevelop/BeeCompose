# SonarQube

> **OCI Artifact** - Deploy directly from GitHub Container Registry

Continuous code quality inspection platform for detecting bugs, vulnerabilities, and code smells across 30+ programming languages.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Prepare host system (required for Elasticsearch)
sudo sysctl -w vm.max_map_count=524288
sudo sysctl -w fs.file-max=131072

# 2. Create environment file
cat > .env.sonarqube << 'EOF'
COMPOSE_PROJECT_NAME=sonarqube
SERVICE_DOMAIN=sonarqube.example.com
EOF

# 3. Deploy
bc sonarqube up

# 4. Check status
bc sonarqube ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Prepare host system (required for Elasticsearch)
sudo sysctl -w vm.max_map_count=524288
sudo sysctl -w fs.file-max=131072

# 2. Create environment file
cat > .env.sonarqube << 'EOF'
COMPOSE_PROJECT_NAME=sonarqube
SERVICE_DOMAIN=sonarqube.example.com
EOF

# 3. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/sonarqube:latest --env-file .env.sonarqube up -d --pull always

# 4. Check status
docker compose -f oci://ghcr.io/beevelop/sonarqube:latest --env-file .env.sonarqube ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))
- Minimum 4GB RAM
- System configuration:
  ```bash
  # Add to /etc/sysctl.conf for persistence
  vm.max_map_count=524288
  fs.file-max=131072
  ```

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | sonarqube-db | Analysis data storage |

**Note:** Database uses hardcoded credentials (`sonar`/`sonar`) for simplicity.

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| sonarqube | sonarqube:26.6.0.123539-community | SonarQube analysis server |
| sonarqube-db | postgres:17-alpine | PostgreSQL database |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for SonarQube | `sonarqube.example.com` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `sonarqube` |
| `SONARQUBE_VERSION` | SonarQube image version | `26.6.0.123539-community` |
| `POSTGRES_TAG` | PostgreSQL image tag | `17-alpine` |

### Internal (Pre-configured)

| Variable | Value | Purpose |
|----------|-------|---------|
| `SONARQUBE_JDBC_URL` | `jdbc:postgresql://database:5432/sonar` | Database connection |
| `SONARQUBE_JDBC_USERNAME` | `sonar` | Database user |
| `SONARQUBE_JDBC_PASSWORD` | `sonar` | Database password |

## Volumes

| Volume | Purpose |
|--------|---------|
| `postgres_data` | PostgreSQL database files |
| `sonarqube_data` | Analysis data and embedded database |
| `sonarqube_extensions` | Plugins and custom rules |
| `sonarqube_logs` | Application logs |

## Post-Deployment

### Initial Login

1. Navigate to `https://sonarqube.example.com`
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin`
3. **Change the password immediately** when prompted

### Generate Project Token

1. Go to User > My Account > Security
2. Generate a new token for scanner authentication
3. Save the token securely

### Analyze Your First Project

Using SonarScanner CLI:

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarqube.example.com \
  -Dsonar.token=your-token-here
```

Using Maven:

```bash
mvn sonar:sonar \
  -Dsonar.host.url=https://sonarqube.example.com \
  -Dsonar.token=your-token-here
```

### Install Plugins

1. Go to Administration > Marketplace
2. Search for plugins (e.g., "Python", "TypeScript")
3. Install and restart SonarQube

## Common Operations

### Using bc CLI

```bash
bc sonarqube logs -f       # View logs
bc sonarqube logs -f sonarqube  # View specific service logs
bc sonarqube restart       # Restart
bc sonarqube down          # Stop
bc sonarqube update        # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/sonarqube:latest --env-file .env.sonarqube"

# View logs
dc logs -f

# View specific service logs
dc logs -f sonarqube
dc logs -f database

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d
```

### Backup Database

```bash
docker exec sonarqube-db pg_dump -U sonar sonar > sonarqube-backup.sql
```

### Restore Database

```bash
cat sonarqube-backup.sql | docker exec -i sonarqube-db psql -U sonar sonar
```

## Troubleshooting

### Elasticsearch Bootstrap Error

If SonarQube fails to start with Elasticsearch errors:

```bash
# Check current value
sysctl vm.max_map_count

# Set required value
sudo sysctl -w vm.max_map_count=524288

# Make persistent
echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf
```

### Out of Memory

SonarQube requires significant memory. Ensure the host has at least 4GB RAM available. Check memory usage:

```bash
docker stats sonarqube
```

### Slow Startup

SonarQube has a long startup time (up to 2 minutes). The healthcheck is configured with `start_period: 120s` to accommodate this.

### Database Connection Failed

Verify PostgreSQL is running and healthy:

```bash
docker exec sonarqube-db pg_isready -U sonar
```

### Container not healthy

Check logs with `dc logs sonarqube` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.sonarqube.org/)
- [Docker Hub](https://hub.docker.com/_/sonarqube)
- [GitHub](https://github.com/SonarSource/sonarqube)
- [Supported Languages](https://docs.sonarqube.org/latest/analysis/languages/overview/)
