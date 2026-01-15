# Authentication Guide

Complete guide for configuring @convex-dev/auth with self-hosted Convex.

## Overview

@convex-dev/auth provides:
- Multiple authentication providers (Anonymous, Email/Password, OAuth)
- JWT-based session management
- User and session management
- Token generation and validation

> **Important**: The CLI does not support self-hosted deployments for Convex Auth. Manual setup is required.

## Required Environment Variables

### 1. JWT_PRIVATE_KEY

**Purpose**: RSA private key for signing JWT tokens.

**Format**: Must be **PKCS#8** format (NOT PKCS#1/RSAPrivateKey).

> **PKCS#8** is a generic, standardized format with algorithm identification (uses `BEGIN PRIVATE KEY`), while **PKCS#1** is RSA-specific format (uses `BEGIN RSA PRIVATE KEY`). PKCS#8 is more portable and recommended.

### How to Generate

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem
```

### Verification

The file should start with:
```
-----BEGIN PRIVATE KEY-----
```

NOT:
```
-----BEGIN RSA PRIVATE KEY-----
```

### Setting in Convex

**Using heredoc (to preserve multiline format)**:
```bash
npx convex env set JWT_PRIVATE_KEY << 'PEMEOF'
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCHbqvhQBKUY4pw
...
-----END PRIVATE KEY-----
PEMEOF
```

**Known Issue**: The `convex env set` command fails when trying to set environment variables with multi-line values, such as PEM-formatted private keys.

### Alternative Workaround - Base64 Encoding

```bash
# Base64 encode the key first
base64 jwt_private_key.pem > jwt_private_key.b64

# Set the base64 version
npx convex env set JWT_PRIVATE_KEY_BASE64 "$(cat jwt_private_key.b64)"

# Decode in your application code
```

> Base64 encoding is a common approach for handling multi-line certificates and private keys as single-line environment variables across various platforms.

### Docker Configuration for Base64-Encoded Keys

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

## 2. JWKS (JSON Web Key Set)

**Purpose**: Public key set for verifying JWT signatures. Contains the public key corresponding to JWT_PRIVATE_KEY.

### Required Format

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

### How to Generate

**1. Extract public key from private key**:
```bash
openssl pkey -in jwt_private_key.pem -pubout -out jwt_public.pem
```

**2. Convert to JWK format using Node.js**:
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

### Setting in Convex

```bash
npx convex env set JWKS '{"keys":[{"kty":"RSA",...}]}'
```

## 3. JWT_ISSUER

**Purpose**: The issuer URL for JWT tokens. Must match your Convex deployment URL or be configured based on your auth provider.

### For Self-Hosted Convex with Custom Auth

```bash
# Use your Convex API URL from Coder DNS routing
JWT_ISSUER=https://convex-api--<workspace>--<owner>.coder.<domain>
```

> **Note**: Replace `<workspace>`, `<owner>`, and `<domain>` with your specific Coder environment values.

### For Clerk Integration

- Use `CLERK_JWT_ISSUER_DOMAIN` instead
- Set to your Clerk Frontend API URL (found in Clerk Dashboard → API Keys)
- Format: `https://your-app.clerk.accounts.dev`

> For Clerk integration, the Frontend API URL from the Clerk Dashboard is the issuer domain for Clerk's JWT templates.

### For Other Auth Providers

- **Auth0**: Your Auth0 domain URL (e.g., `https://your-domain.auth0.com`)
- Found in your `.well-known/openid-configuration` endpoint

### Setting in Convex

```bash
npx convex env set JWT_ISSUER "https://your-convex-url.com"
```

## Session Management and Token Security

### Token Expiration and Refresh

Convex Auth uses JWT tokens with the following security characteristics:

> **Refresh Token Security**: Refresh tokens can only be used once to get new access tokens. Using an "old" refresh token will invalidate the entire session. This is a key security feature to prevent token replay attacks.

### Session Lifecycle

- Session documents exist until the session expires or user signs out
- One user can have many active sessions simultaneously
- Access tokens have short expiration times requiring refresh

### JWT-based Authentication

- Convex uses OpenID Connect (based on OAuth) ID tokens in JWT form
- JWTs authenticate WebSocket connections
- Compatible with most authentication providers

## Common Session Issues

### Permanent Unauthenticated State

Some users report the Convex React client entering a permanent unauthenticated state after access token expiration, even when AuthKit refreshes tokens properly. This is a known issue being tracked.

### Session Persistence After Page Refresh

Google OAuth sessions may not persist after browser refresh, showing "Invalid" errors in Convex logs.

## Key Rotation Strategy

> **Best Practice**: Rotate admin keys and JWT keys regularly (quarterly recommended). Use different keys for dev/staging/production.

### Key Rotation Process

1. Generate new key pair
2. Add new public key to JWKS (with new `kid`)
3. Deploy new keys to Convex
4. Verify tokens are issued with new key
5. Monitor for any issues
6. Remove old key from JWKS after verification period

## Security Considerations

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

## Troubleshooting Auth Issues

### Common Error: Missing JWKS

**Error**:
```
Missing environment variable `JWKS`
```

**Solution**: Generate and set JWKS from the public key (see above).

### Common Error: PKCS#8 Format

**Error**:
```
Uncaught TypeError: "pkcs8" must be PKCS#8 formatted string
```

**Solution**:
1. Ensure key was generated with `openssl genpkey` (not `openssl genrsa`)
2. Verify key starts with `-----BEGIN PRIVATE KEY-----`
3. Use heredoc syntax when setting via CLI

### Common Error: Auth Provider Discovery Failed

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

## Complete Auth Setup Script

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

## Auth Provider Integration

### Clerk

```typescript
// convex/auth.config.ts
import { convexAuth } from "@convex-dev/auth/clerk";

export const { auth, signIn, signOut, store } = convexAuth({
  provider: clerk,
});
```

**Environment Variables**:
```bash
CLERK_JWT_ISSUER_DOMAIN=https://your-app.clerk.accounts.dev
CLERK_SECRET_KEY=sk_test_...
```

### Auth0

```typescript
// convex/auth.config.ts
import { convexAuth } from "@convex-dev/auth/auth0";

export const { auth, signIn, signOut, store } = convexAuth({
  provider: auth0,
});
```

**Environment Variables**:
```bash
AUTH0_SECRET=your-client-secret
AUTH0_ISSUER_BASE_URL=https://your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
```

### Anonymous Provider

```typescript
// convex/auth.config.ts
import { convexAuth } from "@convex-dev/auth";

export const { auth, signIn, signOut, store } = convexAuth({
  providers: [anonymous],
});
```

## Resources

- [Convex Auth Manual Setup](https://labs.convex.dev/auth/setup/manual)
- [Convex Auth Security Guide](https://labs.convex.dev/auth/security)
- [Convex Auth Authorization Guide](https://labs.convex.dev/auth/authz)
- [Convex & Clerk Documentation](https://docs.convex.dev/auth/clerk)
- [GitHub Issue #98: JWT_PRIVATE_KEY not in environment](https://github.com/get-convex/convex-backend/issues/98)
- [GitHub Issue #128: Multi-line environment variables](https://github.com/get-convex/convex-backend/issues/128)
