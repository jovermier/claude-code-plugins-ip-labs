# Changelog

All notable changes to the Coder plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-15

### Added
- **coder-workspace-management skill** - Comprehensive Coder CLI command reference with:
  - Workspace lifecycle commands (create, start, stop, restart, update, delete)
  - Workspace filtering and querying (owner, status, template, outdated, dormant filters)
  - Template management (init, list, show, push, update)
  - SSH access and port forwarding commands
  - State management for troubleshooting
  - Workspace scheduling for automated start/stop
  - Authentication commands (login, logout, whoami)
  - Token management and dotfiles configuration
  - Network debugging (netcheck, ping, speedtest)
  - Server operations and configuration
  - Best practices and troubleshooting guides
  - Integration examples with CI/CD workflows
  - Official Coder documentation links

### Changed
- Plugin version bumped to 1.2.0
- Updated plugin.json description to reflect two-skill architecture
- **Removed** `coder-environment` skill - its content is now included in `coder-hahomelabs`
- Added keywords: cli, workspace-management, templates, terraform, ssh, port-forwarding, scheduling, troubleshooting

## [1.1.0] - 2026-01-15

### Added
- **coder-hahomelabs skill** - hahomelabs.com-specific workspace configuration with:
  - Service URL patterns (`https://<service>--<workspace>--<user>.coder.hahomelabs.com`)
  - **PostgreSQL (CloudNativePG)** - Database configuration, environment variables, cloning support, backup buckets
  - **S3 Storage (Ceph)** - Storage configuration at `s3.us-central-1.hahomelabs.com`
  - **Convex Backend** - Dashboard, API, and proxy URLs with internal PostgreSQL/S3 integration
  - **Nhost Backend** - Dashboard, Hasura, MailHog, auth, functions, storage, GraphQL URLs
  - **LLM Gateway** - LiteLLM proxy at `llm-gateway.hahomelabs.com` with model mapping (Haiku/Sonnet/Opus)
  - **GitHub CLI** - Auto-authenticated OAuth token refresh documentation
  - **Workspace Cloning** - PostgreSQL and S3 cloning limitations and restrictions
  - **Gotchas section** - 7 common pitfalls and important notes
- **Two-skill architecture** - `coder-environment` (general context) and `coder-hahomelabs` (domain-specific configuration)

### Changed
- Plugin version bumped to 1.1.0
- Updated plugin.json description to reflect two-skill architecture
- `coder-environment` skill refactored as portable, deployment-agnostic context (PM2, Docker, general service URL patterns, environment variables, optional features)
- `coder-hahomelabs` skill contains all hahomelabs.com-specific configuration (PostgreSQL details, S3 endpoints, Convex/Nhost URLs, LLM gateway, workspace cloning, gotchas)
- Added keywords: postgresql, cloudnativepg, s3, ceph, convex, nhost, hasura, litellm, pm2, service-urls, coder-hahomelabs, hahomelabs, workspace-configuration

## [1.0.0] - 2026-01-12

### Added
- Initial Coder plugin release
- Coder workspace environment skills (`coder-environment`)
- Docker-in-Docker capabilities
- Kubernetes context awareness
