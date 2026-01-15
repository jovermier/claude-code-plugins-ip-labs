# Troubleshooting Guide

Common issues and solutions for self-hosted Convex deployments.

## Common Issues

### Environment Variable Issues

#### Issue: Database Connection Errors

**Error**:
```
cluster url already contains db name: /app
```

**Cause**: Using `DATABASE_URL` with database name included.

**Solution**:
- Use `POSTGRES_URL` instead of `DATABASE_URL`
- Remove database name from URL (Convex adds it based on `INSTANCE_NAME`)
- Use `sslmode=disable` for internal networking

**Example**:
```bash
# Wrong
DATABASE_URL=postgresql://user:pass@host:5432/convex_self_hosted

# Correct
POSTGRES_URL=postgres://user:pass@host:5432?sslmode=disable
INSTANCE_NAME=app  # Must match PostgreSQL database name
```

#### Issue: Multi-line Environment Variables

**Error**: PEM keys and other multi-line values fail when set via CLI.

**What Doesn't Work**:
```bash
cat /tmp/key.pem | npx convex env set PRIVATE_KEY -
```

**Solutions**:
1. Use dashboard UI to set environment variables
2. Base64-encode the value before storing
3. Use file-based secrets (Docker Secrets)

#### Issue: Environment Variables Not Applied

**Symptoms**: Changes not reflected in application.

**Solutions**:
1. Restart Docker containers
2. Run `npx convex dev` to regenerate .env.local
3. Verify variable is set: `npx convex env list`

### Authentication Issues

#### Issue: Missing JWKS

**Error**:
```
Missing environment variable `JWKS`
```

**Solution**: Generate and set JWKS from the public key. See [Authentication Guide](authentication.md).

#### Issue: PKCS#8 Format

**Error**:
```
Uncaught TypeError: "pkcs8" must be PKCS#8 formatted string
```

**Solution**:
1. Ensure key was generated with `openssl genpkey` (not `openssl genrsa`)
2. Verify key starts with `-----BEGIN PRIVATE KEY-----`
3. Use heredoc syntax when setting via CLI

#### Issue: Auth Provider Discovery Failed

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

#### Issue: Permanent Unauthenticated State

**Symptoms**: Convex React client enters permanent unauthenticated state after access token expiration.

**Status**: Known issue being tracked.

**Workaround**: Clear browser storage and re-authenticate.

### Docker Issues

#### Issue: Local Backend Database State

**Error**: Backend run fails with "persisted db metadata" error.

**Solution**:
```bash
rm convex_local_backend.sqlite3
```

Then restart the backend.

#### Issue: Container Won't Start

**Symptoms**: Docker container exits immediately.

**Debug**:
```bash
# Check logs
docker compose logs backend

# Check container status
docker compose ps

# Inspect container
docker compose exec backend env
```

**Common Causes**:
- Missing required environment variables
- Invalid configuration
- Port conflicts
- Volume permission issues

### Development Workflow Issues

#### Issue: Environment File Updates

**Problem**: Application doesn't pick up changes after switching environments.

**Solution**: Always run `npx convex dev` **before** testing client app when switching between local and cloud. This updates `.env.local` with correct URLs.

#### Issue: Functions Not Updating

**Symptoms**: Changes to Convex functions not reflected in application.

**Solution**: Deploy functions to update backend:
```bash
npx convex deploy
```

#### Issue: Type Errors After Schema Change

**Symptoms**: TypeScript errors after modifying schema.

**Solution**: Restart Convex dev server to regenerate types:
```bash
npx convex dev
```

### CLI Issues

#### Issue: Convex Auth Manual Setup

**Problem**: CLI doesn't support self-hosted deployments for Convex Auth.

**Solution**: Manual setup required. See [Authentication Guide](authentication.md).

#### Issue: Version Compatibility

**Error**: Deploy failures due to version mismatches between CLI and backend.

**Solution**: Ensure backend version matches CLI version. Pin versions in production.

### CORS Issues

#### Issue: CORS Errors in Browser

**Error**:
```
Access to fetch at 'https://your-convex-url.com' from origin 'https://your-app.com' has been blocked by CORS policy
```

**Solution**: Configure CORS in your Convex functions:

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { internal } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/",
  method: "GET",
  handler: async (_request) => {
    return new Response(null, {
      status: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  },
});

