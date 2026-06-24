# GitLab

> **OCI Artifact** - Deploy directly from GitHub Container Registry

GitLab is a complete DevOps platform delivered as a single application. It provides Git repository management, CI/CD pipelines, issue tracking, code review, and much more.

## What is an OCI Artifact?

This is a **Docker Compose OCI artifact**, not a traditional Docker image. It contains a complete docker-compose.yml configuration that you can deploy directly using Docker 25.0+.

## Quick Start

### Using bc CLI (Recommended)

```bash
# 1. Create environment file
cat > .env.gitlab << 'EOF'
COMPOSE_PROJECT_NAME=gitlab
SERVICE_DOMAIN=gitlab.example.com
DB_PASS=Swordfish
GITLAB_ROOT_PASSWORD=Swordfish
GITLAB_SECRETS_DB_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_SECRET_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_OTP_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY=["1234567890abcdef1234567890abcdef"]
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY=["abcdef1234567890abcdef1234567890"]
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT=fedcba0987654321fedcba0987654321
EOF

# 2. Deploy
bc gitlab up

# 3. Check status
bc gitlab ps
```

> **Note:** Install the bc CLI with: `curl -fsSL https://raw.githubusercontent.com/beevelop/beecompose/main/scripts/install.sh | sudo bash`

### Manual Deployment

```bash
# 1. Create environment file
cat > .env.gitlab << 'EOF'
COMPOSE_PROJECT_NAME=gitlab
SERVICE_DOMAIN=gitlab.example.com
DB_PASS=Swordfish
GITLAB_ROOT_PASSWORD=Swordfish
GITLAB_SECRETS_DB_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_SECRET_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_OTP_KEY_BASE=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY=["1234567890abcdef1234567890abcdef"]
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY=["abcdef1234567890abcdef1234567890"]
GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT=fedcba0987654321fedcba0987654321
EOF

# 2. Deploy from GHCR
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab up -d --pull always

# 3. Check status
docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab ps
```

## Prerequisites

- Docker 25.0+ (required for OCI artifact support)
- Docker Compose v2.24+
- Traefik reverse proxy (see [traefik](../traefik/))
- Minimum 4GB RAM recommended

## Dependencies

This service includes all required backing stores:

| Dependency | Container | Purpose |
|------------|-----------|---------|
| PostgreSQL | gitlab-postgres | Primary database (kkimurak/sameersbn-postgresql) |
| Redis | gitlab-redis | Cache and session store |

See [Service Dependency Graph](../../docs/DEPENDENCIES.md) for details.

## Architecture

| Container | Image | Purpose |
|-----------|-------|---------|
| gitlab | sameersbn/gitlab:19.1.0 | GitLab application server |
| gitlab-postgres | kkimurak/sameersbn-postgresql:17 | PostgreSQL database |
| gitlab-redis | redis:7-alpine | Redis cache and session store |

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICE_DOMAIN` | Domain for Traefik routing | `gitlab.example.com` |
| `DB_PASS` | PostgreSQL database password | `Swordfish` |
| `GITLAB_ROOT_PASSWORD` | Initial root user password | `Swordfish` |
| `GITLAB_SECRETS_DB_KEY_BASE` | 64-char hex key for database encryption | Generate with `openssl rand -hex 64` |
| `GITLAB_SECRETS_SECRET_KEY_BASE` | 64-char hex key for session secrets | Generate with `openssl rand -hex 64` |
| `GITLAB_SECRETS_OTP_KEY_BASE` | 64-char hex key for OTP encryption | Generate with `openssl rand -hex 64` |
| `GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY` | JSON array of key(s) for ActiveRecord encryption (GitLab 19+) | `["<32-char-key>"]` (generate with `openssl rand -hex 16`) |
| `GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY` | JSON array of key(s) for deterministic encryption (GitLab 19+) | `["<32-char-key>"]` (generate with `openssl rand -hex 16`) |
| `GITLAB_SECRETS_ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT` | Salt string for key derivation (GitLab 19+) | `<32-char-salt>` (generate with `openssl rand -hex 16`) |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `gitlab` |
| `TZ` | System timezone | `Europe/Berlin` |
| `GITLAB_TIMEZONE` | GitLab application timezone | `Berlin` |
| `DB_NAME` | PostgreSQL database name | `gitlabhq_production` |
| `DB_USER` | PostgreSQL database user | `gitlab` |
| `GIT_PORT` | Host SSH port for Git operations | `2222` |
| `GITLAB_SSH_HOST` | SSH hostname shown in clone URLs | `${SERVICE_DOMAIN}` |
| `GITLAB_EMAIL` | Sender email for notifications | `noreply@example.com` |
| `GITLAB_EMAIL_DISPLAY_NAME` | Email display name | `BeeCompose GitLab` |
| `GITLAB_BACKUPS` | Backup schedule | `daily` |
| `GITLAB_BACKUP_TIME` | Backup time (HH:MM) | `04:00` |
| `GITLAB_BACKUP_EXPIRY` | Backup retention (seconds) | `172800` |
| `GITLAB_BACKUP_SKIP` | Skip backup components | `builds,artifacts` |
| `GITLAB_NOTIFY_ON_BROKEN_BUILDS` | Email on broken builds | `true` |
| `GITLAB_PROJECTS_SNIPPETS` | Enable project snippets | `true` |
| `NGINX_MAX_UPLOAD_SIZE` | Max upload size | `100m` |
| `GITLAB_UNICORN_MEMORY_MAX` | Unicorn max memory (bytes) | `629145600` |

### SMTP Configuration (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_ENABLED` | Enable SMTP | `false` |
| `SMTP_HOST` | SMTP server hostname | - |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP username | - |
| `SMTP_PASS` | SMTP password | - |
| `SMTP_DOMAIN` | SMTP domain | - |
| `SMTP_TLS` | Enable TLS | `true` |
| `SMTP_AUTHENTICATION` | Auth method | `login` |

