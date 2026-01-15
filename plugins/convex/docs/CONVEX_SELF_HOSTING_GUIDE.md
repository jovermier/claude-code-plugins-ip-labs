# Self-Hosting Convex: A Comprehensive Guide

> **TL;DR**: Self-hosting Convex is possible via Docker or building from source, but comes with significant operational responsibilities. For most users, the Convex Cloud service remains the recommended option due to managed scaling, migrations, and support. Self-hosting is best suited for specific requirements like data sovereignty, compliance, or integration with existing infrastructure.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture and Components](#architecture-and-components)
3. [Self-Hosting Methods](#self-hosting-methods)
4. [Docker Deployment (Recommended)](#docker-deployment-recommended)
5. [Building from Source](#building-from-source)
6. [Production Configuration](#production-configuration)
7. [Authentication with @convex-dev/auth](#authentication-with-convex-devauth)
8. [Operational Responsibilities](#operational-responsibilities)
9. [Security and Hardening](#security-and-hardening)
10. [Monitoring and Observability](#monitoring-and-observability)
11. [Backup and Disaster Recovery](#backup-and-disaster-recovery)
12. [Performance and Scaling](#performance-and-scaling)
13. [Platform-Specific Deployments](#platform-specific-deployments)
14. [Gotchas and Non-Obvious Issues](#gotchas-and-non-obvious-issues)
15. [Limitations](#limitations)
16. [Resources and Community](#resources-and-community)

---

## Overview

### What is Convex?

Convex is a Backend-as-a-Service (BaaS) platform that provides:
- A **reactive database** with real-time synchronization
- **Serverless function compute** using TypeScript
- **Client libraries** for automatic real-time updates

[Source: Convex Official Site](https://www.convex.dev/) [Source: Dev.to Article](https://dev.to/gimnathperera/unlocking-the-potential-of-convexdev-revolutionizing-backend-development-2fpn)

### The Open-Source Commitment

Convex open-sourced its core backend in **February 2025**, including:
- **200,000+ lines of Rust** code for the reactive database
- **TypeScript components** for UDF runtime
- **Dashboard** and **CLI** tools
- **Client libraries** for multiple platforms (JavaScript, Python, Rust, Swift, Kotlin)

The self-hosted version runs the **same fully up-to-date code** as the cloud service.

[Source: GitHub Repository](https://github.com/get-convex/convex-backend) [Source: Reddit Announcement](https://www.reddit.com/r/programming/comments/1cdlloi/open_sourcing_200k_lines_of_convex_a_reactive) [Source: Open Source Announcement](https://news.convex.dev/self-hosting/)

### License

**FSL Apache 2.0 License** - A modified Apache license that converts to standard Apache 2.0 after 4 years.

This allows you to:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Sublicense
- ✅ Use专利权利终止于4年后

[Source: Convex Self-Hosting Docs](https://docs.convex.dev/self-hosting)

### Official Self-Hosting Warning

> "Self hosting is not for everyone. If you're looking for a more hands-off solution, we recommend using the Convex-hosted product."

> "While the process of setting up a self-hosted backend is very simple, the work to run a production system is never easy."

[Source: Official Documentation](https://docs.convex.dev/self-hosting) [Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

---

## Architecture and Components

### Backend Architecture

| Component | Language | Purpose |
|-----------|----------|---------|
| Core Database | Rust | Reactive data storage and queries |
| Runtime | Rust | Function execution environment |
| UDF Runtime | TypeScript | User-defined function execution |
| System UDFs | TypeScript | Built-in functions |

[Source: GitHub Repository Structure](https://github.com/get-convex/convex-backend)

### Self-Hosted Stack Requirements

A complete self-hosted Convex setup requires **three services**:

1. **Convex Backend** - The core backend service
2. **Convex Dashboard** - Web-based management interface
3. **Frontend Application** - Your application (can be hosted separately)

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Default Ports and Endpoints

| Service | Port | Description | Cloud Equivalent |
|---------|------|-------------|------------------|
| **Convex Backend API** | 3210 | Main API endpoint (WebSocket + HTTP) | `*.convex.cloud` |
| **Convex HTTP Actions** | 3211 | HTTP action endpoints | `*.convex.site` |
| **Convex Dashboard** | 6791 | Web-based management UI | `dashboard.convex.dev` |

**Internal URLs** (accessible within backend functions):
- `process.env.CONVEX_CLOUD_URL` - Backend API URL
- `process.env.CONVEX_SITE_URL` - HTTP actions URL

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md) [Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### System Resources

| Resource | Minimum | Recommended (with Postgres) |
|----------|---------|-----------------------------|
| **RAM** | 2 GB | 4 GB |
| **CPU** | 1-2 cores | 2-4 cores |
| **Disk** | 10 GB | 50+ GB (SSD recommended) |
| **Network** | 100 Mbps | 1 Gbps |

**Base Memory Usage**: ~225MB for the Convex backend (surprisingly high for Rust, due to TypeScript runtime).

[Source: GitHub Issue #225](https://github.com/get-convex/convex-backend/issues/225)

---

## Self-Hosting Methods

### Comparison Table

| Method | Difficulty | Use Case | Scaling | Cost |
|--------|------------|----------|---------|------|
| **Docker Compose** | Low-Medium | Production self-hosting | Single-node | Low |
| **Prebuilt Binary** | Low | Simple deployments | Single-node | Low |
| **Build from Source** | High | Contributors, customization | Single-node | Free |
| **PaaS (Fly.io)** | Medium | Managed but self-hosted | Single-node | Medium |
| **Kubernetes** | High | Large-scale deployments | Single-node* | High |

*Horizontal scaling requires code modifications.

> **⚠️ CRITICAL**: All self-hosted methods are **single-node by default**. Distributed scaling requires modifying the Rust codebase.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

---

## Docker Deployment (Recommended)

### Prerequisites

- Docker and Docker Compose
- Convex CLI (`npm install convex@latest`)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/get-convex/convex-backend
cd convex-backend/self-hosted

# 2. Start the services
docker compose up

# 3. Generate an admin key
docker compose exec backend ./generate_admin_key.sh

# 4. Configure your project
cat > .env.local << EOF
CONVEX_SELF_HOSTED_URL=http://127.0.0.1:3210
CONVEX_SELF_HOSTED_ADMIN_KEY=<your-generated-key>
EOF

# 5. Deploy your code
npx convex deploy
```

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Default Storage Configuration

By default, the Docker setup uses:
- **SQLite** database (stored in Docker volume)
- **Local filesystem** for file storage

This is **recommended for initial setups** but **not recommended for production**.

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Environment Variables

#### Required Variables

| Variable | Purpose | Example | Required |
|----------|---------|---------|----------|
| `CONVEX_SELF_HOSTED_URL` | Backend API URL | `http://127.0.0.1:3210` | Yes |
| `CONVEX_SELF_HOSTED_ADMIN_KEY` | Admin authentication | Generated key | Yes |
| `CONVEX_CLOUD_ORIGIN` | Backend API endpoint | `https://your-domain.com` | For PaaS |
| `CONVEX_SITE_ORIGIN` | HTTP actions endpoint | `https://your-site.com` | For PaaS |
| `INSTANCE_NAME` | Instance identifier | `app` | For Postgres |

#### Database Configuration

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | Postgres connection string | `postgresql://user:pass@host:5432/dbname` |
| `POSTGRES_URL` | Alternative Postgres URL (preferred) | `postgres://user:pass@host:5432?sslmode=require` |

**⚠️ GOTCHA**: Use `POSTGRES_URL` instead of `DATABASE_URL` for better compatibility. Remove database name from URL - Convex adds it based on `INSTANCE_NAME`.

#### Security Configuration

| Variable | Purpose | Example |
|----------|---------|---------|
| `INSTANCE_SECRET` | Instance authentication secret | Generate with `openssl rand -hex 32` |
| `CONVEX_ADMIN_KEY` | Dashboard/deployment access | Generated via script |
| `DISABLE_BEACON` | Disable telemetry beacon | `true` |
| `DO_NOT_REQUIRE_SSL` | Disable SSL requirement | `false` (for production) |

#### S3 Storage Configuration

| Variable | Purpose | Example |
|----------|---------|---------|
| `AWS_REGION` | S3 region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | `your-key` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret | `your-secret` |
| `AWS_S3_BUCKET` | S3 bucket name | `your-bucket` |
| `AWS_ENDPOINT` | S3-compatible endpoint | `https://s3.wasabisys.com` |
| `S3_FORCE_PATH_STYLE` | Use path-style URLs | `true` (for MinIO) |

**⚠️ GOTCHA**: The CLI **prevents mixing** cloud and self-hosted environment variables to avoid accidental deployments.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy) [Source: S3 Storage Guide](https://github.com/get-convex/convex-backend/blob/main/self-hosted/advanced/s3_storage.md)

---

## Building from Source

### Prerequisites

| Tool | Purpose | Version |
|------|---------|---------|
| **Rust** | Core language | Via `rust-toolchain` file |
| **Node.js** | CLI and scripts | Via `.nvmrc` file |
| **Just** | Command runner | Required |
| **Rush** | Monorepo manager | Required |

### Setup

```bash
# Install Rush
npm clean-install --prefix scripts

# Install JavaScript dependencies
just rush install

# Build and run local backend
just run-local-backend
```

[Source: BUILD.md](https://github.com/get-convex/convex-backend/blob/main/BUILD.md)

### Useful Commands

```bash
# List database tables
just convex data

# Manage environment variables
just convex env

# Stream backend logs
just convex logs --success

# Import data
just convex import

# Export data
just convex export
```

[Source: BUILD.md](https://github.com/get-convex/convex-backend/blob/main/BUILD.md)

### Platform Support

| Platform | Support Level |
|----------|---------------|
| **Linux** | ✅ Battle-tested |
| **macOS** | ✅ Battle-tested |
| **Windows** | ⚠️ Less experience |

[Source: Main README](https://github.com/get-convex/convex-backend)

---

## Production Configuration

### Database Options

#### SQLite (Default)
- ✅ Simple setup
- ❌ Not recommended for production
- ❌ Limited scalability

#### PostgreSQL/MySQL (Recommended)
```bash
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

**⚠️ GOTCHA**: You must create a database named `convex_self_hosted` for Postgres setups.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### File Storage Options

#### Local Filesystem (Default)
- ✅ Simple setup
- ❌ Not recommended for production

#### Amazon S3 (Recommended)
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket
```

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Platform-Specific Configuration

#### Fly.io

Required environment variables:
```bash
CONVEX_CLOUD_ORIGIN=https://your-app.fly.dev
CONVEX_SITE_ORIGIN=https://your-site.fly.dev
```

These are accessible as:
- `process.env.CONVEX_CLOUD_URL`
- `process.env.CONVEX_SITE_URL`

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

---

## Authentication with @convex-dev/auth

@convex-dev/auth is an authentication library for Convex that provides:
- Multiple authentication providers (Anonymous, Email/Password, OAuth)
- JWT-based session management
- User and session management
- Token generation and validation

> **Important**: The CLI does not support self-hosted deployments for Convex Auth. Manual setup is required.
> — [Self-Hosted README](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

[Source: Convex Auth Manual Setup](https://labs.convex.dev/auth/setup/manual)

### Required Environment Variables

#### 1. JWT_PRIVATE_KEY

**Purpose**: RSA private key for signing JWT tokens.

**Format**: Must be **PKCS#8** format (NOT PKCS#1/RSAPrivateKey).

> **PKCS#8** is a generic, standardized format with algorithm identification (uses `BEGIN PRIVATE KEY`), while **PKCS#1** is RSA-specific format (uses `BEGIN RSA PRIVATE KEY`). PKCS#8 is more portable and recommended.
> — [Creating RSA Keys using OpenSSL - Scott Brady](https://www.scottbrady.io/openssl/creating-rsa-keys-using-openssl)

**How to Generate**:
```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem
```

**Verification**: The file should start with:
```
-----BEGIN PRIVATE KEY-----
```

NOT:
```
-----BEGIN RSA PRIVATE KEY-----
```

**Setting in Convex** (using heredoc to preserve multiline format):
```bash
npx convex env set JWT_PRIVATE_KEY << 'PEMEOF'
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCHbqvhQBKUY4pw
...
-----END PRIVATE KEY-----
PEMEOF
```

**Known Issue**: The `convex env set` command fails when trying to set environment variables with multi-line values, such as PEM-formatted private keys. This is a known limitation of the Convex CLI.
> — [GitHub Issue #128: Multi-line environment variables](https://github.com/get-convex/convex-backend/issues/128)

**Alternative Workaround - Base64 Encoding**:
```bash
# Base64 encode the key first
base64 jwt_private_key.pem > jwt_private_key.b64

# Set the base64 version
npx convex env set JWT_PRIVATE_KEY_BASE64 "$(cat jwt_private_key.b64)"

# Decode in your application code
```

> Base64 encoding is a common approach for handling multi-line certificates and private keys as single-line environment variables across various platforms.
> — [Stack Overflow: Using private key in a .env file](https://stackoverflow.com/questions/55459528/using-private-key-in-a-env-file)

#### 2. JWKS (JSON Web Key Set)

**Purpose**: Public key set for verifying JWT signatures. Contains the public key corresponding to JWT_PRIVATE_KEY.

**Required Format**:
```json
{
  "keys": [{
    "kty": "RSA",
    "e": "AQAB",
    "n": "...",
    "alg": "RS256",
    "kid": "unique-key-id",
    "use": "sig"
  }]
}
```

**How to Generate**:

1. Extract public key from private key:
```bash
openssl pkey -in jwt_private_key.pem -pubout -out jwt_public.pem
```

2. Convert to JWK format using Node.js:
```javascript
const fs = require('fs');
const { subtle } = require('crypto').webcrypto;

const publicKeyPem = fs.readFileSync('jwt_public.pem', 'utf-8');
const binaryDer = Buffer.from(
  publicKeyPem
    .replace(/-----BEGIN PUBLIC KEY-----/, '')
    .replace(/-----END PUBLIC KEY-----/, '')
    .replace(/\s/g, ''),
  'base64'
);

subtle.importKey('spki', binaryDer, { name: 'RSA-PSS', hash: 'SHA-256' }, true, ['verify'])
  .then(key => subtle.exportKey('jwk', key))
  .then(jwk => {
    const jwks = {
      keys: [{
        kty: jwk.kty,
        e: jwk.e,
        n: jwk.n,
        alg: 'RS256',
        kid: 'convex-auth-key',  // Generate unique ID for rotation
        use: 'sig'
      }]
    };
    console.log(JSON.stringify(jwks));
  });
```

**Setting in Convex**:
```bash
npx convex env set JWKS '{"keys":[{"kty":"RSA",...}]}'
```

#### 3. JWT_ISSUER

**Purpose**: The issuer URL for JWT tokens. Must match your Convex deployment URL or be configured based on your auth provider.

**For Self-Hosted Convex with Custom Auth**:
```bash
# Use your Convex API URL from Coder DNS routing
JWT_ISSUER=https://convex-api--<workspace>--<owner>.coder.<domain>
```

**For Clerk Integration**:
- Use `CLERK_JWT_ISSUER_DOMAIN` instead
- Set to your Clerk Frontend API URL (found in Clerk Dashboard → API Keys)
- Format: `https://your-app.clerk.accounts.dev`

> For Clerk integration, the Frontend API URL from the Clerk Dashboard is the issuer domain for Clerk's JWT templates.
> — [Convex & Clerk Documentation](https://docs.convex.dev/auth/clerk)

**For Other Auth Providers**:
- **Auth0**: Your Auth0 domain URL (e.g., `https://your-domain.auth0.com`)
- Found in your `.well-known/openid-configuration` endpoint

**Setting in Convex**:
```bash
npx convex env set JWT_ISSUER "https://your-convex-url.com"
```

### Session Management and Token Security

#### Token Expiration and Refresh

Convex Auth uses JWT tokens with the following security characteristics:

> **Refresh Token Security**: Refresh tokens can only be used once to get new access tokens. Using an "old" refresh token will invalidate the entire session. This is a key security feature to prevent token replay attacks.
> — [Convex Auth Security Guide](https://labs.convex.dev/auth/security)

**Session Lifecycle**:
- Session documents exist until the session expires or user signs out
- One user can have many active sessions simultaneously
- Access tokens have short expiration times requiring refresh
> — [Convex Auth Authorization Guide](https://labs.convex.dev/auth/authz)

**JWT-based Authentication**:
- Convex uses OpenID Connect (based on OAuth) ID tokens in JWT form
- JWTs authenticate WebSocket connections
- Compatible with most authentication providers
> — [Convex Authentication Documentation](https://docs.convex.dev/auth)

#### Common Session Issues

**Permanent Unauthenticated State**:
Some users report the Convex React client entering a permanent unauthenticated state after access token expiration, even when AuthKit refreshes tokens properly. This is a known issue being tracked.
> — [GitHub Issue #259](https://github.com/get-convex/convex-backend/issues/259)

**Session Persistence After Page Refresh**:
Google OAuth sessions may not persist after browser refresh, showing "Invalid" errors in Convex logs.
> — [GitHub Issue #193](https://github.com/get-convex/convex-auth/issues/193)

### Docker Configuration for Auth

#### Custom Entrypoint for Base64-Encoded Keys

If storing JWT_PRIVATE_KEY as base64 (for Docker env file compatibility), use a custom entrypoint:

**docker-entrypoint.sh**:
```bash
#!/bin/sh
set -e

# Decode JWT_PRIVATE_KEY from base64 if provided
if [ -n "$JWT_PRIVATE_KEY_BASE64" ]; then
  echo "Decoding JWT_PRIVATE_KEY from base64..."
  JWT_PRIVATE_KEY=$(echo "$JWT_PRIVATE_KEY_BASE64" | base64 -d)
  export JWT_PRIVATE_KEY
  echo "JWT_PRIVATE_KEY decoded (length: ${#JWT_PRIVATE_KEY})"
fi

# Run the original entrypoint
exec ./run_backend.sh "$@"
```

**docker-compose.convex.yml**:
```yaml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
    entrypoint: ["/docker-entrypoint.sh"]
    volumes:
      - ./docker-entrypoint.sh:/docker-entrypoint.sh:ro
```

### Key Rotation Strategy

> **Best Practice**: Rotate admin keys and JWT keys regularly (quarterly recommended). Use different keys for dev/staging/production.
> — [Convex Self-Hosting Guide](https://stack.convex.dev/self-hosted-develop-and-deploy)

**Key Rotation Process**:
1. Generate new key pair
2. Add new public key to JWKS (with new `kid`)
3. Deploy new keys to Convex
4. Verify tokens are issued with new key
5. Monitor for any issues
6. Remove old key from JWKS after verification period

### Security Considerations

1. **Never commit** `jwt_private_key.pem` to version control
2. Add to `.gitignore`:
   ```
   jwt_private_key.pem
   *.pem
   *.key
   .env.local
   .env.convex.local
   ```
3. Use different keys for dev/staging/production
4. Rotate keys regularly (quarterly recommended)
5. Store keys in secret management systems for production

### Troubleshooting Auth Issues

#### Common Error: Missing JWKS

**Error**:
```
Missing environment variable `JWKS`
```

**Solution**: Generate and set JWKS from the public key (see above).

#### Common Error: PKCS#8 Format

**Error**:
```
Uncaught TypeError: "pkcs8" must be PKCS#8 formatted string
```

**Solution**:
1. Ensure key was generated with `openssl genpkey` (not `openssl genrsa`)
2. Verify key starts with `-----BEGIN PRIVATE KEY-----`
3. Use heredoc syntax when setting via CLI

#### Common Error: Auth Provider Discovery Failed

**Error**:
```
Auth provider discovery failed: 500 Internal Server Error
```

**Causes**:
1. Missing JWKS environment variable
2. JWT_PRIVATE_KEY format incorrect
3. JWT_ISSUER mismatch with deployment URL

**Verification**: Check that all three environment variables are set:
```bash
npx convex env list
```

Should show:
```
JWT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...
JWT_ISSUER=https://your-url
JWKS={"keys":[...]}
```

### Complete Auth Setup Script

```bash
#!/bin/bash
set -e

# 1. Generate RSA key pair
echo "Generating RSA key pair..."
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem
openssl pkey -in jwt_private_key.pem -pubout -out jwt_public.pem

# 2. Generate JWKS
echo "Generating JWKS..."
node -e "
const fs = require('fs');
const { subtle } = require('crypto').webcrypto;

const publicKeyPem = fs.readFileSync('jwt_public.pem', 'utf-8');
const binaryDer = Buffer.from(
  publicKeyPem
    .replace(/-----BEGIN PUBLIC KEY-----/, '')
    .replace(/-----END PUBLIC KEY-----/, '')
    .replace(/\s/g, ''),
  'base64'
);

subtle.importKey('spki', binaryDer, { name: 'RSA-PSS', hash: 'SHA-256' }, true, ['verify'])
  .then(key => subtle.exportKey('jwk', key))
  .then(jwk => {
    const jwks = { keys: [{ kty: jwk.kty, e: jwk.e, n: jwk.n, alg: 'RS256', kid: 'convex-auth-key', use: 'sig' }] };
    fs.writeFileSync('jwks.json', JSON.stringify(jwks, null, 2));
  });
"

# 3. Set environment variables in Convex
echo "Setting Convex environment variables..."
export CONVEX_SELF_HOSTED_URL="http://127.0.0.1:3210"
export CONVEX_SELF_HOSTED_ADMIN_KEY="your-admin-key"

# Set JWT_PRIVATE_KEY using heredoc
npx convex env set JWT_PRIVATE_KEY << 'PEMEOF'
$(cat jwt_private_key.pem)
PEMEOF

# Set JWKS
npx convex env set JWKS "$(cat jwks.json)"

# Set JWT_ISSUER
npx convex env set JWT_ISSUER "https://your-convex-url.com"

# 4. Deploy
echo "Deploying Convex functions..."
npx convex deploy --yes

echo "✅ Auth setup complete!"
```

---

## Operational Responsibilities

### What You're Responsible For

| Responsibility | Convex Cloud | Self-Hosted |
|----------------|--------------|-------------|
| **Scaling** | ✅ Managed | ❌ Your responsibility |
| **Migrations** | ✅ Automatic | ❌ Manual |
| **Backups** | ✅ Automatic | ❌ Manual |
| **Monitoring** | ✅ Included | ❌ Your setup |
| **Security Updates** | ✅ Automatic | ❌ Manual |
| **Support** | ✅ Available | ❌ Community only |

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Scaling Challenges

The self-hosted Convex is **single-node by default**. The Convex Cloud service uses:
- Distributed text search
- Separate function execution services
- Dedicated WebSocket handling

To achieve similar scalability:
- You must **modify the Rust codebase**
- Separate services manually
- Build your own distributed system

> **💡 REALITY CHECK**: For most applications that need to scale, Convex Cloud is "a safer (and likely cheaper) bet."

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Migration Management

When upgrading between versions:
1. **Identify required SQL migrations** for each version
2. **Run migrations in sequence** from current to target
3. **OR export from old, import to new**

**⚠️ GOTCHA**: Never use `latest` tag in production. Always pin to specific versions.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Failure Recovery

You must implement:
- Database replication
- Regular snapshots/backups
- Disaster recovery procedures
- Monitoring and alerting
- Automatic restart mechanisms

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

---

## Security and Hardening

### Authentication Best Practices

#### Admin Key Management

Generate a secure admin key for your self-hosted instance:

```bash
# Inside the container
docker compose exec backend ./generate_admin_key.sh
```

**Best Practices**:
- Never commit admin keys to version control
- Rotate admin keys regularly (quarterly recommended)
- Use different keys for dev/staging/production
- Store in secret management systems (Vault, AWS Secrets Manager, Docker Secrets)

#### Instance Secret

When building from source, **always generate a unique instance secret**:

```bash
openssl rand -hex 32
```

**⚠️ CRITICAL**: Never use default instance secrets from repository.

[Source: Main README](https://github.com/get-convex/convex-backend)

### Network Security

#### Firewall Rules

Only expose necessary ports:

```bash
# Allow only necessary traffic
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 22/tcp    # SSH (limit to specific IPs)
ufw deny 3210/tcp   # Don't expose Convex API directly
ufw deny 3211/tcp   # Don't expose site proxy directly
ufw deny 6791/tcp   # Don't expose dashboard publicly
ufw enable
```

#### Reverse Proxy Configuration

Place Convex behind a reverse proxy (nginx, Caddy, Traefik):

**nginx Example**:

```nginx
# /etc/nginx/sites-available/convex
server {
    listen 443 ssl http2;
    server_name convex.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Convex API (WebSocket support)
    location / {
        proxy_pass http://localhost:3210;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}

# Dashboard (restrict access)
server {
    listen 443 ssl http2;
    server_name convex-dashboard.yourdomain.com;

    # IP whitelist
    allow 1.2.3.4/32;  # Your office IP
    deny all;

    location / {
        proxy_pass http://localhost:6791;
        proxy_set_header Host $host;
    }
}
```

**Caddy Example** (automatic HTTPS):

```caddy
convex.yourdomain.com {
    reverse_proxy localhost:3210
}

convex-dashboard.yourdomain.com {
    reverse_proxy localhost:6791
    # Add authentication via Caddy's basic_auth module
}
```

[Source: NGINX SSL Reverse Proxy Guide](https://miguelabate.com/nginx-ssl-reverse-proxy/)

### Secrets Management

#### Docker Secrets

```yaml
# docker-compose.yml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
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

#### Environment-Based

For development, use `.env` files (never commit):

```bash
# .env
CONVEX_ADMIN_KEY=your_key_here
INSTANCE_SECRET=your_secret_here
DATABASE_URL=postgresql://user:pass@host/dbname
```

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

### Rate Limiting

#### nginx Rate Limiting

```nginx
# In http block
limit_req_zone $binary_remote_addr zone=convex_limit:10m rate=10r/s;

# In location block
location / {
    limit_req zone=convex_limit burst=20 nodelay;
    proxy_pass http://localhost:3210;
}
```

#### Cloudflare Integration

1. Enable Cloudflare Proxy (orange cloud)
2. Configure rate limiting rules
3. Enable Web Application Firewall (WAF)
4. Enable Bot Fight Mode

[Source: nginx Rate Limiting Guide](https://blog.nginx.org/blog/rate-limiting-nginx)

### TLS/SSL Configuration

#### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d convex.yourdomain.com

# Auto-renewal is configured automatically
```

#### Caddy (Automatic HTTPS)

Caddy automatically obtains and renews TLS certificates from Let's Encrypt.

---

## Monitoring and Observability

### Health Checks

Convex exposes a health check endpoint:

```
http://localhost:3210/version
```

**Docker Healthcheck**:

```yaml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3210/version"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Logging Configuration

#### Log Levels

```bash
RUST_LOG=info,convex=debug
```

| Level | Description |
|-------|-------------|
| `error` | Only errors |
| `warn` | Warnings and errors |
| `info` | General information (default) |
| `debug` | Detailed debugging |
| `trace` | Very detailed tracing |

#### Streaming Logs

```bash
# Stream all logs
npx convex logs

# Include successful function executions
npx convex logs --success

# Follow logs in real-time
docker compose logs -f backend
```

### Built-in Dashboard Features

The Convex dashboard provides:
- Logs view with filtering
- Function execution monitoring
- Real-time data inspection
- Search functionality
- Failure tracking

### External Monitoring

#### Prometheus + Grafana Stack

```yaml
# docker-compose.yml additions
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus-data:/prometheus

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=your-password
  volumes:
    - grafana-data:/var/lib/grafana

volumes:
  prometheus-data:
  grafana-data:
```

**Key Metrics to Monitor**:
- CPU/Memory usage
- Database connections
- Request latency
- Error rates
- Disk usage
- Network traffic

#### PostgreSQL Monitoring

Use `postgres_exporter` for PostgreSQL metrics:

```yaml
postgres-exporter:
  image: prometheuscommunity/postgres-exporter
  environment:
    - DATA_SOURCE_NAME=postgresql://user:pass@postgres:5432/convex_self_hosted?sslmode=disable
  ports:
    - "9187:9187"
```

### Alerting

#### Recommended Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| **High CPU** | > 80% for 5 minutes | Warning |
| **High Memory** | > 90% for 5 minutes | Critical |
| **Database Down** | Connection failed | Critical |
| **High Error Rate** | > 5% error rate | Warning |
| **Disk Space Low** | < 20% free | Warning |

#### AlertManager Configuration

```yaml
# alertmanager.yml
route:
  receiver: 'email-notifications'
  group_by: ['alertname', 'cluster', 'service']

receivers:
  - name: 'email-notifications'
    email_configs:
      - to: 'your-email@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.example.com:587'
```

---

## Backup and Disaster Recovery

### Backup Strategies

#### Convex CLI Export/Import

```bash
# Export all data
npx convex export --filename backup-$(date +%Y%m%d_%H%M%S).zip

# Import data
npx convex import --filename backup-20250115.zip
```

**Features**:
- Complete database snapshot
- Includes all documents and indexes
- Suitable for migrations and disaster recovery

[Source: Import/Export Documentation](https://docs.convex.dev/database/import-export/)

#### Automated Backup Script

```bash
#!/bin/bash
# /usr/local/bin/convex-backup.sh

set -e

BACKUP_DIR="/backups/convex"
RETENTION_DAYS=30
S3_BUCKET="s3://your-backup-bucket"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="convex_backup_${DATE}.zip"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Export data
echo "Starting backup at $(date)"
cd /path/to/convex/project
npx convex export --filename "${BACKUP_DIR}/${BACKUP_FILE}"

# Upload to S3
echo "Uploading to S3"
aws s3 cp "${BACKUP_DIR}/${BACKUP_FILE}" "${S3_BUCKET}/${BACKUP_FILE}"

# Clean old backups
echo "Cleaning old backups (older than ${RETENTION_DAYS} days)"
find ${BACKUP_DIR} -name "convex_backup_*.zip" -mtime +${RETENTION_DAYS} -delete

# Log completion
echo "Backup completed at $(date)"
```

**Setup cron job**:
```bash
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/convex-backup.sh >> /var/log/convex-backup.log 2>&1
```

#### Community Backup Tool

**[convex-self-hosted-backups](https://github.com/orenaksakal/convex-self-hosted-backups)**

Features:
- File storage backup to S3
- Complete database backup via CLI
- Scheduled backups
- Upload to S3

### PostgreSQL Backup Strategies

#### pg_dump (Logical Backup)

```bash
# Full database backup
pg_dump -U username -h localhost -d convex_self_hosted -F c -f backup.dump

# Restore from backup
pg_restore -U username -h localhost -d convex_self_hosted --clean backup.dump
```

#### Continuous Archiving (WAL)

Configure for point-in-time recovery:

```sql
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /wal_archive/%f'
max_wal_senders = 3
wal_keep_size = '1GB'
```

#### Replication Setup

**Master**:
```sql
-- postgresql.conf
listen_addresses = '*'
wal_level = replica
max_wal_senders = 3
wal_keep_size = '1GB'

-- pg_hba.conf
host    replication     replicator      10.0.0.0/8      md5
```

**Replica**:
```bash
# Create replica
pg_basebackup -h master-host -D /var/lib/postgresql/data -U replicator -P -v -R

# Configure recovery
# standby.signal is created automatically by pg_basebackup
```

### S3 Backup Strategies

#### Cross-Region Replication

Configure S3 bucket replication for disaster recovery:

```json
{
  "Role": "arn:aws:iam::account-id:role/replication-role",
  "Rules": [
    {
      "Status": "Enabled",
      "Priority": 1,
      "Filter": {},
      "Destination": {
        "Bucket": "arn:aws:s3:::destination-bucket",
        "ReplicationTime": {
          "Status": "Enabled",
          "Time": {
            "Minutes": 15
          }
        }
      }
    }
  ]
}
```

#### Versioning

Enable S3 versioning for file recovery:

```bash
aws s3api put-bucket-versioning \
  --bucket your-bucket \
  --versioning-configuration Status=Enabled
```

### Disaster Recovery Plan

#### Recovery Time Objectives (RTO/RPO)

| Metric | Target | Strategy |
|--------|--------|----------|
| **RTO** (Recovery Time) | < 4 hours | Automated restore scripts |
| **RPO** (Recovery Point) | < 1 hour | Hourly backups + WAL archiving |

#### Recovery Procedure

1. **Assess damage** - Identify failed components
2. **Restore database** - From latest backup or promote replica
3. **Restore Convex backend** - Deploy to new infrastructure
4. **Verify data integrity** - Run checks
5. **Update DNS** - Point to new infrastructure
6. **Monitor** - Watch for issues

#### Testing

**Monthly restore testing**:
1. Restore to staging environment
2. Verify data integrity
3. Test application functionality
4. Document any issues
5. Update procedures

---

## Performance and Scaling

### Performance Optimization

#### Database Optimization

**PostgreSQL Configuration**:

```sql
-- Configure for Convex workload
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET work_mem = '2621kB';
ALTER SYSTEM SET min_wal_size = '1GB';
ALTER SYSTEM SET max_wal_size = '4GB';

-- Reload configuration
SELECT pg_reload_conf();
```

#### Connection Pooling

**PgBouncer** for high-traffic deployments:

```yaml
# docker-compose.yml
pgbouncer:
  image: pgbouncer/pgbouncer
  environment:
    - DATABASES_HOST=postgres
    - DATABASES_PORT=5432
    - DATABASES_USER=postgres
    - DATABASES_PASSWORD=password
    - DATABASES_DBNAME=convex_self_hosted
    - POOL_MODE=transaction
    - MAX_CLIENT_CONN=1000
    - DEFAULT_POOL_SIZE=50
  ports:
    - "6432:6432"
```

#### Application Optimization

1. **Minimize function execution time**
   - Use efficient algorithms
   - Avoid unnecessary computations
   - Cache frequently accessed data

2. **Use batch operations**
   - Batch writes when possible
   - Use `query.collect()` for multiple reads

3. **Optimize WebSocket connections**
   - Close unused connections
   - Implement reconnection logic

### Scaling Strategies

#### Vertical Scaling

**Increase server resources**:
- CPU: 1 → 2 → 4 → 8 cores
- RAM: 2GB → 4GB → 8GB → 16GB
- Storage: HDD → SSD → NVMe

**When to scale vertically**:
- CPU usage > 70% consistently
- Memory usage > 80% consistently
- Slow query response times

#### Horizontal Scaling Challenges

**⚠️ CRITICAL LIMITATION**: Self-hosted Convex is **single-node by default**.

To scale horizontally:
1. Modify the Rust codebase to separate services
2. Implement load balancing
3. Ensure all instances access the same database
4. Handle WebSocket session affinity

> **"If you want to scale it, you'll need to modify the open-source backend code to scale the various services for your own infrastructure."**

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

**Required for Horizontal Scaling**:
- Separate API, function execution, and WebSocket services
- Shared storage (PostgreSQL + S3)
- Load balancer with sticky sessions
- Stateless function design

#### Performance Benchmarks

| Operation | Expected Latency |
|-----------|------------------|
| **Single record query** | ~1ms (co-located) |
| **Complex query** | 10-100ms |
| **Function execution** | 50-500ms |
| **WebSocket message** | <10ms |

**Note**: Latency increases with distance between Convex backend and database. Co-locate in same datacenter for best performance.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Resource Sizing Guide

| Scale | CPU | RAM | Database | Storage |
|-------|-----|-----|----------|---------|
| **Development** | 1 vCPU | 2 GB | SQLite | 10 GB |
| **Small Production** | 2 vCPUs | 4 GB | Postgres 2 GB | 50 GB SSD |
| **Medium Production** | 4 vCPUs | 8 GB | Postgres 8 GB | 200 GB SSD |
| **Large Production** | 8+ vCPUs | 16+ GB | Postgres 32 GB + Replica | 500+ GB SSD |

---

## Platform-Specific Deployments

### Fly.io Deployment

**[Official Tutorial](https://www.youtube.com/watch?v=YPCgr_hesYM)**

**fly.toml Configuration**:

```toml
# fly.toml
app = "your-convex-app"

[build]
  image = "ghcr.io/get-convex/convex-backend:latest"

[[services]]
  http_checks = []
  internal_port = 3210

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[env]
  CONVEX_CLOUD_ORIGIN = "https://your-app.fly.dev"
  CONVEX_SITE_ORIGIN = "https://your-app.fly.dev"
```

**Deployment Commands**:

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch
flyctl launch

# Set environment variables
flyctl secrets set CONVEX_ADMIN_KEY=your-key

# Deploy
flyctl deploy
```

**Benefits**:
- Automatic restarts
- Built-in TLS
- Easy scaling
- Global deployment

**Limitations**:
- Single-node
- Limited free tier

[Source: Fly.io Deployment Guide](https://stack.convex.dev/self-hosted-develop-and-deploy) [Source: Fly.io Tutorial](https://app.daily.dev/posts/self-hosting-convex-on-fly-io-jewxtagan)

### Railway Deployment

**[Railway Template](https://railway.com/deploy/convex)**

Railway offers one-click deployment with:
- Automatic HTTPS
- Built-in Postgres
- GitHub integration
- Free tier available

**Setup**:
1. Click "Deploy on Railway" button
2. Connect GitHub repository
3. Configure environment variables
4. Deploy!

**Postgres Integration**:

```bash
# Add Railway Postgres
railway add postgres

# Set DATABASE_URL
railway variables set DATABASE_URL=$POSTGRES_URL
```

[Source: Railway Deployment Guide](https://railway.com/deploy/convex) [Source: Railway + Postgres](https://railway.com/deploy/convex-postgres)

### AWS Deployment

**[SST (Serverless Stack) Tutorial](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst/)**

**Infrastructure**:
- **SST** for infrastructure as code
- **EC2** for compute
- **RDS** for database (optional)
- **S3** for file storage

**EC2 Deployment**:

```bash
# Launch EC2 instance (Ubuntu)
ssh ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone https://github.com/get-convex/convex-backend
cd convex-backend/self-hosted
docker compose up -d
```

**SST Configuration** (TypeScript):

```typescript
// stack.ts
import { Convex } from "convex-sst";

new Convex(stack, "Convex", {
  // Configure your Convex instance
});
```

[Source: AWS SST Tutorial](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst/) [Source: EC2 Deployment](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst-ec2/)

### Neon.tech Deployment

**[Neon + Convex Guide](https://neon.com/guides/convex-neon)**

Neon provides serverless Postgres with auto-scaling.

**Setup**:

```bash
# Create Neon database
neonctl create-database convex_self_hosted

# Get connection string
neonctl connection-string

# Set DATABASE_URL
export DATABASE_URL="postgresql://user:pass@host.neon.tech/dbname"
```

**Benefits**:
- Serverless scaling
- Automatic backups
- Branching for development
- Free tier available

[Source: Neon Convex Guide](https://neon.com/guides/convex-neon)

### Self-Managed MinIO

For on-premises S3-compatible storage:

```yaml
# docker-compose.yml
minio:
  image: minio/minio
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"  # API
    - "9001:9001"  # Console
  environment:
    - MINIO_ROOT_USER=admin
    - MINIO_ROOT_PASSWORD=your-password
  volumes:
    - minio-data:/data

# Convex environment
S3_BUCKET_NAME=convex-files
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY_ID=admin
S3_SECRET_ACCESS_KEY=your-password
S3_REGION=us-east-1
S3_FORCE_PATH_STYLE=true
```

[Source: MinIO Self-Hosted Guide](https://selfhostschool.com/minio-self-hosted-s3-storage-guide/)

### Kubernetes Deployment

**Note**: Self-hosted Convex is designed as a single-node deployment. Kubernetes adds complexity but provides:

- Automated deployments
- Self-healing
- Resource management
- Secret management

**Deployment Manifest**:

```yaml
# convex-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: convex-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: convex-backend
  template:
    metadata:
      labels:
        app: convex-backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/get-convex/convex-backend:latest
        ports:
        - containerPort: 3210
        env:
        - name: CONVEX_CLOUD_ORIGIN
          value: "https://convex.example.com"
        - name: CONVEX_ADMIN_KEY
          valueFrom:
            secretKeyRef:
              name: convex-secrets
              key: admin-key
        volumeMounts:
        - name: data
          mountPath: /convex/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: convex-data
---
apiVersion: v1
kind: Service
metadata:
  name: convex-backend
spec:
  selector:
    app: convex-backend
  ports:
  - port: 3210
    targetPort: 3210
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: convex-data
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```

---

## Gotchas and Non-Obvious Issues

### Security Gotchas

#### 1. Default Admin Key
**⚠️ CRITICAL**: When building from source, **always change** the default instance secret and admin key from repository values.

[Source: Main README](https://github.com/get-convex/convex-backend)

#### 2. Beacon Feature
Self-hosted instances send **anonymous telemetry** to Convex:
- Random deployment identifier
- Database migration version
- Git revision
- Backend uptime

**Disable with**: `--disable-beacon` flag

Messages are printed to logs for transparency.

[Source: Main README](https://github.com/get-convex/convex-backend)

### Configuration Gotchas

#### 3. Environment Variable Mixing
The CLI **prevents** using both cloud and self-hosted variables simultaneously. You can't accidentally deploy to the wrong environment.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

#### 4. Database Name for Postgres
When using Postgres, you **must** create a database named `convex_self_hosted`. This is not automatic.

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

#### 5. Latency Considerations
The further your database/storage is from the backend, the higher the latency. For best performance:
- Co-locate services in the same datacenter
- Convex Cloud achieves ~1ms query times via optimization

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Development Workflow Gotchas

#### 6. Local Backend Database State
If backend run fails with "persisted db metadata" error:
```bash
rm convex_local_backend.sqlite3
```

Then restart the backend.

[Source: BUILD.md](https://github.com/get-convex/convex-backend/blob/main/BUILD.md)

#### 7. Don't Run Both Backends
When using local backend with demo apps:
- ✅ Use `just convex dev`
- ❌ Don't use `npm run dev:backend` (if present)

The local command already handles backend synchronization.

[Source: BUILD.md](https://github.com/get-convex/convex-backend/blob/main/BUILD.md)

#### 8. Environment File Updates
Always run `npx convex dev` **before** testing client app when switching between local and cloud. This updates `.env.local` with correct URLs.

[Source: BUILD.md](https://github.com/get-convex/convex-backend/blob/main/BUILD.md)

### CLI Limitations

#### 9. Convex Auth Manual Setup
The CLI **does not support** self-hosted deployments for Convex Auth. Manual setup required.

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Version Management

#### 10. Docker Image Tagging
Never use `latest` tag in production:
- Unwanted upgrades can break compatibility
- Migrations might be required
- Pin to specific versions

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Platform-Specific Gotchas

#### 11. Windows Support
Windows support exists but has "less experience". Issues? Check `#self-hosted` Discord channel.

[Source: Main README](https://github.com/get-convex/convex-backend)

#### 12. Dev Container Challenges
No official dev container config exists. Community reports:
- URL/admin key prompting issues
- Docker-in-Docker complexity

Requires custom `devcontainer.json` setup.

[Source: GitHub Issues #79, #173](https://github.com/get-convex/convex-backend/issues/79)

### Additional Gotchas from Community

#### 13. POSTGRES_URL vs DATABASE_URL

**Issue**: Using `DATABASE_URL` can cause connection errors.

**Error**:
```
cluster url already contains db name: /app
```

**Solution**:
- Use `POSTGRES_URL` instead of `DATABASE_URL`
- Remove database name from URL (Convex adds it based on `INSTANCE_NAME`)
- Use `sslmode=disable` for internal networking

**Example**:
```bash
POSTGRES_URL=postgres://user:pass@host:5432?sslmode=disable
INSTANCE_NAME=app  # Must match PostgreSQL database name
```

#### 14. Large Input Size Crashes

**Issue**: Large argument inputs can cause instance crashes.

**Solution**: Limit argument sizes or implement chunking for large payloads.

[Source: GitHub Issue #179](https://github.com/get-convex/convex-backend/issues/179)

#### 15. DISABLE_BEACON Not Always Obeyed

**Issue**: Beacon telemetry may still send even when `DISABLE_BEACON` is set.

**Status**: Known bug, may require workaround or verify in logs.

[Source: GitHub Issue #194](https://github.com/get-convex/convex-backend/issues/194)

#### 16. Multi-line Environment Variables

**Issue**: PEM keys and other multi-line values fail when set via CLI.

**What Doesn't Work**:
```bash
cat /tmp/key.pem | npx convex env set PRIVATE_KEY -
```

**Workarounds**:
1. Use dashboard UI to set environment variables
2. Try base64-encoding the value before storing
3. Use file-based secrets (Docker Secrets)

[Source: GitHub Issue #128](https://github.com/get-convex/convex-backend/issues/128)

#### 17. JWT_PRIVATE_KEY Format Problem

**Issue**: @convex-dev/auth requires `JWT_PRIVATE_KEY` to be PKCS#8 formatted.

**Error**:
```
Uncaught TypeError: "pkcs8" must be PKCS#8 formatted string
```

**What Works**:
1. Generate correct PKCS#8 key:
   ```bash
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out /tmp/jwt_pkcs8.pem
   ```

2. Key should start with `-----BEGIN PRIVATE KEY-----` (NOT `-----BEGIN RSA PRIVATE KEY-----`)

**What Doesn't Work**:
```bash
cat /tmp/jwt_pkcs8.pem | npx convex env set JWT_PRIVATE_KEY -
```

**Potential Solutions**:
1. Use Convex dashboard UI to set environment variables
2. Try base64-encoding the PEM key before storing
3. Direct database insertion (bypass CLI)

[Source: GitHub Issue #128](https://github.com/get-convex/convex-backend/issues/128) [Source: GitHub Issue #98](https://github.com/get-convex/convex-backend/issues/98)

#### 18. Domain Configuration

**Issue**: Single domain requirement can cause confusion.

**Solution**: Configure both `CONVEX_CLOUD_ORIGIN` and `CONVEX_SITE_ORIGIN` appropriately for your setup.

[Source: GitHub Issue #177](https://github.com/get-convex/convex-backend/issues/177)

#### 19. Version Compatibility

**Issue**: Deploy failures due to version mismatches between CLI and backend.

**Solution**: Ensure backend version matches CLI version. Pin versions in production.

[Source: GitHub Issue #258](https://github.com/get-convex/convex-backend/issues/258)

#### 20. Runtime Limits

**Issue**: Convex functions have runtime limits that may cause unexpected failures.

**Limits**:
- Node.js runtime: 512MB memory limit
- Convex runtime: 64MB memory limit
- Not all NPM packages supported in Actions
- Some Node.js APIs unavailable

[Source: Convex Limits Documentation](https://docs.convex.dev/production/state/limits)

---

## Limitations

### Feature Limitations

**Self-hosted Convex supports all free-tier features of cloud-hosted product.**

Paid tier features may not be available.

[Source: self-hosted/README.md](https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md)

### Support Limitations

> **"Self-hosting doesn't currently have a support plan available from the Convex team."**

Support is **community-only** via:
- `#self-hosted` Discord channel
- GitHub Issues
- GitHub Discussions

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

### Scalability Limitations

| Aspect | Cloud | Self-Hosted |
|--------|-------|-------------|
| **Nodes** | Distributed | Single |
| **Scaling** | Automatic | Manual |
| **Services** | Separated | Monolithic |

[Source: Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)

---

## Resources and Community

### Official Resources

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/get-convex/convex-backend |
| **Self-Hosting Documentation** | https://docs.convex.dev/self-hosting |
| **Self-Hosting Blog Post** | https://stack.convex.dev/self-hosted-develop-and-deploy |
| **Official Site** | https://www.convex.dev/ |
| **Open Source Overview** | https://www.convex.dev/open-source |

### Community Resources

| Resource | Purpose |
|----------|---------|
| **#self-hosted Discord** | Community support |
| **GitHub Issues** | Bug reports and questions |
| **GitHub Discussions** | General discussions |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and quick start |
| `self-hosted/README.md` | Self-hosting specific instructions |
| `BUILD.md` | Building from source guide |
| `self-hosted/advanced/s3_storage.md` | S3 storage configuration |

### Tutorials and Blog Posts

| Resource | Description | Source |
|----------|-------------|--------|
| **Self-Hosting with Convex: Everything You Need to Know** | Official comprehensive guide | [Convex Stack Blog](https://stack.convex.dev/self-hosted-develop-and-deploy) |
| **Self-Hosted Convex on AWS with SST** | AWS deployment with SST infrastructure | [Sean Campbell's Blog](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst/) |
| **Getting Started with Convex and Neon** | Neon Postgres integration guide | [Neon Docs](https://neon.com/guides/convex-neon) |
| **How to Self-Host Convex with Dokploy** | Complete Docker setup guide | [BitDoze](https://www.bitdoze.com/convex-self-host/) |
| **EC2 Deployment Guide** | AWS EC2 specific deployment | [Sean Campbell's Blog](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst-ec2/) |

### Video Tutorials

| Resource | Description | Link |
|----------|-------------|------|
| **Self-hosting Convex on Fly.io** | Official walkthrough | [YouTube](https://www.youtube.com/watch?v=YPCgr_hesYM) |
| **How I Self-Host Convex** | Community experience | [YouTube](https://www.youtube.com/watch?v=lFn27k58VkY) |
| **Run Convex Yourself** | VPS tutorial | [YouTube](https://www.youtube.com/watch?v=rEcOmzYyb1g) |

### Deployment Platforms

| Platform | Documentation | Quick Start |
|----------|---------------|-------------|
| **Fly.io** | [Deployment Guide](https://stack.convex.dev/self-hosted-develop-and-deploy) | `flyctl launch` |
| **Railway** | [Deploy Convex](https://railway.com/deploy/convex) | One-click deploy |
| **Railway + Postgres** | [Convex + Postgres](https://railway.com/deploy/convex-postgres) | One-click deploy |
| **Neon.tech** | [Neon + Convex Guide](https://neon.com/guides/convex-neon) | Serverless Postgres |

### Community Tools

| Tool | Description | Repository |
|------|-------------|------------|
| **convex-self-hosted-backups** | Automated backup script with S3 upload | [GitHub](https://github.com/orenaksakal/convex-self-hosted-backups) |
| **convex-helpers** | CORS and utility helpers | [GitHub](https://github.com/get-convex/convex-helpers) |
| **convex-migrations** | Migration tools and scripts | [GitHub](https://github.com/get-convex/migrations) |

### Support Channels

| Channel | Best For | Link |
|---------|----------|------|
| **#self-hosted Discord** | Community support, real-time help | [Convex Discord](https://www.convex.dev/discord) |
| **GitHub Issues** | Bug reports, feature requests | [Issue Tracker](https://github.com/get-convex/convex-backend/issues) |
| **GitHub Discussions** | General questions, discussions | [Discussions](https://github.com/get-convex/convex-backend/discussions) |
| **Stack Overflow** | Technical Q&A | Tag: `convex-dev` |

---

## Decision Framework

### When to Self-Host

✅ **Consider self-hosting if you need:**
- Data sovereignty/compliance requirements
- Private network/VPC deployment
- Specific geographic data residency
- Unlimited testing environments
- Integration with existing infrastructure
- Custom backend modifications

❌ **Use Convex Cloud if you want:**
- Automatic scaling
- Managed migrations
- Professional support
- Reduced operational overhead
- Focus on application logic

### Migration Path

You can **start on Convex Cloud** and migrate to self-hosted later:
1. Export data from cloud
2. Import to self-hosted
3. Update environment variables
4. Deploy code to self-hosted

---

## Quick Reference

### Docker Commands

```bash
# Start services
docker compose up

# Generate admin key
docker compose exec backend ./generate_admin_key.sh

# View logs
docker compose logs -f backend

# Stop services
docker compose down
```

### Convex CLI Commands

```bash
# Deploy to self-hosted
npx convex deploy

# Run in development mode
npx convex dev

# View database state
npx convex data

# Stream logs
npx convex logs --success

# Manage environment variables
npx convex env
```

### Environment Variables Checklist

```bash
# Required for self-hosted
CONVEX_SELF_HOSTED_URL=http://your-backend:3210
CONVEX_SELF_HOSTED_ADMIN_KEY=your-admin-key

# Optional: External database
DATABASE_URL=postgresql://user:pass@host/db

# Optional: S3 storage
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket

# Optional: Disable beacon
CONVEX_DISABLE_BEACON=true
```

---

## Conclusion

Self-hosting Convex is a **viable option** for organizations with specific requirements around data control, compliance, or infrastructure integration. However, it comes with **significant operational responsibilities** that should not be underestimated.

The **Docker-based approach** is recommended for most self-hosting scenarios, offering a balance of simplicity and flexibility. For contributors or those needing customization, **building from source** provides maximum control.

For the majority of users, especially those prioritizing ease of use, automatic scaling, and professional support, the **Convex Cloud service** remains the recommended choice.

---

## Contributing

Contributions to the self-hosted Convex ecosystem are welcome! Consider:
- Sharing dev container configurations
- Documenting platform-specific deployments
- Contributing to the core codebase
- Helping in the #self-hosted Discord channel

---

## Production Deployment Checklist

### Pre-Deployment Planning

- [ ] **Assess Requirements**
  - [ ] Estimate traffic/load
  - [ ] Define data retention requirements
  - [ ] Identify compliance requirements
  - [ ] Plan backup strategy
  - [ ] Choose hosting platform

- [ ] **Choose Deployment Method**
  - [ ] Docker Compose (self-managed)
  - [ ] Fly.io (managed)
  - [ ] Railway (managed)
  - [ ] AWS/GCP/Azure (cloud)
  - [ ] Kubernetes (orchestrated)

### Infrastructure Setup

- [ ] **Domain and DNS**
  - [ ] Register domain
  - [ ] Configure DNS records
  - [ ] Set up SSL certificates (Let's Encrypt)
  - [ ] Configure reverse proxy (nginx/Caddy)

- [ ] **Database**
  - [ ] Provision PostgreSQL instance
  - [ ] Create `convex_self_hosted` database
  - [ ] Configure connection pooling (if needed)
  - [ ] Set up replication (for production)
  - [ ] Test connection

- [ ] **Storage**
  - [ ] Configure S3 or S3-compatible storage
  - [ ] Create bucket
  - [ ] Set up IAM credentials
  - [ ] Configure lifecycle policies
  - [ ] Enable versioning

- [ ] **Security**
  - [ ] Generate secure `INSTANCE_SECRET`
  - [ ] Generate admin key
  - [ ] Configure firewall rules
  - [ ] Set up reverse proxy with SSL
  - [ ] Configure rate limiting
  - [ ] Set up secrets management
  - [ ] Disable beacon if required

### Application Deployment

- [ ] **Deploy Convex Backend**
  - [ ] Pull/pin specific Docker image version
  - [ ] Configure environment variables
  - [ ] Set up persistent volumes
  - [ ] Configure health checks
  - [ ] Deploy with restart policy

- [ ] **Deploy Dashboard** (optional)
  - [ ] Configure dashboard access
  - [ ] Set up IP whitelist
  - [ ] Add authentication

- [ ] **Deploy Frontend**
  - [ ] Configure `CONVEX_SELF_HOSTED_URL`
  - [ ] Set up CORS if needed
  - [ ] Deploy to hosting platform

- [ ] **Run Migrations**
  - [ ] Backup before migration
  - [ ] Review migration requirements
  - [ ] Test migrations in staging
  - [ ] Execute migrations
  - [ ] Verify data integrity

### Monitoring and Observability

- [ ] **Logging**
  - [ ] Configure log levels
  - [ ] Set up log aggregation
  - [ ] Configure log rotation
  - [ ] Test log streaming

- [ ] **Monitoring**
  - [ ] Set up Prometheus metrics
  - [ ] Configure Grafana dashboards
  - [ ] Set up database monitoring
  - [ ] Configure system monitors

- [ ] **Alerting**
  - [ ] Configure alert rules
  - [ ] Set up notification channels
  - [ ] Test alert delivery
  - [ ] Document on-call procedures

### Backup and Disaster Recovery

- [ ] **Backups**
  - [ ] Set up automated backups
  - [ ] Configure off-site backup storage
  - [ ] Test backup procedures
  - [ ] Document backup locations
  - [ ] Set up backup retention policy

- [ ] **Disaster Recovery**
  - [ ] Document recovery procedures
  - [ ] Test restore procedures
  - [ ] Set up RTO/RPO targets
  - [ ] Configure database replication
  - [ ] Test failover procedures

### Post-Deployment

- [ ] **Verification**
  - [ ] Test all functionality
  - [ ] Verify API endpoints
  - [ ] Check WebSocket connections
  - [ ] Test authentication
  - [ ] Verify file uploads

- [ ] **Performance**
  - [ ] Run load tests
  - [ ] Monitor resource usage
  - [ ] Optimize queries
  - [ ] Tune PostgreSQL configuration

- [ ] **Documentation**
  - [ ] Document architecture
  - [ ] Create runbooks
  - [ ] Document escalation paths
  - [ ] Update team documentation

### Security Review

- [ ] **Security Assessment**
  - [ ] Review access controls
  - [ ] Audit environment variables
  - [ ] Review secrets management
  - [ ] Check for exposed ports
  - [ ] Review SSL/TLS configuration
  - [ ] Test for common vulnerabilities

---

## Coder Workspace Specific Setup

### Environment Characteristics

All Coder workspaces share these characteristics:
- **Platform**: Kubernetes-managed Coder workspace
- **OS**: Linux (Ubuntu/Debian-based), x86_64 architecture
- **Networking**: Internal cluster networking with port forwarding
- **Package Manager**: Detected from lockfile (pnpm/yarn/npm/bun)

### Coder DNS Routing

**Critical**: Using `localhost` URLs causes CORS and authentication issues when accessed from external browsers.

Use Coder's automatic port-based DNS routing:
```
https://<slug>--<workspace>--<owner>.coder.<domain>
```

#### Standard Service Patterns

| Slug | Port | Display Name | URL Pattern |
|------|------|--------------|-------------|
| `app` | 3000 | Dev App | `https://app--<workspace>--<owner>.coder.<domain>` |
| `app-prod` | 3010 | Prod App | `https://app-prod--<workspace>--<owner>.coder.<domain>` |

#### Convex Applications (When Convex Enabled)

| Slug | Port | Display Name | URL Pattern | Visibility |
|------|------|--------------|-------------|------------|
| `convex` | 6791 | Convex Dashboard | `https://convex--<workspace>--<owner>.coder.<domain>` | Public |
| `convex-api` | 3210 | Convex API | `https://convex-api--<workspace>--<owner>.coder.<domain>` | Public (hidden) |
| `convex-proxy` | 3211 | Convex Proxy | `https://convex-proxy--<workspace>--<owner>.coder.<domain>` | Public (hidden) |

> **Note**: Replace `<workspace>`, `<owner>`, and `<domain>` with your specific Coder environment values.

### PostgreSQL Configuration

When using Convex with PostgreSQL in Coder environments:

**Issue**: Connection attempts may fail with:
```
cluster url already contains db name: /app
```

**Solution**:
- Use `POSTGRES_URL` instead of deprecated `DATABASE_URL`
- Remove database name from URL (Convex adds it based on `INSTANCE_NAME`)
- Use `sslmode=disable` for Coder internal networking

**Example**:
```bash
POSTGRES_URL=postgres://user:pass@host.coder-dev-envs:5432?sslmode=disable
INSTANCE_NAME=app  # Must match PostgreSQL database name
```

### Playwright Testing in Coder

**Required System Dependencies**:
```bash
sudo apt-get install -y \
  libnspr4 libnss3 libatk-bridge2.0-0 libdrm2 \
  libxkbcommon0 libgbm1 libxcomposite1 libxcursor1 \
  libxdamage1 libxfixes3 libxi6 libxtst6 libxrandr2 \
  libxss1 libglib2.0-0 libgtk-3-0 libpangocairo-1.0-0 \
  libatk1.0-0 libcairo-gobject2 libasound2t64
```

**Configuration**: Do NOT use `webServer` in playwright.config.ts - tests assume server is already running.

---

## Open Issues and Workarounds

### JWT_PRIVATE_KEY Format Problem

**Issue**: @convex-dev/auth requires `JWT_PRIVATE_KEY` to be a PKCS#8 formatted RSA private key, but setting it via `convex env set` appears to fail.

**Error**:
```
Uncaught TypeError: "pkcs8" must be PKCS#8 formatted string
```

**What Works**:
1. Generate correct PKCS#8 key:
   ```bash
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out /tmp/jwt_pkcs8.pem
   ```

2. Key should start with `-----BEGIN PRIVATE KEY-----` (NOT `-----BEGIN RSA PRIVATE KEY-----`)

**What Doesn't Work**:
```bash
cat /tmp/jwt_pkcs8.pem | npx convex env set JWT_PRIVATE_KEY -
```

**Status**: Unresolved - the key format appears correct when generated, but Convex functions report it as invalid.

**Potential Solutions**:
1. Use Convex dashboard UI to set environment variables
2. Try base64-encoding the PEM key before storing
3. Direct database insertion (bypass CLI)
4. Consider alternative auth mechanisms

**Sources**:
- [Issue #128: Multi-line environment variables](https://github.com/get-convex/convex-backend/issues/128)
- [Issue #98: JWT_PRIVATE_KEY not in environment](https://github.com/get-convex/convex-backend/issues/98)

---

**Last Updated**: Based on Convex backend documentation as of January 2026

**Document Version**: 2.1 (Generic Coder environment support + production deployment guides, security, monitoring, backup strategies, platform-specific deployments, and 20+ gotchas)

**Sources**: All statements in this document are sourced from official Convex documentation, GitHub repository, community discussions, and research from:

- [Convex Developer Hub - Self Hosting](https://docs.convex.dev/self-hosting)
- [get-convex/convex-backend GitHub Repository](https://github.com/get-convex/convex-backend)
- [Self-Hosting with Convex: Everything You Need to Know](https://stack.convex.dev/self-hosted-develop-and-deploy)
- [Self-Hosted Convex on AWS with SST](https://seanpaulcampbell.com/blog/self-hosting-convex-aws-sst/)
- [Getting started with Convex and Neon](https://neon.com/guides/convex-neon)
- [Deploy Convex on Railway](https://railway.com/deploy/convex)
- [Convex Self-Hosting Announcement](https://news.convex.dev/self-hosting/)
- [Data Import & Export Documentation](https://docs.convex.dev/database/import-export/)
- [Backup & Restore Documentation](https://docs.convex.dev/database/backup-restore)
- Various GitHub issues and community discussions

## Changelog

### Version 2.1 (January 2026)
- **Generic Coder Environment Support**: Made Coder workspace section generic to apply to any project
- Replaced hardcoded workspace-specific URLs with placeholder patterns
- Added note that workspace/owner/domain values should be replaced with actual environment values
- Documented standard service URL patterns for any Coder project

### Version 2.0 (January 2026)
- Added comprehensive Security and Hardening section
- Added Monitoring and Observability guide
- Added Backup and Disaster Recovery strategies
- Added Performance and Scaling guidance
- Added Platform-Specific Deployment guides (Fly.io, Railway, AWS, Neon, MinIO, Kubernetes)
- Expanded Gotchas section from 12 to 20 issues
- Added Production Deployment Checklist
- Enhanced Environment Variables reference
- Added S3-compatible storage options
- Added PostgreSQL configuration and optimization
- Added connection pooling guidance
- Added nginx/Caddy reverse proxy examples
- Added community tools and resources

### Version 1.1 (Initial)
- Basic self-hosting guide
- Docker deployment instructions
- Building from source guide
- Core gotchas and limitations
- Coder workspace specific setup
