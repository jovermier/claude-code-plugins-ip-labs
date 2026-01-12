---
name: coder-environment
description: Coder workspace environment context and available tools
---

# Coder Environment Skill

Provides context about the Coder development workspace environment, available tools, and platform-specific considerations.

## Environment Overview

You are running in a **Coder development workspace** with the following characteristics:

| Property | Value |
|----------|-------|
| **OS** | Linux (Ubuntu/Debian-based) |
| **Architecture** | x86_64 (modern Intel/AMD processors, NOT ARM/Apple Silicon) |
| **Container Runtime** | Docker-in-Docker capability via envbox |
| **Infrastructure** | Kubernetes-managed workspace with persistent storage |
| **Networking** | Internal cluster networking with port forwarding capabilities |
| **System Package Manager** | `apt`/`apt-get` |
| **Node.js Package Manager** | Check lockfile (pnpm/yarn/npm/bun) |

## Available Tools & Services

The following tools are pre-installed and available:

| Tool | Purpose |
|------|---------|
| **Docker & Docker Compose** | Full container management capability |
| **Kubernetes CLI (kubectl)** | Cluster access and management (requires VPN) |
| **GitHub CLI (gh)** | Repository management and operations |
| **VS Code Server** | IDE with extensions |
| **Coder CLI (coder)** | Coder-specific workspace operations |
| **PM2** | Process manager for keeping Node.js services running in the background |
| **Convex CLI** | Available when Convex feature is enabled |
| **Claude Code** | AI-powered CLI (custom installation via base image) |
| **ccusage** | Claude Code usage monitoring utility |

### Background Service Management

**PM2** is installed for managing development and production services:

```bash
# Check PM2 process status
pm2 status

# View logs from all PM2 processes
pm2 logs

# View logs for a specific application
pm2 logs [app-name]

# View recent log entries
pm2 logs --lines 50 --nostream
```

**Docker** is available for containerized services:

```bash
# List running containers
docker ps

# View container logs
docker logs [container-name]

# View logs with tail
docker logs -f [container-name]
```

## Platform-Specific Considerations

### Package Installation

- **System packages**: Use `apt-get` for installation
  ```bash
  sudo apt-get update
  sudo apt-get install package-name
  ```

- **Node.js packages**: Use the detected package manager
  ```bash
  [package-manager] install
  [package-manager] add package-name
  ```

**Note**: The workspace may have a preferred package manager configured. Check the environment or lockfile (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`) to determine which to use.

### Docker Usage

- Docker commands work normally (this is not Docker Desktop)
- No special port mapping or host configurations needed
- Docker-in-Docker means containers run inside the workspace environment

### File Paths

- Use **standard Linux paths** (not Windows or macOS formats)
- **Relative paths** for project files: `src/components/Header.tsx`
- **Absolute paths** for system files: `/usr/local/bin/tool`

### Hardware Optimizations

- Target **x86_64 architecture** for any hardware-specific optimizations
- Do NOT use ARM/Apple Silicon-specific flags or binaries
- Modern Intel/AMD processor features are available

### Network Services

- Services run on **standard Linux ports**
- No macOS/Windows port conflicts to consider
- Internal cluster networking with port forwarding for external access

#### Service URLs

Coder workspace services are accessed using the following URL pattern:

```
https://<service>--<workspace>--<owner>.<domain>
```

Common service names:
| Service | Port | URL Pattern |
|---------|------|-------------|
| Development server | 3000 | `https://app--<workspace>--<owner>.<domain>` |
| Production/preview | 3010 | `https://app-prod--<workspace>--<owner>.<domain>` |

Example URLs:
- **Dev**: `https://app--myproject--jdoe.example.com`
- **Prod**: `https://prod--myproject--jdoe.example.com`

**IMPORTANT**: Always use the full URL pattern for service access. Do NOT use `localhost:` URLs as they cause issues with remote services, authentication, cookies, and cross-origin requests.

### Environment Variables

**CRITICAL**: Before using or changing ANY environment variable, you MUST:

1. **Ask the user for permission** - "May I check the environment variables?" or "May I use/change the X environment variable?"
2. **Explain what you need** - Describe which variable(s) you need to access and why
3. **Wait for explicit approval** - Do not proceed without user consent

To check available environment variables:
```bash
env | grep -i <pattern>    # Search for specific variables
env                        # List all environment variables
printenv                   # Alternative way to list all
echo $VAR_NAME             # Check specific variable
```

**Never** modify environment variables without explicit user permission, as they may affect:
- API authentication and routing
- Service connections
- Model selection behavior
- Workspace functionality

### Workspace Scripts

The workspace supports these startup/shutdown scripts (configurable via parameters):

| Script | Default | Purpose |
|--------|---------|---------|
| **Startup** | `start.sh` | Runs in workspace directory when workspace starts |
| **Shutdown** | `stop.sh` | Runs in workspace directory when workspace stops |

Scripts are executed automatically by the Coder agent. Use them for:
- Starting development servers with PM2
- Running database migrations
- Setting up environment-specific configurations
- Graceful shutdown of services

### Optional Features

These features can be enabled when creating a workspace:

| Feature | Description |
|---------|-------------|
| **PostgreSQL (CNPG)** | CloudNativePG database cluster with clone support |
| **S3 Storage (Ceph)** | S3-compatible storage for file uploads |
| **Convex** | Backend-as-a-service with postgres and S3 pre-configured |
| **AI Marketplaces** | Claude Code marketplaces (ip-labs-marketplace) with review agents |

## Capabilities

You can help with:

- **Code Development**: Writing, reviewing, and debugging code
- **Concept Explanations**: Explaining complex programming concepts
- **Best Practices**: Suggesting optimizations and patterns
- **Architecture**: Helping with design decisions
- **Troubleshooting**: Debugging technical issues
- **Documentation**: Providing comments and docs
- **DevOps**: Infrastructure and deployment tasks
- **Containers**: Docker and Kubernetes operations

## Response Guidelines

- Provide clear, concise, and accurate responses
- Consider the context of the workspace and the user's current task
- Account for the Linux x86_64 environment in all recommendations