export default http;
```

### Performance Issues

#### Issue: Slow Query Performance

**Symptoms**: Queries take longer than expected.

**Debugging**:
```typescript
// Add timing to your query
export const debugQuery = query({
  args: {},
  handler: async (ctx) => {
    const start = Date.now();
    const result = await ctx.db.query("tasks").collect();
    console.log(`Query took ${Date.now() - start}ms`);
    return result;
  },
});
```

**Solutions**:
- Use indexes instead of `.filter()`
- Co-locate database with backend
- Use SSD storage
- Optimize PostgreSQL configuration

#### Issue: High Memory Usage

**Symptoms**: Container using more memory than expected.

**Solutions**:
- Monitor with `docker stats`
- Check for memory leaks in functions
- Increase container memory limits
- Optimize function logic

### Security Issues

#### Issue: Beacon Telemetry

**Problem**: Self-hosted instances send anonymous telemetry even when `DISABLE_BEACON` is set.

**Status**: Known bug, may require workaround or verify in logs.

**Workaround**: Check logs for beacon messages and verify environment variable is set correctly.

#### Issue: Exposed Ports

**Problem**: Dashboard or API ports exposed publicly.

**Solution**: Configure firewall rules and reverse proxy:

```bash
# Don't expose Convex ports directly
ufw deny 3210/tcp
ufw deny 3211/tcp
ufw deny 6791/tcp
```

Use nginx/Caddy as reverse proxy instead.

## Debug Commands

### Database State

```bash
# List database tables
just convex data

# Or use CLI
npx convex data
```

### Environment Variables

```bash
# List all environment variables
npx convex env list

# Check specific variable
npx convex env get VARIABLE_NAME
```

### Logs

```bash
# Stream all logs
npx convex logs

# Include successful function executions
npx convex logs --success

# Docker logs
docker compose logs -f backend

# Last 100 lines
docker compose logs --tail 100 backend
```

### Health Check

```bash
# Check if backend is running
curl http://localhost:3210/version

# With Docker
docker compose exec backend curl http://localhost:3210/version
```

### Function Testing

```typescript
// Add debug endpoints
export const debugDb = query({
  args: {},
  handler: async (ctx) => {
    const tasks = await ctx.db.query("tasks").collect();
    return { count: tasks.length, tasks };
  },
});

export const debugEnv = query({
  args: {},
  handler: async (_ctx) => {
    return {
      timestamp: Date.now(),
      envKeys: Object.keys(process.env),
    };
  },
});
```

## Platform-Specific Issues

### Coder Workspace

#### Issue: CORS and Authentication Issues

**Problem**: Using `localhost` URLs causes CORS and authentication issues when accessed from external browsers.

**Solution**: Use Coder's automatic port-based DNS routing:
```
https://<slug>--<workspace>--<owner>.coder.hahomelabs.com
```

#### Issue: PostgreSQL Connection

**Error**:
```
cluster url already contains db name: /app
```

**Solution**: Use `POSTGRES_URL` instead of `DATABASE_URL` and remove database name:
```bash
POSTGRES_URL=postgres://user:pass@host.coder-dev-envs:5432?sslmode=disable
INSTANCE_NAME=app
```

### Fly.io

#### Issue: Required Environment Variables

**Problem**: Deployment fails without proper origins.

**Solution**: Set required environment variables:
```toml
[env]
  CONVEX_CLOUD_ORIGIN = "https://your-app.fly.dev"
  CONVEX_SITE_ORIGIN = "https://your-app.fly.dev"
```

### Railway

#### Issue: Postgres Integration

**Problem**: Connection string format issues.

**Solution**:
```bash
# Add Railway Postgres
railway add postgres

# Set POSTGRES_URL
railway variables set POSTGRES_URL=$POSTGRES_URL
```

## Getting Help

### Community Resources

- **#self-hosted Discord** - Community support, real-time help
- **GitHub Issues** - Bug reports and questions
- **GitHub Discussions** - General discussions
- **Stack Overflow** - Tag: `convex-dev`

### What to Include When Asking for Help

1. **Convex version**:
   ```bash
   npx convex --version
   docker compose exec backend ./run_backend.sh --version
   ```

2. **Environment**:
   ```bash
   npx convex env list
   ```

3. **Logs**:
   ```bash
   docker compose logs backend --tail 100
   npx convex logs --success
   ```

4. **Configuration**:
   - Docker Compose file (sanitized)
   - Environment variables (sanitized)

5. **Steps to reproduce**:
   - What you were trying to do
   - What you expected to happen
   - What actually happened

## Prevention

### Best Practices

1. **Version Pinning**: Never use `latest` tag in production
2. **Backup Before Changes**: Always backup before major changes
3. **Test in Staging**: Test migrations and upgrades in staging first
4. **Monitor Logs**: Regularly check logs for issues
5. **Document Issues**: Document issues and solutions for future reference

### Health Monitoring

Set up automated health checks:

```yaml
# docker-compose.yml
services:
  convex-backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3210/version"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Automated Backups

Set up regular backups to prevent data loss:

```bash
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/convex-backup.sh >> /var/log/convex-backup.log 2>&1
```

## Additional Resources

- [Deployment Guide](deployment.md) - Deployment methods and configuration
- [Authentication Guide](authentication.md) - Auth setup and troubleshooting
- [Environment Variables](environment.md) - Complete environment reference
- [Production Configuration](production.md) - Security, monitoring, backups
