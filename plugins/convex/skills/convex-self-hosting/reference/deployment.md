# Deployment Methods

Comprehensive guide for deploying self-hosted Convex using different methods.

## Docker Deployment (Recommended)

### Prerequisites

- Docker and Docker Compose installed
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

### Default Storage Configuration

By default, Docker setup uses:
- **SQLite** database (stored in Docker volume)
- **Local filesystem** for file storage

> **Warning**: This is recommended for initial setups but **not recommended for production**.

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

**Gotcha**: Use `POSTGRES_URL` instead of `DATABASE_URL` for better compatibility. Remove database name from URL - Convex adds it based on `INSTANCE_NAME`.

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

### Docker Compose Configuration

```yaml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
    ports:
      - "3210:3210"  # Convex API
      - "3211:3211"  # HTTP actions
      - "6791:6791"  # Dashboard
    environment:
      - CONVEX_CLOUD_ORIGIN=http://127.0.0.1:3210
      - POSTGRES_URL=postgres://user:pass@postgres:5432?sslmode=disable
      - INSTANCE_NAME=app
    volumes:
      - convex-data:/convex/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3210/version"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app  # Must match INSTANCE_NAME
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  convex-data:
  postgres-data:
```

### Docker Commands

```bash
# Start services
docker compose up

# Start in detached mode
docker compose up -d

# View logs
docker compose logs -f backend

# Stop services
docker compose down

# Generate admin key
docker compose exec backend ./generate_admin_key.sh

# Execute commands in container
docker compose exec backend bash
```

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

### Platform Support

| Platform | Support Level |
|----------|---------------|
| **Linux** | Battle-tested |
| **macOS** | Battle-tested |
| **Windows** | Less experience |

## Production Configuration

### Database Options

#### SQLite (Default)
- Simple setup
- Not recommended for production
- Limited scalability

#### PostgreSQL/MySQL (Recommended)

```bash
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

**Gotcha**: You must create a database named `convex_self_hosted` for Postgres setups.

### File Storage Options

#### Local Filesystem (Default)
- Simple setup
- Not recommended for production

#### Amazon S3 (Recommended)

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket
```

## Version Management

> **Critical**: Never use `latest` tag in production. Always pin to specific versions.

**Docker Compose**:
```yaml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:v0.15.0  # Pin version
```

**Migration Management**:
- Identify required SQL migrations for each version
- Run migrations in sequence from current to target
- OR export from old, import to new

## Self-Hosted vs Convex Cloud

| Feature | Self-Hosted | Convex Cloud |
|---------|-------------|--------------|
| **Dashboard** | None (use CLI) | Web dashboard at convex.dev |
| **Deployment URL** | Custom internal URL | `*.convex.cloud` |
| **Admin Key** | Generated via Docker | Auto-provisioned |
| **Environment Variables** | `.env` file | Dashboard UI |
| **Initial Setup** | Manual | Guided in dashboard |
| **Pricing** | Self-managed infrastructure | Usage-based pricing |

## Default Ports and Endpoints

| Service | Port | Description | Cloud Equivalent |
|---------|------|-------------|------------------|
| **Convex Backend API** | 3210 | Main API endpoint (WebSocket + HTTP) | `*.convex.cloud` |
| **Convex HTTP Actions** | 3211 | HTTP action endpoints | `*.convex.site` |
| **Convex Dashboard** | 6791 | Web-based management UI | `dashboard.convex.dev` |

**Internal URLs** (accessible within backend functions):
- `process.env.CONVEX_CLOUD_ORIGIN` - Backend API URL
- `process.env.CONVEX_SITE_ORIGIN` - HTTP actions URL (site proxy)

## System Resources

| Resource | Minimum | Recommended (with Postgres) |
|----------|---------|-----------------------------|
| **RAM** | 2 GB | 4 GB |
| **CPU** | 1-2 cores | 2-4 cores |
| **Disk** | 10 GB | 50+ GB (SSD recommended) |
| **Network** | 100 Mbps | 1 Gbps |

**Base Memory Usage**: ~225MB for the Convex backend (surprisingly high for Rust, due to TypeScript runtime).

## CLI Gotchas

### Environment Variable Mixing

The CLI **prevents** using both cloud and self-hosted variables simultaneously. You can't accidentally deploy to the wrong environment.

### Auth CLI Limitation

The CLI **does not support** self-hosted deployments for Convex Auth. Manual setup required. See [Authentication Guide](authentication.md).

### Multi-line Environment Variables

**Issue**: PEM keys and other multi-line values fail when set via CLI.

**What Doesn't Work**:
```bash
cat /tmp/key.pem | npx convex env set PRIVATE_KEY -
```

**Workarounds**:
1. Use dashboard UI to set environment variables
2. Try base64-encoding the value before storing
3. Use file-based secrets (Docker Secrets)
