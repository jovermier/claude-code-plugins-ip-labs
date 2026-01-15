# Platform-Specific Deployment Guides

Guides for deploying self-hosted Convex on various platforms.

## Fly.io Deployment

### Overview

Fly.io provides a simple platform for deploying self-hosted Convex with automatic restarts, built-in TLS, and easy scaling.

### fly.toml Configuration

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

### Deployment Commands

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

### Benefits

- Automatic restarts
- Built-in TLS
- Easy scaling
- Global deployment

### Limitations

- Single-node
- Limited free tier

### Resources

- [Official Tutorial Video](https://www.youtube.com/watch?v=YPCgr_hesYM)
- [Deployment Guide](https://stack.convex.dev/self-hosted-develop-and-deploy)

## Railway Deployment

### Overview

Railway offers one-click deployment with automatic HTTPS, built-in Postgres, and GitHub integration.

### Quick Start

1. Click "Deploy on Railway" button from [Railway Template](https://railway.com/deploy/convex)
2. Connect GitHub repository
3. Configure environment variables
4. Deploy!

### Postgres Integration

```bash
# Add Railway Postgres
railway add postgres

# Set POSTGRES_URL
railway variables set POSTGRES_URL=$POSTGRES_URL
```

### Environment Variables

```bash
# Required
CONVEX_CLOUD_ORIGIN=https://your-app.railway.app
CONVEX_SITE_ORIGIN=https://your-app.railway.app
CONVEX_ADMIN_KEY=your-admin-key

# Optional - Postgres
POSTGRES_URL=${{Postgres.POSTGRES_URL}}
```

### Benefits

- Automatic HTTPS
- Built-in Postgres
- GitHub integration
- Free tier available

### Resources

- [Railway Template](https://railway.com/deploy/convex)
- [Railway + Postgres](https://railway.com/deploy/convex-postgres)

## AWS Deployment

### Overview

AWS deployment provides maximum control and scalability with infrastructure as code options.

### SST (Serverless Stack) Deployment

**Infrastructure**:
- **SST** for infrastructure as code
- **EC2** for compute
- **RDS** for database (optional)
- **S3** for file storage

#### EC2 Deployment

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

#### SST Configuration (TypeScript)

```typescript
// stack.ts
import { Convex } from "convex-sst";

new Convex(stack, "Convex", {
  // Configure your Convex instance
});
```

### Benefits

- Full control over infrastructure
- Scalable (with modifications)
- Integrates with AWS services
- Cost-optimized for scale

### Resources

- [AWS SST Tutorial](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst/)
- [EC2 Deployment Guide](https://seanpaulcampbell.com/blog/self-hosted-convex-aws-sst-ec2/)

## Neon.tech Deployment

### Overview

Neon provides serverless Postgres with auto-scaling and branching for development.

### Setup

```bash
# Install neonctl
npm install -g neonctl

# Create Neon database
neonctl create-database convex_self_hosted

# Get connection string
neonctl connection-string

# Set POSTGRES_URL
export POSTGRES_URL="postgresql://user:pass@host.neon.tech/dbname"
```

### Environment Variables

```bash
POSTGRES_URL=postgresql://user:pass@host.neon.tech/dbname
CONVEX_SELF_HOSTED_URL=https://your-convex-url.com
```

### Benefits

- Serverless scaling
- Automatic backups
- Branching for development
- Free tier available

### Resources

- [Neon + Convex Guide](https://neon.com/guides/convex-neon)

## Self-Managed MinIO

### Overview

MinIO provides S3-compatible storage for on-premises deployments.

### Docker Compose Configuration

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

### Environment Variables for Convex

```bash
AWS_ACCESS_KEY_ID=admin
AWS_SECRET_ACCESS_KEY=your-password
AWS_REGION=us-east-1
AWS_S3_BUCKET=convex-files
AWS_ENDPOINT=http://minio:9000
S3_FORCE_PATH_STYLE=true
```

### Benefits

- On-premises storage
- S3-compatible API
- Self-hosted and private
- No external dependencies

### Resources

- [MinIO Self-Hosted Guide](https://selfhostschool.com/minio-self-hosted-s3-storage-guide/)

## Kubernetes Deployment

### Overview

Kubernetes provides automated deployments, self-healing, resource management, and secret management.

### Deployment Manifest

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
---
apiVersion: v1
kind: Secret
metadata:
  name: convex-secrets
type: Opaque
stringData:
  admin-key: "your-admin-key-here"
  instance-secret: "your-instance-secret-here"
```

### Apply Configuration

```bash
kubectl apply -f convex-deployment.yaml
```

### Benefits

- Automated deployments
- Self-healing
- Resource management
- Secret management

### Limitations

- Self-hosted Convex is designed as a single-node deployment
- Kubernetes adds complexity but provides orchestration benefits

## Coder Workspace Deployment

### Overview

Coder workspaces provide Kubernetes-managed development environments with port forwarding and DNS routing.

### Environment Characteristics

- **Platform**: Kubernetes-managed Coder workspace
- **OS**: Linux (Ubuntu/Debian-based), x86_64 architecture
- **Networking**: Internal cluster networking with port forwarding
- **Package Manager**: pnpm for Node.js

### Coder DNS Routing

**Critical**: Using `localhost` URLs causes CORS and authentication issues when accessed from external browsers.

Use Coder's automatic port-based DNS routing:
```
https://<slug>--<workspace>--<owner>.coder.hahomelabs.com
```

### Example URLs

| Service | Port | URL |
|---------|------|-----|
| Convex API | 3210 | `https://convex-api--workspace--owner.coder.hahomelabs.com` |
| Convex Dashboard | 6791 | `https://convex--workspace--owner.coder.hahomelabs.com` |
| Frontend App | 3000 | `https://app--workspace--owner.coder.hahomelabs.com` |

### PostgreSQL Configuration

**Issue**: Initial connection attempts failed with:
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

### Docker Compose for Coder

```yaml
# docker-compose.convex.yml
version: '3.8'

services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
    ports:
      - "3210:3210"
      - "3211:3211"
      - "6791:6791"
    environment:
      - CONVEX_CLOUD_ORIGIN=https://convex-api--workspace--owner.coder.hahomelabs.com
      - POSTGRES_URL=postgres://user:pass@host.coder-dev-envs:5432?sslmode=disable
      - INSTANCE_NAME=app
    volumes:
      - convex-data:/convex/data
    restart: unless-stopped

volumes:
  convex-data:
```

## VPS Deployment (Generic)

### Prerequisites

- Ubuntu/Debian server
- SSH access
- Domain name (optional)

### Setup Steps

```bash
# 1. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Install Docker Compose
sudo apt-get install docker-compose -y

# 4. Clone repository
git clone https://github.com/get-convex/convex-backend
cd convex-backend/self-hosted

# 5. Configure environment
cat > .env << EOF
CONVEX_CLOUD_ORIGIN=https://your-domain.com
CONVEX_SITE_ORIGIN=https://your-domain.com
POSTGRES_URL=postgres://user:pass@localhost:5432/dbname
EOF

# 6. Start services
sudo docker compose up -d

# 7. Generate admin key
sudo docker compose exec backend ./generate_admin_key.sh
```

### Reverse Proxy with nginx

```bash
# Install nginx
sudo apt-get install nginx -y

# Install certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot --nginx -d your-domain.com

# Configure nginx
sudo nano /etc/nginx/sites-available/convex
```

**nginx Configuration**:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3210;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

## Platform Comparison

| Platform | Difficulty | Scaling | Cost | Best For |
|----------|------------|---------|------|----------|
| **Fly.io** | Medium | Single-node | Medium | Managed simplicity |
| **Railway** | Low | Single-node | Medium | Quick start |
| **AWS EC2** | Medium | Vertical | Low-Medium | AWS integration |
| **Neon + VPS** | Low | Single-node | Low | Serverless Postgres |
| **Kubernetes** | High | Single-node* | High | Complex deployments |
| **Coder** | Low | Single-node | Internal | Development |

*Horizontal scaling requires code modifications

## Choosing a Platform

### Use Fly.io if you want:
- Managed deployment
- Automatic HTTPS
- Easy scaling (vertical)
- Simple configuration

### Use Railway if you want:
- One-click deployment
- Built-in Postgres
- GitHub integration
- Free tier option

### Use AWS if you want:
- Full infrastructure control
- AWS service integration
- Cost optimization at scale
- Existing AWS expertise

### Use Kubernetes if you want:
- Automated deployments
- Self-healing
- Resource management
- Existing K8s infrastructure

### Use Coder if you want:
- Development workspace
- Team collaboration
- Integrated development environment
- Remote development

## Migration Between Platforms

### Export from Source

```bash
# Export data from current deployment
npx convex export --filename backup-$(date +%Y%m%d).zip
```

### Import to Target

```bash
# Import data to new deployment
npx convex import --filename backup-20250115.zip
```

### Update Configuration

1. Update environment variables for new platform
2. Update DNS to point to new deployment
3. Deploy functions to new backend
4. Verify application functionality
5. Switch DNS when ready

## Resources

- [Official Self-Hosting Docs](https://docs.convex.dev/self-hosting)
- [GitHub Repository](https://github.com/get-convex/convex-backend)
- [Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)
- [#self-hosted Discord](https://www.convex.dev/discord)
