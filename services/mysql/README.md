# MySQL

> **OCI Artifact** - Deploy directly from GitHub Container Registry

MySQL is a widely-used open-source relational database management system. This stack provides a production-ready MySQL 8.0 instance with UTF-8 support and health checks.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.mysql << 'EOF'
COMPOSE_PROJECT_NAME=mysql
MYSQL_VERSION=8.4
MYSQL_ROOT_PASSWORD=Swordfish
EOF

# 2. Deploy
bc mysql up

# 3. Check status
bc mysql ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.mysql << 'EOF'
COMPOSE_PROJECT_NAME=mysql
MYSQL_VERSION=8.4
MYSQL_ROOT_PASSWORD=Swordfish
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/mysql:latest --env-file .env.mysql up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/mysql:latest --env-file .env.mysql ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| mysql | mysql:8.4 | MySQL database server |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | Root user password | `Swordfish` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `mysql` |
| `MYSQL_VERSION` | MySQL image version | `8.4` |

## Volumes

| Volume | Purpose |
|--------|---------|
| `mysql_data` | MySQL database files (`/var/lib/mysql`) |
| `mysql_config` | Custom MySQL configuration (`/etc/mysql/conf.d`) |

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 3306 | TCP | MySQL server |

## Post-Deployment

### Connect to MySQL

```bash
# Using mysql client
mysql -h localhost -P 3306 -u root -p

# Or via docker exec
docker exec -it mysql mysql -u root -p
```

### Create a Database and User

```sql
CREATE DATABASE myapp;
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON myapp.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
```

### Custom Configuration

Place custom `.cnf` files in the `mysql_config` volume to customize MySQL settings.

## Common Operations

### Using bc CLI

```bash
bc mysql logs -f     # View logs
bc mysql restart     # Restart
bc mysql down        # Stop
bc mysql update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/mysql:latest --env-file .env.mysql"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d

# Backup database
docker exec mysql mysqldump -u root -p --all-databases > backup.sql

# Restore database
docker exec -i mysql mysql -u root -p < backup.sql
```

## Troubleshooting

### Connection refused
Ensure the container is running and healthy. MySQL may take up to 30 seconds to initialize on first start.

### Authentication errors
Verify `MYSQL_ROOT_PASSWORD` matches what was set during initial deployment. The password is only set on first container creation.

### Container not healthy
Check logs with `dc logs mysql` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://dev.mysql.com/doc/)
- [Docker Hub](https://hub.docker.com/_/mysql)
- [GitHub](https://github.com/mysql/mysql-server)