### IMAP Configuration (Optional - Reply by Email)

| Variable | Description | Default |
|----------|-------------|---------|
| `IMAP_ENABLED` | Enable IMAP | `false` |
| `IMAP_HOST` | IMAP server hostname | - |
| `IMAP_PORT` | IMAP server port | - |
| `IMAP_USER` | IMAP username | - |
| `IMAP_PASS` | IMAP password | - |
| `IMAP_SSL` | Enable SSL | - |

## Volumes

| Volume | Purpose |
|--------|---------|
| `postgres_data` | PostgreSQL database files |
| `gitlab_data` | Git repositories, uploads, and artifacts |
| `redis_data` | Redis persistence |

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 2222 | TCP | SSH for Git operations (configurable via `GIT_PORT`) |

## Post-Deployment

1. **Wait for startup**: GitLab takes 3-5 minutes to fully initialize
2. **Access the UI**: Navigate to `https://gitlab.example.com`
3. **Login as root**: Use username `root` and the `GITLAB_ROOT_PASSWORD`
4. **Configure SSH**: Add your SSH key in User Settings → SSH Keys
5. **Clone via SSH**: Use port 2222 (or your configured `GIT_PORT`):
   ```bash
   git clone ssh://git@gitlab.example.com:2222/username/repo.git
   ```
6. **Configure SMTP**: Enable email notifications by setting SMTP variables
7. **Set up runners**: Install GitLab Runner for CI/CD pipelines

## Common Operations

### Using bc CLI

```bash
bc gitlab logs -f     # View logs
bc gitlab restart     # Restart
bc gitlab down        # Stop
bc gitlab update      # Pull and recreate
```

### Using docker compose directly

```bash
# Define alias for convenience
alias dc="docker compose -f oci://ghcr.io/beevelop/gitlab:latest --env-file .env.gitlab"

# View logs
dc logs -f

# Restart
dc restart

# Stop
dc down

# Update
dc pull && dc up -d

# Access Rails console
docker exec -it gitlab sudo -u git -H bundle exec rails console -e production

# Create backup manually
docker exec -it gitlab sudo -u git -H bundle exec rake gitlab:backup:create RAILS_ENV=production
```

## Troubleshooting

### GitLab takes too long to start
GitLab requires significant startup time (3-5 minutes). Check logs for progress:
```bash
dc logs -f gitlab
```

### SSH clone fails
Ensure the `GIT_PORT` is accessible and not blocked by firewall. Verify SSH is working:
```bash
ssh -T git@gitlab.example.com -p 2222
```

### Email notifications not working
Verify SMTP settings and check logs for email errors. Test with:
```bash
docker exec -it gitlab sudo -u git -H bundle exec rails console -e production
# Then run: Notify.test_email('your@email.com', 'Test', 'Test').deliver_now
```

### Container not healthy
Check logs with `dc logs gitlab` and ensure all required environment variables are set.

## Links

- [Official Documentation](https://docs.gitlab.com/)
- [Docker Hub](https://hub.docker.com/r/sameersbn/gitlab)
- [GitHub](https://github.com/sameersbn/docker-gitlab)
