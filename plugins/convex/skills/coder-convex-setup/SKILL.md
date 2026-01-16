# Coder-Convex-Setup: Initial Convex Workspace Setup in Coder

You are an expert at **initial setup and configuration** of self-hosted Convex in Coder workspaces. This skill is ONLY for the one-time setup of a new Convex workspace. For everyday Convex development, use the `coder-convex` skill instead.

## When to Use This Skill

Use this skill when:
- Setting up Convex in a new Coder workspace for the first time
- Configuring a self-hosted Convex deployment
- Setting up Docker-based Convex backend
- Configuring environment variables for Convex
- Generating admin keys and deployment URLs

**DO NOT use this skill for:**
- Everyday Convex development (use `coder-convex` instead)
- Writing queries, mutations, or actions (use `coder-convex` instead)
- Schema modifications (use `coder-convex` instead)
- React integration issues (use `coder-convex` instead)

## Prerequisites

Before setting up Convex in a Coder workspace, ensure:

1. **Node.js and a package manager are installed**:
   ```bash
   node --version  # Should be v18+
   # Check for package manager: pnpm, yarn, npm, or bun
   pnpm --version  # Or: yarn --version, npm --version, bun --version
   ```

2. **Docker is available**:
   ```bash
   docker --version
   docker compose version
   ```

3. **PM2 is installed** (for frontend process management):
   ```bash
   pm2 --version
   ```

4. **Project has package.json with Convex dependency**:
   ```json
   {
     "dependencies": {
       "convex": "^1.31.3"
     }
   }
   ```

## Step 1: Install Convex Dependencies

```bash
# Install Convex package
[package-manager] add convex

# Install dev dependencies if not present
[package-manager] add -D @types/node typescript
```

## Step 2: Create Convex Directory Structure

Create the following directory structure:

```bash
mkdir -p convex/lib
```

The structure should look like:

```
convex/
├── lib/                  # Internal utilities (optional)
└── schema.ts            # Database schema (required)
```

## Step 3: Create Initial Schema

Create [convex/schema.ts](convex/schema.ts):

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Start with an empty schema or add initial tables
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
});
```

**Key Schema Rules**:
- Never manually add `_id` or `_creationTime` - they're automatic
- Index names should be descriptive: `by_fieldName`
- All indexes automatically include `_creationTime` as the last field
- Don't use `.index("by_creation_time", ["_creationTime"])` - it's built-in

## Step 4: Create Docker Compose Configuration

Create [docker-compose.yml](docker-compose.yml) for self-hosted Convex:

```yaml
services:
  backend:
    image: convex-dev/convex:latest
    ports:
      - "3210:3210"    # Convex API
      - "3211:3211"    # Convex S3 Proxy
      - "3212:3212"    # Convex Auth Proxy
      - "6791:6791"    # Convex Dashboard
    environment:
      - CONVEX_LOG_LEVEL=debug
    volumes:
      - convex_data:/convex/data
    restart: unless-stopped

volumes:
  convex_data:
```

**Note**: The exact image and configuration may vary based on your self-hosted Convex setup.

**Port Reference**:
- `3210` - Convex Backend API
- `3211` - Convex S3 Proxy (for file storage)
- `3212` - Convex Auth Proxy (for authentication)
- `6791` - Convex Dashboard (web UI)

## Step 5: Create Environment Generation Script

Create [generate-env.js](generate-env.js) to generate environment variables:

```javascript
import fs from 'fs';
import crypto from 'crypto';

// Generate or load deployment URL
const CONVEX_DEPLOYMENT = process.env.CONVEX_DEPLOYMENT || 'http://localhost:3210';

// Generate admin key if not provided
const CONVEX_ADMIN_KEY = process.env.CONVEX_ADMIN_KEY ||
  `sk_admin_${crypto.randomBytes(32).toString('hex')}`;

// LiteLLM configuration (self-hosted AI proxy)
const LITELLM_BASE_URL = process.env.LITELLM_BASE_URL || 'https://llm-gateway.hahomelabs.com';
const LITELLM_APP_API_KEY = process.env.LITELLM_APP_API_KEY || '';

// OpenAI for embeddings (optional, for RAG)
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';

// Feature flags
const ENABLE_RAG = process.env.ENABLE_RAG || 'false';

