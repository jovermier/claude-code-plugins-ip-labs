# Environment Variables Reference

Complete reference for all Convex self-hosted environment variables.

## Core Variables

### CONVEX_SELF_HOSTED_URL

**Purpose**: Backend API URL for self-hosted Convex.

**Required**: Yes

**Example**:
```bash
CONVEX_SELF_HOSTED_URL=http://127.0.0.1:3210
```

**Notes**:
- Use `http://127.0.0.1:3210` for local development
- Use `https://your-domain.com` for production
- Must be accessible from your application

### CONVEX_SELF_HOSTED_ADMIN_KEY

**Purpose**: Admin authentication key for deployment and dashboard access.

**Required**: Yes

**Example**:
```bash
CONVEX_SELF_HOSTED_ADMIN_KEY=prod_xYz...123
```

**Generation**:
```bash
docker compose exec backend ./generate_admin_key.sh
```

**Best Practices**:
- Never commit to version control
- Rotate regularly (quarterly recommended)
- Use different keys for dev/staging/production
- Store in secret management systems for production

## Platform-Specific Variables

### CONVEX_CLOUD_ORIGIN

**Purpose**: Backend API endpoint for PaaS deployments (Fly.io, Railway, etc.).

**Required**: For PaaS deployments

**Example**:
```bash
CONVEX_CLOUD_ORIGIN=https://your-app.fly.dev
```

**Accessible As**: `process.env.CONVEX_CLOUD_URL` in backend functions

### CONVEX_SITE_ORIGIN

**Purpose**: HTTP actions endpoint for PaaS deployments.

**Required**: For PaaS deployments

**Example**:
```bash
CONVEX_SITE_ORIGIN=https://your-site.fly.dev
```

**Accessible As**: `process.env.CONVEX_SITE_ORIGIN` in backend functions

## Database Configuration

### POSTGRES_URL

**Purpose**: PostgreSQL connection string (preferred over DATABASE_URL).

**Required**: For PostgreSQL deployments

**Example**:
```bash
POSTGRES_URL=postgres://user:pass@host:5432?sslmode=require
```

**Gotcha**: Remove database name from URL - Convex adds it based on `INSTANCE_NAME`.

### DATABASE_URL

**Purpose**: Alternative database connection string.

**Required**: For database deployments

**Example**:
```bash
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

**Gotcha**: Use `POSTGRES_URL` instead for better compatibility.

### INSTANCE_NAME

**Purpose**: Instance identifier used for database name prefix.

**Required**: When using PostgreSQL

**Example**:
```bash
INSTANCE_NAME=app
```

**Notes**:
- Must match PostgreSQL database name
- Default is `app` if not specified

## Authentication Variables

### JWT_PRIVATE_KEY

**Purpose**: RSA private key for signing JWT tokens (@convex-dev/auth).

**Required**: For authentication

**Format**: Must be **PKCS#8** format (starts with `-----BEGIN PRIVATE KEY-----`)

**Example**:
```bash
JWT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCHbqvhQBKUY4pw
...
-----END PRIVATE KEY-----"
```

**See**: [Authentication Guide](authentication.md) for detailed setup instructions.

### JWKS

**Purpose**: JSON Web Key Set for verifying JWT signatures.

**Required**: For authentication

**Format**: JSON string with JWK format

**Example**:
```bash
JWKS='{"keys":[{"kty":"RSA","e":"AQAB","n":"...","alg":"RS256","kid":"convex-auth-key","use":"sig"}]}'
```

### JWT_ISSUER

**Purpose**: Issuer URL for JWT tokens.

**Required**: For authentication

**Example**:
```bash
JWT_ISSUER=https://your-convex-url.com
```

**For Clerk**:
```bash
CLERK_JWT_ISSUER_DOMAIN=https://your-app.clerk.accounts.dev
```

### CONVEX_SITE_ORIGIN (Deployment)

**Purpose**: Convex Site URL for auth provider discovery and JWT validation. Used by `auth.config.ts`.

**Required**: For authentication with `@convex-dev/auth`

**Set via**: `npx convex env set CONVEX_SITE_ORIGIN "https://your-convex-site-url.com"`

**Example**:
```bash
# For Coder workspaces
CONVEX_SITE_ORIGIN=https://convex-site--workspace--user.coder.domain

