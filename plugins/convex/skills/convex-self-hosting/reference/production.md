# Production Configuration

Comprehensive guide for production deployment of self-hosted Convex.

## Security and Hardening

### Authentication Best Practices

#### Admin Key Management

Generate a secure admin key:

```bash
docker compose exec backend ./generate_admin_key.sh
```

**Best Practices**:
- Never commit admin keys to version control
- Rotate admin keys regularly (quarterly recommended)
- Use different keys for dev/staging/production
- Store in secret management systems (Vault, AWS Secrets Manager, Docker Secrets)

#### Instance Secret

When building from source, always generate a unique instance secret:

```bash
openssl rand -hex 32
```

**Critical**: Never use default instance secrets from repository.

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

### Alerting

#### Recommended Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| **High CPU** | > 80% for 5 minutes | Warning |
| **High Memory** | > 90% for 5 minutes | Critical |
| **Database Down** | Connection failed | Critical |
| **High Error Rate** | > 5% error rate | Warning |
| **Disk Space Low** | < 20% free | Warning |

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

#### PostgreSQL Backup Strategies

##### pg_dump (Logical Backup)

```bash
# Full database backup
pg_dump -U username -h localhost -d convex_self_hosted -F c -f backup.dump

# Restore from backup
pg_restore -U username -h localhost -d convex_self_hosted --clean backup.dump
```

##### Continuous Archiving (WAL)

Configure for point-in-time recovery:

```sql
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /wal_archive/%f'
max_wal_senders = 3
wal_keep_size = '1GB'
```

##### Replication Setup

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

**Critical Limitation**: Self-hosted Convex is **single-node by default**.

To scale horizontally:
1. Modify the Rust codebase to separate services
2. Implement load balancing
3. Ensure all instances access the same database
4. Handle WebSocket session affinity

> **"If you want to scale it, you'll need to modify the open-source backend code to scale the various services for your own infrastructure."**

**Required for Horizontal Scaling**:
- Separate API, function execution, and WebSocket services
- Shared storage (PostgreSQL + S3)
- Load balancer with sticky sessions
- Stateless function design

### Resource Sizing Guide

| Scale | CPU | RAM | Database | Storage |
|-------|-----|-----|----------|---------|
| **Development** | 1 vCPU | 2 GB | SQLite | 10 GB |
| **Small Production** | 2 vCPUs | 4 GB | Postgres 2 GB | 50 GB SSD |
| **Medium Production** | 4 vCPUs | 8 GB | Postgres 8 GB | 200 GB SSD |
| **Large Production** | 8+ vCPUs | 16+ GB | Postgres 32 GB + Replica | 500+ GB SSD |

## Operational Responsibilities

### What You're Responsible For

| Responsibility | Convex Cloud | Self-Hosted |
|----------------|--------------|-------------|
| **Scaling** | Managed | Your responsibility |
| **Migrations** | Automatic | Manual |
| **Backups** | Automatic | Manual |
| **Monitoring** | Included | Your setup |
| **Security Updates** | Automatic | Manual |
| **Support** | Available | Community only |

### Migration Management

When upgrading between versions:
1. **Identify required SQL migrations** for each version
2. **Run migrations in sequence** from current to target
3. **OR export from old, import to new**

**Gotcha**: Never use `latest` tag in production. Always pin to specific versions.

### Failure Recovery

You must implement:
- Database replication
- Regular snapshots/backups
- Disaster recovery procedures
- Monitoring and alerting
- Automatic restart mechanisms