const envContent = `
# Convex Self-Hosted Deployment
CONVEX_DEPLOYMENT=${CONVEX_DEPLOYMENT}
CONVEX_ADMIN_KEY=${CONVEX_ADMIN_KEY}

# LiteLLM (Self-Hosted AI Proxy)
LITELLM_BASE_URL=${LITELLM_BASE_URL}
LITELLM_APP_API_KEY=${LITELLM_APP_API_KEY}

# OpenAI (for RAG embeddings - optional)
OPENAI_API_KEY=${OPENAI_API_KEY}

# Feature Flags
ENABLE_RAG=${ENABLE_RAG}
`.trim();

fs.writeFileSync('.env', envContent);
console.log('.env file generated successfully');
console.log(`CONVEX_DEPLOYMENT: ${CONVEX_DEPLOYMENT}`);
console.log(`CONVEX_ADMIN_KEY: ${CONVEX_ADMIN_KEY.slice(0, 20)}...`);
```

Make it executable and run:

```bash
chmod +x generate-env.js
node generate-env.js
```

## Step 6: Generate Admin Key from Docker

After starting Docker services, generate an admin key:

```bash
# Start Docker services
[package-manager] run [docker-up-script]

# Generate admin key from container
docker exec <container-name> /convex/generate_admin_key.sh
```

Add the generated key to your `.env` file:

```bash
# In .env
CONVEX_ADMIN_KEY=<generated-key>
```

## Step 7: Add NPM Scripts

Add these scripts to your [package.json](package.json):

```json
{
  "scripts": {
    "dev:backend": "npx convex dev",
    "deploy:functions": "npx convex deploy --yes",
    "docker:up": "docker compose --env-file .env.docker up -d",
    "docker:down": "docker compose --env-file .env.docker down",
    "docker:logs": "docker compose --env-file .env.docker logs -f",
    "docker:generate-admin-key": "docker exec <container-name> /convex/generate_admin_key.sh",
    "generate-env": "node generate-env.js"
  }
}
```

**Note**: Replace `<container-name>` with your actual Docker container name.

## Step 8: Initialize Convex Deployment

```bash
# Generate environment file
[package-manager] run [generate-env-script]

# Start Docker services
[package-manager] run [docker-up-script]

# Wait for services to be healthy, then initialize
[package-manager] run [dev-backend-script]
```

This will:
1. Connect to the self-hosted Convex deployment
2. Create the database schema
3. Generate type definitions in `convex/_generated/`

## Step 9: Deploy Functions

```bash
[package-manager] run [deploy-functions-script]
```

This deploys your Convex functions to the self-hosted backend.

## Step 10: Verify Setup

Create a test query to verify everything works:

```typescript
// convex/test.ts
import { query } from "./_generated/server";

export const healthCheck = query({
  args: {},
  handler: async () => {
    return {
      status: "ok",
      timestamp: Date.now(),
    };
  },
});
```

Deploy and test:

```bash
[package-manager] run [deploy-functions-script]
```

## Verification Checklist

After setup, verify:

- [ ] `convex/_generated/` directory exists with type definitions
- [ ] `convex/schema.ts` defines your tables
- [ ] `.env` file contains `CONVEX_DEPLOYMENT` and `CONVEX_ADMIN_KEY`
- [ ] Docker services are running: `docker ps`
- [ ] Can run `[package-manager] run [dev-backend-script]` without errors
- [ ] Can run `[package-manager] run [deploy-functions-script]` successfully
- [ ] Frontend can import from `convex/_generated/api`

## Troubleshooting Setup Issues

### Issue: `CONVEX_DEPLOYMENT not set`

**Solution**: Run `[package-manager] run [generate-env-script]` and verify `.env` exists.

### Issue: `Invalid admin key`

**Solution**:
1. Run `pnpm docker:generate-admin-key`
2. Copy the generated key
3. Update `.env` with the new key
4. Restart Docker services

### Issue: Docker container not starting

**Solution**:
```bash
# Check container logs
docker logs <container-name>

# Check if ports are already in use
lsof -i :3210    # Convex API
lsof -i :3211    # Convex S3 Proxy
lsof -i :3212    # Convex Auth Proxy
lsof -i :6791    # Convex Dashboard

# Recreate container
[package-manager] run [docker-down-script]
[package-manager] run [docker-up-script]
```

### Issue: Type definitions not generating

**Solution**:
```bash
# Clear Convex cache
rm -rf convex/_generated

# Re-run dev backend
[package-manager] run [dev-backend-script]

# Or explicitly deploy
[package-manager] run [deploy-functions-script]
```

### Issue: Cannot connect to Convex deployment

**Solution**:
```bash
# Verify Docker services are running
docker ps