# For local development
CONVEX_SITE_ORIGIN=http://localhost:3211
```

**Critical**: This must be set as a deployment environment variable (via `npx convex env set`) because `auth.config.ts` reads it via `process.env.CONVEX_SITE_ORIGIN`.

## Security Variables

### INSTANCE_SECRET

**Purpose**: Instance authentication secret for backend security.

**Required**: When building from source

**Generation**:
```bash
openssl rand -hex 32
```

**Best Practices**:
- Generate unique secret for each deployment
- Never use default from repository
- Rotate regularly
- Store in secret management systems

### DISABLE_BEACON

**Purpose**: Disable anonymous telemetry beacon.

**Required**: No

**Values**: `true` or `false` (default: false)

**Example**:
```bash
DISABLE_BEACON=true
```

**What it disables**:
- Anonymous deployment identifier
- Database migration version
- Git revision
- Backend uptime

**Note**: Messages are printed to logs for transparency when enabled.

### DO_NOT_REQUIRE_SSL

**Purpose**: Disable SSL requirement for connections.

**Required**: No

**Values**: `true` or `false` (default: false)

**Warning**: Only use for development. Never disable SSL in production.

## Storage Variables

### S3-Compatible Storage

#### AWS_REGION

**Purpose**: AWS S3 region.

**Required**: For S3 storage

**Example**:
```bash
AWS_REGION=us-east-1
```

#### AWS_ACCESS_KEY_ID

**Purpose**: AWS access key ID.

**Required**: For S3 storage

**Example**:
```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
```

#### AWS_SECRET_ACCESS_KEY

**Purpose**: AWS secret access key.

**Required**: For S3 storage

**Example**:
```bash
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

#### AWS_S3_BUCKET

**Purpose**: S3 bucket name.

**Required**: For S3 storage

**Example**:
```bash
AWS_S3_BUCKET=my-convex-files
```

#### AWS_ENDPOINT

**Purpose**: S3-compatible endpoint (for MinIO, Wasabi, etc.).

**Required**: For S3-compatible storage

**Example**:
```bash
AWS_ENDPOINT=https://s3.wasabisys.com
```

#### S3_FORCE_PATH_STYLE

**Purpose**: Use path-style URLs for S3 (required for some S3-compatible services).

**Required**: For MinIO and some S3-compatible services

**Values**: `true` or `false`

**Example**:
```bash
S3_FORCE_PATH_STYLE=true
```

## Application Variables

### NODE_ENV

**Purpose**: Application environment mode.

**Values**: `development`, `production`, `test`

**Example**:
```bash
NODE_ENV=production
```

### RUST_LOG

**Purpose**: Rust log level for backend.

**Values**: `error`, `warn`, `info`, `debug`, `trace`

**Example**:
```bash
RUST_LOG=info,convex=debug
```

**Log Levels**:
| Level | Description |
|-------|-------------|
| `error` | Only errors |
| `warn` | Warnings and errors |
| `info` | General information (default) |
| `debug` | Detailed debugging |
| `trace` | Very detailed tracing |

## Coder Workspace Variables

### Coder-Specific URLs

For Coder workspaces, use automatic port-based DNS routing:

```bash
# Convex API (port 3210)
CONVEX_CLOUD_ORIGIN=https://convex-api--<workspace>--<owner>.coder.<domain>

# Dashboard (port 6791)
CONVEX_DASHBOARD_URL=https://convex--<workspace>--<owner>.coder.<domain>

# Frontend (port 3000)
FRONTEND_URL=https://app--<workspace>--<owner>.coder.<domain>
```

> **Note**: Replace `<workspace>`, `<owner>`, and `<domain>` with your specific Coder environment values.

### Coder Postgres Configuration

