# Claude Code

Remote [Claude Code](https://code.claude.com/) instance with remote control support. Run Claude Code 24/7 on your server and connect from the Claude mobile/web app.

## Prerequisites

1. Copy `.env.example` to `.env.production` and fill in your values.

2. **For git access (optional):** Generate an SSH deploy key, add it to your repo, and set `DEPLOY_KEY_PATH` in your env file. See [Git Repository](#git-repository) below.

## Quick Start

### Using bc CLI

```bash
# Deploy
bc claude-code up

# View logs
bc claude-code logs -f

# Stop
bc claude-code down
```

### Using OCI Artifact

```bash
# Deploy directly from GHCR
docker compose -f oci://ghcr.io/beevelop/claude-code:latest --env-file .env up -d

# View logs
docker compose -f oci://ghcr.io/beevelop/claude-code:latest --env-file .env logs -f

# Stop
docker compose -f oci://ghcr.io/beevelop/claude-code:latest --env-file .env down
```

### Local Development

```bash
cd services/claude-code

# Deploy locally
docker compose --env-file .env.example up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

## Configuration

### Authentication

You need **one** of the following:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key (charges API account) |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth token for Claude Pro/Max subscription |

**API Key** is recommended for automation. Get one from [console.anthropic.com](https://console.anthropic.com/).

**OAuth Token** bills against your Claude subscription instead of API credits. Generate once on a trusted machine:

```bash
claude setup-token
```

### Git Repository

To let Claude Code clone a repo and push changes, set up SSH deploy key authentication:

1. Generate a deploy key:
   ```bash
   ssh-keygen -t ed25519 -f deploy_key -N ""
   ```

2. Add `deploy_key.pub` as a **Deploy key** to your GitHub repo (Settings > Deploy keys > Add deploy key). Enable **Allow write access**.

3. Configure in your `.env.production`:
   ```bash
   GIT_REPO=git@github.com:your-org/your-repo.git
   GIT_USER_NAME=Claude Code
   GIT_USER_EMAIL=claude@example.com
   DEPLOY_KEY_PATH=./deploy_key
   ```

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_REPO` | *(empty)* | SSH clone URL (e.g., `git@github.com:your-org/your-repo.git`) |
| `GIT_BRANCH` | *(repo default)* | Branch to clone |
| `GIT_USER_NAME` | *(empty)* | Git commit author name |
| `GIT_USER_EMAIL` | *(empty)* | Git commit author email |
| `DEPLOY_KEY_PATH` | `/dev/null` | Path to SSH private key file |

The deploy key is injected via Docker Compose [secrets](https://docs.docker.com/compose/how-tos/use-secrets/), which mounts it at `/run/secrets/deploy_key` with restricted permissions. The entrypoint copies it to the SSH config directory automatically.

On first start, if `GIT_REPO` is set and `/workspace` is empty, the entrypoint clones the repository. On subsequent restarts the existing clone is reused.

Without a deploy key, the service still works for general Claude Code usage — git features are simply unavailable.

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_MODEL` | *(Claude default)* | Override the default model |
| `INIT_COMMAND` | *(empty)* | One-time setup command (runs once, persisted via stamp file) |
| `CLAUDE_EXTRA_ARGS` | *(empty)* | Extra flags for `claude remote-control` |

### Init Command

The `INIT_COMMAND` variable lets you install additional tools into the container on first boot. It runs once and is tracked via a stamp file in the Claude home volume, so it won't re-run on subsequent container restarts.

```bash
# Example: Install Python and build tools
INIT_COMMAND=apt-get update && apt-get install -y build-essential python3 python3-pip
```

## Volumes

| Volume | Container Path | Purpose |
|--------|---------------|---------|
| `claude_home` | `/opt/claude` | Claude config, credentials, history |
| `claude_workspace` | `/workspace` | Project files (auto-cloned from `GIT_REPO`) |

## Connecting

Once the container is running, open Claude on iOS/Android or the web app, navigate to **Remote Control**, and attach to the running session. All code edits and tool executions happen inside the container on your server.

## Docker Image

This service uses the [`beevelop/claude`](https://hub.docker.com/r/beevelop/claude) Docker image, which is based on `node:22-bookworm-slim` with Claude Code CLI pre-installed.

Source: [github.com/beevelop/docker-claude](https://github.com/beevelop/docker-claude)