# Check deployment URL is correct
echo $CONVEX_DEPLOYMENT

# Test connection
curl $CONVEX_DEPLOYMENT/health
```

## Self-Hosted vs Convex Cloud

| Aspect | Self-Hosted | Convex Cloud |
|--------|-------------|--------------|
| **Deployment URL** | Custom (e.g., `http://localhost:3210`) | `*.convex.cloud` |
| **Dashboard** | None (CLI only) | Web dashboard at convex.dev |
| **Admin Key** | Generated via Docker | Auto-provisioned |
| **Environment Variables** | `.env` file | Dashboard UI |
| **Authentication** | Custom setup | Built-in |
| **CLI Support** | Limited - CLI designed for Convex Cloud | Full support |
| **Cost** | Self-managed infrastructure | Usage-based pricing |

> **IMPORTANT**: The Convex CLI (`npx convex`) is designed primarily for Convex Cloud and has **limited support for self-hosted backends**. Some CLI commands may not work correctly with self-hosted deployments. Environment-based configuration and direct API interaction are often required instead.

## Environment Variables Reference

### Required for Self-Hosted Convex

```bash
# Convex Deployment
CONVEX_DEPLOYMENT=<deployment-url>    # e.g., http://localhost:3210
CONVEX_ADMIN_KEY=<admin-key>          # Generated from Docker

# AI Services (if using)
LITELLM_BASE_URL=<proxy-url>          # e.g., https://llm-gateway.hahomelabs.com
LITELLM_APP_API_KEY=<api-key>
OPENAI_API_KEY=<openai-key>           # For embeddings/RAG
```

### Optional Feature Flags

```bash
ENABLE_RAG=true/false                 # Enable RAG functionality
```

## Docker Commands Reference

```bash
# Start services
[package-manager] run [docker-up-script]                    # or: docker compose up -d

# Stop services
[package-manager] run [docker-down-script]                  # or: docker compose down

# View logs
[package-manager] run [docker-logs-script]                  # or: docker compose logs -f

# Restart services
docker compose restart

# Check container status
docker ps

# Execute command in container
docker exec <container-name> <command>

# Generate admin key
docker exec <container-name> /convex/generate_admin_key.sh
```

## Post-Setup: Next Steps

After completing the setup:

1. **Switch to `coder-convex` skill** for everyday development
2. **Define your schema** in `convex/schema.ts`
3. **Write queries and mutations** in `convex/*.ts` files
4. **Integrate with React** using `convex/react` hooks
5. **Deploy functions** with `[package-manager] run [deploy-functions-script]`

## Common Setup Patterns

### Pattern 1: Minimal Setup

For quick prototyping without authentication:

```typescript
// convex/schema.ts
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
});
```

### Pattern 2: With Authentication

Setup requires additional auth configuration (see `coder-convex` skill for details).

### Pattern 3: With AI/RAG

Requires:
- `OPENAI_API_KEY` in environment
- `ENABLE_RAG=true`
- Embeddings generation script

## Quick Setup Command Sequence

For a complete fresh setup:

```bash
# 1. Install dependencies
[package-manager] add convex
[package-manager] add -D @types/node typescript

# 2. Create directories
mkdir -p convex/lib

# 3. Create schema
cat > convex/schema.ts << 'EOF'
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
});
EOF

# 4. Generate environment
[package-manager] run [generate-env-script]

# 5. Start Docker
[package-manager] run [docker-up-script]

# 6. Initialize Convex
[package-manager] run [dev-backend-script]

# 7. Deploy functions
[package-manager] run [deploy-functions-script]
```

## Migration from Convex Cloud

If migrating from Convex Cloud to self-hosted:

1. **Export existing data** from Convex Cloud dashboard
2. **Update environment variables**:
   - Change `CONVEX_DEPLOYMENT` from `*.convex.cloud` to self-hosted URL
   - Generate new `CONVEX_ADMIN_KEY`
3. **Update schema** to match existing schema
4. **Import data** to self-hosted instance
5. **Update frontend imports** to use new deployment URL
6. **Deploy functions** to self-hosted backend

## Summary

This skill covers the **one-time setup** of self-hosted Convex in Coder workspaces:

1. Install dependencies
2. Create directory structure
3. Define initial schema
4. Configure Docker
5. Generate environment variables
6. Generate admin key
7. Initialize deployment
8. Verify setup

For **everyday Convex development** (queries, mutations, React integration, etc.), use the `coder-convex` skill instead.