```bash
# Use POSTGRES_URL (not DATABASE_URL)
POSTGRES_URL=postgres://user:pass@host.coder-dev-envs:5432?sslmode=disable
INSTANCE_NAME=app  # Must match PostgreSQL database name
```

## Environment Variable Precedence

1. **Docker environment variables** (highest priority)
2. **Environment files** (.env, .env.local)
3. **System environment variables**
4. **Default values** (lowest priority)

## CLI Behavior

### Environment Variable Mixing

The CLI **prevents** using both cloud and self-hosted variables simultaneously. This prevents accidental deployments to the wrong environment.

**Cloud Variables** (blocked with self-hosted):
- `CONVEX_DEPLOYMENT`
- `CONVEX_PROD_URL`

**Self-Hosted Variables** (blocked with cloud):
- `CONVEX_SELF_HOSTED_URL`
- `CONVEX_SELF_HOSTED_ADMIN_KEY`

### Setting Environment Variables

```bash
# List all environment variables
npx convex env list

# Set a variable
npx convex env set VARIABLE_NAME "value"

# Remove a variable
npx convex env unset VARIABLE_NAME

# Pull variables to .env.local file
npx convex dev
```

## Production Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
*.pem
*.key
jwt_private_key.pem
```

### 2. Use Secrets Management

**Docker Secrets**:
```yaml
services:
  convex-backend:
    secrets:
      - convex_admin_key
      - instance_secret
    environment:
      - CONVEX_ADMIN_KEY_FILE=/run/secrets/convex_admin_key
      - INSTANCE_SECRET_FILE=/run/secrets/instance_secret

secrets:
  convex_admin_key:
    external: true
  instance_secret:
    external: true
```

**Kubernetes Secrets**:
```yaml
env:
  - name: CONVEX_ADMIN_KEY
    valueFrom:
      secretKeyRef:
        name: convex-secrets
        key: admin-key
```

### 3. Environment-Specific Configs

**Development** (.env.development):
```bash
CONVEX_SELF_HOSTED_URL=http://localhost:3210
DISABLE_BEACON=true
RUST_LOG=debug
```

**Production** (.env.production):
```bash
CONVEX_SELF_HOSTED_URL=https://convex.yourdomain.com
DISABLE_BEACON=false
RUST_LOG=info
```

### 4. Rotate Keys Regularly

- Admin keys: Quarterly
- JWT keys: Quarterly
- Instance secrets: When compromised or annually

### 5. Audit Regularly

```bash
# List all variables
npx convex env list

# Check for sensitive data exposure
git log --all --full-history --source -- "*.env*"
```

## Troubleshooting

### Issue: Database Connection Errors

**Error**:
```
cluster url already contains db name: /app
```

**Solution**:
- Use `POSTGRES_URL` instead of `DATABASE_URL`
- Remove database name from URL
- Set `INSTANCE_NAME` to match database name

### Issue: Multi-line Environment Variables

**Error**: PEM keys fail when set via CLI

**Solutions**:
1. Use dashboard UI to set environment variables
2. Base64-encode the value before storing
3. Use file-based secrets (Docker Secrets)

### Issue: Variables Not Applied

**Symptoms**: Changes not reflected in application

**Solutions**:
1. Restart Docker containers
2. Run `npx convex dev` to regenerate .env.local
3. Verify variable is set: `npx convex env list`

## Quick Reference

### Required for Self-Hosting

```bash
CONVEX_SELF_HOSTED_URL=http://your-backend:3210
CONVEX_SELF_HOSTED_ADMIN_KEY=your-admin-key
```

### Required for Authentication

```bash
JWT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
JWKS='{"keys":[...]}'
JWT_ISSUER=https://your-convex-url.com
CONVEX_SITE_ORIGIN=https://convex-site--workspace--user.coder.domain  # Set via npx convex env set
```

### Required for PostgreSQL

```bash
POSTGRES_URL=postgres://user:pass@host:5432?sslmode=require
INSTANCE_NAME=app
```

### Required for S3 Storage

```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket
```

### Optional Security

```bash
INSTANCE_SECRET=$(openssl rand -hex 32)
DISABLE_BEACON=true
```
