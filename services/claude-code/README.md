# Claude Code

Remote [Claude Code](https://code.claude.com/) instance with remote control support. Run Claude Code 24/7 on your server and connect from the Claude mobile/web app.

## Prerequisites

1. Copy `.env.example` to `.env.production` and fill in your values.

2. **For git access (optional):** Generate an SSH deploy key, add it to your repo, and set `DEPLOY_KEY_B64` in your env file. See [Git Repository](#git-repository) below.

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

## First Launch -- Interactive Login

Remote control mode requires an OAuth login (API keys are **not** supported). On first launch, you must attach to the container and complete the login flow:

1. **Start the container** (see Quick Start above).

2. **Attach to the running container:**
   ```bash
   docker attach claude-code
   ```

3. **Complete the OAuth login** -- the entrypoint will automatically run `claude login`. Follow the URL printed in the terminal to authenticate in your browser.

4. **After login succeeds**, press `Ctrl+C` to continue. The entrypoint will then launch `claude remote-control`.

5. **Detach from the container** with `Ctrl+P` then `Ctrl+Q` (Docker's detach sequence). The container continues running in the background.

Subsequent container restarts will use the persisted credentials and skip the login step entirely.

## Credential Storage

Claude Code stores its credentials in these locations inside the container:

| Path | Purpose |
|------|---------|
| `/home/node/.claude/.credentials.json` | OAuth tokens (access + refresh) |
| `/home/node/.claude.json` | Account metadata and onboarding state |
| `/home/node/.claude/` | Full config directory (credentials, settings, history) |

To persist credentials across container restarts, a volume is mounted at `/home/node/.claude` (the `claude_config` volume in docker-compose.yml).

The image pre-seeds `/home/node/.claude.json` with onboarding state so Claude Code does not prompt for initial setup.

## Configuration

### Git Repository

To let Claude Code clone a repo and push changes, set up SSH deploy key authentication:

1. Generate a deploy key:
   ```bash
   ssh-keygen -t ed25519 -f deploy_key -N ""
   ```

2. Add `deploy_key.pub` as a **Deploy key** to your GitHub repo (Settings > Deploy keys > Add deploy key). Enable **Allow write access**.

3. Base64-encode the private key and add it to your `.env.claude-code`:
   ```bash
   # Encode (works on both macOS and Linux):
   base64 < deploy_key | tr -d '\n'
   ```
   ```bash
   DEPLOY_KEY_B64=LS0tLS1CRUdJTi...  # paste the base64 output here
   GIT_REPO=git@github.com:your-org/your-repo.git
   GIT_USER_NAME=Claude Code
   GIT_USER_EMAIL=claude@example.com
   ```

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_REPO` | *(empty)* | SSH clone URL (e.g., `git@github.com:your-org/your-repo.git`) |
| `GIT_BRANCH` | *(repo default)* | Branch to clone |
| `GIT_USER_NAME` | *(empty)* | Git commit author name |
| `GIT_USER_EMAIL` | *(empty)* | Git commit author email |
| `DEPLOY_KEY_B64` | *(empty)* | Base64-encoded SSH private key (ed25519) |

The deploy key is base64-encoded so it fits on a single line in the `.env` file. The entrypoint decodes it and writes it to `~/.ssh/id_ed25519` with restricted permissions at startup.

On first start, if `GIT_REPO` is set and `/workspace` is empty, the entrypoint clones the repository. On subsequent restarts the existing clone is reused.

Without a deploy key, the service still works for general Claude Code usage -- git features are simply unavailable.

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_MODEL` | *(Claude default)* | Override the default model |
| `CLAUDE_PERMISSION_MODE` | `acceptEdits` | Permission mode for `remote-control` (see below) |
| `INIT_COMMAND` | *(empty)* | One-time setup command (runs once on first launch, tracked via stamp file) |
| `CLAUDE_EXTRA_ARGS` | *(empty)* | Extra flags for `claude remote-control` |

### Permission Modes

Controls what Claude Code can do without asking for confirmation:

| Mode | Behavior |
|------|----------|
| `default` | Prompts for all file edits and commands |
| `acceptEdits` | Auto-approves file edits, prompts for shell commands **(default)** |
| `bypassPermissions` | Full autonomous / YOLO mode -- no prompts at all |
| `plan` | Read-only planning mode -- no edits or commands |

To run fully autonomous:
```bash
CLAUDE_PERMISSION_MODE=bypassPermissions
```

### Init Command

The `INIT_COMMAND` variable lets you install additional tools into the container on first boot. It runs once and is tracked via a stamp file in the Claude config volume, so it won't re-run on subsequent container restarts.

```bash
# Example: Install Python and build tools
INIT_COMMAND=apt-get update && apt-get install -y build-essential python3 python3-pip
```

## Volumes

| Volume | Container Path | Purpose |
|--------|---------------|---------|
| `claude_config` | `/home/node/.claude` | Claude credentials, config, and history (persists login across restarts) |
| `claude_workspace` | `/workspace` | Project files (auto-cloned from `GIT_REPO`) |

## Connecting

Once the container is running, open Claude on iOS/Android or the web app, navigate to **Remote Control**, and attach to the running session. All code edits and tool executions happen inside the container on your server.

## Docker Image

This service uses the [`beevelop/claude`](https://hub.docker.com/r/beevelop/claude) Docker image, which is based on `node:22-bookworm-slim` with Claude Code CLI pre-installed.

Source: [github.com/beevelop/docker-claude](https://github.com/beevelop/docker-claude)
