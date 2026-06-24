# OCI Artifact Naming Convention

**Status:** Active  
**Version:** 1.0.0  
**Updated:** 2026-01-21

This document defines the naming and versioning standards for BeeCompose OCI artifacts published to GitHub Container Registry (GHCR).

## Registry URL

All BeeCompose OCI artifacts are published to:

```
ghcr.io/beevelop/<service>:<version>
```

## Naming Pattern

### Service Names

Service names in GHCR match the directory names in `services/`:

| Directory | OCI Artifact |
|-----------|--------------|
| `services/gitlab/` | `ghcr.io/beevelop/gitlab` |
| `services/traefik/` | `ghcr.io/beevelop/traefik` |
| `services/bitwarden/` | `ghcr.io/beevelop/bitwarden` |

### Version Tags

Versions are extracted from the service's `.env` file, specifically from the first `*_VERSION` variable found.

**Examples:**

| Service | `.env` Variable | OCI Tag |
|---------|-----------------|---------|
| GitLab | `GITLAB_VERSION=18.8.0` | `ghcr.io/beevelop/gitlab:v18.8.0` |
| Traefik | `TRAEFIK_VERSION=v3.7` | `ghcr.io/beevelop/traefik:v3.7` |
| Metabase | `METABASE_VERSION=v0.58.2` | `ghcr.io/beevelop/metabase:v0.58.2` |

## Versioning Rules

### 1. Version Prefix Normalization

If the version starts with a number, add a `v` prefix:

```bash
# Input: 18.8.0
# Output: v18.8.0

# Input: v3.6
# Output: v3.6 (unchanged)
```

### 2. Latest Tag

Every push to the `main` branch publishes a `latest` tag:

```
ghcr.io/beevelop/gitlab:latest
ghcr.io/beevelop/gitlab:v18.8.0
```

### 3. Development Tags

Pushes to the `develop` branch use the format:

```
ghcr.io/beevelop/gitlab:develop-<short-sha>
```

Example: `ghcr.io/beevelop/gitlab:develop-abc1234`

### 4. Special Cases

| Case | Tag Format | Example |
|------|------------|---------|
| Date-based versions | Use as-is with `v` prefix | `v2025-01-20` |
| Release candidates | Include full suffix | `v18.8.0-rc1` |
| Alpine/variant tags | Preserve suffix | `v3.88.0-alpine` |

## Volume Naming Convention

Named volumes use the pattern:

```
${COMPOSE_PROJECT_NAME:-<service>}_<purpose>
```

### Standard Volume Purposes

| Purpose | Description | Example |
|---------|-------------|---------|
| `_data` | Primary application data | `gitlab_data` |
| `_postgres_data` | PostgreSQL database | `gitlab_postgres_data` |
| `_redis_data` | Redis cache/data | `gitlab_redis_data` |
| `_mysql_data` | MySQL database | `directus_mysql_data` |
| `_config` | Configuration files | `traefik_config` |
| `_logs` | Log files | `traefik_logs` |
| `_acme` | Let's Encrypt certificates | `traefik_acme` |

### Examples

```yaml
volumes:
  postgres_data:
    name: ${COMPOSE_PROJECT_NAME:-gitlab}_postgres_data
  app_data:
    name: ${COMPOSE_PROJECT_NAME:-gitlab}_app_data
  redis_data:
    name: ${COMPOSE_PROJECT_NAME:-gitlab}_redis_data
```

## Usage Examples

### Deploy from GHCR

```bash
# Using specific version
docker compose \
  -f oci://ghcr.io/beevelop/gitlab:v18.8.0 \
  --env-file .env.production \
  up -d

# Using latest
docker compose \
  -f oci://ghcr.io/beevelop/gitlab:latest \
  --env-file .env.production \
  up -d
```

### List Available Versions

```bash
# Using GitHub CLI
gh api user/packages/container/gitlab/versions \
  --jq '.[].metadata.container.tags[]'

# Using Docker
docker manifest inspect ghcr.io/beevelop/gitlab:latest
```

### Pull OCI Artifact

```bash
# Pull compose manifest
docker compose \
  -f oci://ghcr.io/beevelop/gitlab:v18.8.0 \
  config
```

## Complete Service Registry

| Service | OCI URL |
|---------|---------|
| bitwarden | `ghcr.io/beevelop/bitwarden` |
| cabot | `ghcr.io/beevelop/cabot` |
| confluence | `ghcr.io/beevelop/confluence` |
| crowd | `ghcr.io/beevelop/crowd` |
| dependency-track | `ghcr.io/beevelop/dependency-track` |
| directus | `ghcr.io/beevelop/directus` |
| duckling | `ghcr.io/beevelop/duckling` |
| gitlab | `ghcr.io/beevelop/gitlab` |
| graylog | `ghcr.io/beevelop/graylog` |
| huginn | `ghcr.io/beevelop/huginn` |
| jira | `ghcr.io/beevelop/jira` |
| keycloak | `ghcr.io/beevelop/keycloak` |
| metabase | `ghcr.io/beevelop/metabase` |
| minio | `ghcr.io/beevelop/minio` |
| monica | `ghcr.io/beevelop/monica` |
| mysql | `ghcr.io/beevelop/mysql` |
| nexus | `ghcr.io/beevelop/nexus` |
| openvpn | `ghcr.io/beevelop/openvpn` |
| phpmyadmin | `ghcr.io/beevelop/phpmyadmin` |
| redash | `ghcr.io/beevelop/redash` |
| registry | `ghcr.io/beevelop/registry` |
| rundeck | `ghcr.io/beevelop/rundeck` |
| sentry | `ghcr.io/beevelop/sentry` |
| shields | `ghcr.io/beevelop/shields` |
| sonarqube | `ghcr.io/beevelop/sonarqube` |
| statping | `ghcr.io/beevelop/statping` |
| traefik | `ghcr.io/beevelop/traefik` |
| tus | `ghcr.io/beevelop/tus` |
| weblate | `ghcr.io/beevelop/weblate` |
| zabbix | `ghcr.io/beevelop/zabbix` |
