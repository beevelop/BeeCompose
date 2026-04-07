# Sentry

Self-hosted [Sentry](https://sentry. error and performance monitoring platform.io) 

## Architecture

Sentry 26.x is a multi-service stack. All images are pulled from GitHub Container Registry (`ghcr.io`).

| Layer | Services |
|---|---|
| **Ingress** | Relay (Traefik-fronted) |
| **Application** | web, events/attachments consumers, task workers, sentry-cleanup |
| **Snuba** | snuba-api + 6 Kafka consumers + replacer + subscription consumer |
| **Symbolicator** | symbolicator + symbolicator-cleanup |
| **Message Queue** | Kafka (KRaft mode, no ZooKeeper) |
| **Databases** | PostgreSQL 14 + pgbouncer, ClickHouse (Altinity) |
| **Cache** | Redis, Memcached |
| **Mail** | SMTP (exim4) |
| **Task Queue** | taskbroker + taskscheduler + taskworker |
| **Profiling** (feature-complete only) | vroom + seaweedfs + vroom-cleanup |
| **Uptime** (feature-complete only) | uptime-checker |

### Profiles

| Profile | Containers | RAM |
|---|---|---|
| `errors-only` (default) | ~26 | ~8 GB |
| `feature-complete` | ~70 | ~16 GB |

## Prerequisites

- Docker 25.0+, Docker Compose v2.24+
- Traefik running with `traefik_default` network

## Deployment

### 1. Clone or download the service directory

All config files (clickhouse/, relay/, symbolicator/, sentry/, redis.conf) must be present in the working directory alongside `docker-compose.yml`.

### 2. Configure environment

```bash
cp .env.example .env.local
# Edit .env.local with your domain and settings
```

### 3. Generate relay credentials

```bash
docker compose run --rm relay credentials generate
```

Copy the `secret_key` and `public_key` output into `relay/config.yml`:

```bash
cp relay/config.yml.example relay/config.yml
# Edit relay/config.yml and set secret_key + public_key
```

### 4. Generate the Sentry secret key

```bash
docker compose run --rm web config generate-secret-key
```

Copy the output into `sentry.env` as `SENTRY_SYSTEM_SECRET_KEY`.

### 5. Run database migrations

On first deploy only:

```bash
docker compose run --rm web upgrade --noinput
```

### 6. Create an admin user

```bash
docker compose run --rm web createuser --email admin@example.com --password Swordfish --superuser
```

### 7. Start the stack

```bash
# Errors-only (default, ~26 containers)
docker compose --env-file .env.local up -d

# Feature-complete (~70 containers)
COMPOSE_PROFILES=feature-complete docker compose --env-file .env.local up -d
```

### With bc CLI

```bash
bc sentry up
```

### Direct OCI deployment

```bash
# NOTE: Config directories (sentry/, clickhouse/, relay/, symbolicator/) and
# redis.conf must exist in the working directory before running.
docker compose -f oci://ghcr.io/beevelop/sentry:latest --env-file .env.local up -d
```

## Directory Structure

```
services/sentry/
 docker-compose.yml
 .env                      # Image version pins (committed)
 .env.example              # Configuration template
 sentry.env                # Sentry runtime env vars (set SENTRY_SYSTEM_SECRET_KEY!)
 sentry/                   # Mounted to /etc/sentry in sentry containers
 sentry.conf.py        # Django settings   
 config.yml            # Sentry YAML options (mail, filestore, integrations)   
 entrypoint.sh         # Container entrypoint   
 clickhouse/               # ClickHouse tuning (mounted read-only)
 config.xml   
 default-password.xml   
 symbolicator/             # Symbolicator config (mounted read-only)
 config.yml   
 relay/                    # Relay config (mounted read-only)
 config.yml            #  created from config.yml.exampleGenerated    
 config.yml.example    # Template   
 redis.conf                # Redis memory policy
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SERVICE_DOMAIN` | `sentry.example.com` | Public hostname (Traefik routing) |
| `COMPOSE_PROFILES` | `errors-only` | `errors-only` or `feature-complete` |
| `SENTRY_EVENT_RETENTION_DAYS` | `90` | Days to retain event data |
| `SENTRY_MAIL_ | FQDN for outbound mail (e.g. `sentry.example.com`) |HOST` | 
| `SENTRY_TASKWORKER_CONCURRENCY` | `4` | Parallel task worker processes |
| `SENTRY_SYSTEM_SECRET_ | **Required.** Django secret key (set in sentry.env) |KEY` | 

## Upgrading from 25.x

1. Stop the stack
2. Back up Postgres: `docker compose exec postgres pg_dumpall -U postgres > backup.sql`
3. Update images in `.env`
4. Run migrations: `docker compose run --rm web upgrade --noinput`
5. Restart

## Upgrading from 24.x

The internal architecture changed significantly in 25.x+:
 `SENTRY_SYSTEM_SECRET_KEY`
 many specialized Kafka consumers
- PostgreSQL trust auth replaces password auth (pgbouncer handles connections)
- Redis, ClickHouse, Kafka, Snuba, Relay, Symbolicator are now required
