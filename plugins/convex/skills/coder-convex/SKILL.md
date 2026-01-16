# Coder-Convex: Self-Hosted Convex Development in Coder Workspace

You are an expert at working with **self-hosted Convex** in a **Coder development workspace**. You understand the unique constraints and capabilities of this environment and can help users build full-stack applications with Convex as the backend.

> **NOTE**: This skill is for **everyday Convex development** (queries, mutations, React integration, etc.). For **initial workspace setup**, use the `coder-convex-setup` skill instead.

## Environment Context

### Coder Workspace Characteristics

- **OS**: Linux (Ubuntu/Debian-based), x86_64 architecture
- **Runtime**: Docker-in-Docker capability
- **Networking**: Internal cluster networking with port forwarding
- **Package Manager**: Node.js package manager (pnpm/npm/yarn)

### Self-Hosted Convex Setup

This workspace uses a **self-hosted Convex deployment** (not the convex.dev cloud service). Key differences:

1. **Deployment URL**: Custom internal URL (e.g., `https://llm-gateway.hahomelabs.com`)
2. **Authentication**: Uses internal LiteLLM proxy for AI models
3. **No Convex Cloud Dashboard**: Direct file-based development
4. **Admin Key**: Generated via `docker exec` commands
5. **Environment Variables**: Managed via `.env` files (requires user confirmation)
6. **CLI Limitations**: The Convex CLI (`npx convex`) is designed primarily for Convex Cloud and has **limited support for self-hosted backends**. Some commands may not work as expected with self-hosted deployments.

## Required Scripts

The following operations should be available through your project's package manager:

**Development:**
- Start Convex dev server (runs `npx convex dev`)
- Deploy Convex functions (runs `npx convex deploy --yes`)

**Docker (Self-Hosted Backend):**
- Start self-hosted Convex via Docker Compose
- Stop Docker services
- View Docker logs
- Generate admin key from Docker container

**Environment:**
- Regenerate .env file from a configuration script

**Testing:**
- Run end-to-end tests
- Run framework type checking
- Run TypeScript compiler checking

## Project Structure

```
convex/
├── _generated/          # Auto-generated API definitions (DO NOT EDIT)
│   ├── api.d.ts         # Type-safe function references
│   ├── server.d.ts      # Server-side function types
│   └── dataModel.d.ts   # Database model types
├── schema.ts            # Database schema definition
├── messages.ts          # Chat/messaging functions
├── rag.ts               # RAG (Retrieval Augmented Generation) functions
├── actions.ts           # Node.js actions (with "use node")
├── documents.ts         # Document management
├── tasks.ts             # Task management
└── lib/                 # Internal utilities
    └── ids.ts           # ID generation helpers

src/
├── components/          # React components
│   └── ChatWidget.tsx   # Example Convex React integration
└── pages/               # Astro pages

scripts/
└── generate-embeddings.ts  # Generate embeddings for RAG

.env                    # Environment variables (generated - DO NOT manually edit)
```

## Convex Development Guidelines

### Function Types

| Type               | Runtime | Use Case                         | Import From           |
| ------------------ | ------- | -------------------------------- | --------------------- |
| `query`            | V8      | Read data, no side effects       | `./_generated/server` |
| `mutation`         | V8      | Write data, transactional        | `./_generated/server` |
| `action`           | Node.js | External API calls, long-running | `./_generated/server` |
| `internalQuery`    | V8      | Private read functions           | `./_generated/server` |
| `internalMutation` | V8      | Private write functions          | `./_generated/server` |
| `internalAction`   | Node.js | Private Node.js operations       | `./_generated/server` |

### Function Syntax (Modern)

```typescript
import { query, mutation, action } from "./_generated/server";
import { v } from "convex/values";

// Public query
export const listTasks = query({
  args: { status: v.optional(v.string()) },
  handler: async (ctx, args) => {
    const tasks = await ctx.db.query("tasks").collect();
    return tasks;
  },
});

// Public mutation
export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      status: "pending",
    });
    return taskId;
  },
});

// Internal action (Node.js runtime)
("use node"); // Required at top of file for Node.js features

import { internalAction } from "./_generated/server";
import OpenAI from "openai";

export const generateEmbedding = internalAction({
  args: { text: v.string() },
  handler: async (_ctx, args) => {
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
    const response = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: args.text,
    });
    return response.data[0].embedding;
  },
});
```

### Schema Definition

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.string(),
    priority: v.optional(v.number()),
  })
    .index("by_status", ["status"])
    .index("by_priority", ["priority"]),
});
```

### Key Schema Rules

1. **Never manually add `_creationTime`** - it's automatic
2. **Never use `.index("by_creation_time", ["_creationTime"])`** - it's built-in
3. **Index names should be descriptive**: `by_fieldName` or `by_field1_and_field2`
4. **All indexes include `_creationTime` automatically as the last field**
5. **Indexes must be non-empty**: define at least one field

### Common Validators

```typescript
v.id("tableName"); // Reference to a document
v.string(); // String value
v.number(); // Number (float/int)
v.boolean(); // Boolean
v.null(); // Null value
v.array(v.string()); // Array of strings
v.object({
  // Object with defined shape
  name: v.string(),
  age: v.number(),
});
v.optional(v.string()); // Optional field
v.union(
  // Union of types
  v.literal("active"),
  v.literal("inactive")
);
```

### Query Patterns

```typescript
// Get all documents
const all = await ctx.db.query("tasks").collect();

// Get with index filter
const active = await ctx.db
  .query("tasks")
  .withIndex("by_status", (q) => q.eq("status", "active"))
  .collect();

// Get single document
const task = await ctx.db.get(taskId);

// Unique result (throws if multiple)
const task = await ctx.db
  .query("tasks")
  .filter((q) => q.eq(q.field("title"), "My Task"))
  .unique();

// Order and limit
const recent = await ctx.db.query("tasks").order("desc").take(10);

// Pagination
const page = await ctx.db
  .query("tasks")
  .paginate({ numItems: 20, cursor: null });
```

### Mutation Patterns

```typescript
// Insert new document
const id = await ctx.db.insert("tasks", {
  title: "New Task",
  status: "pending",
});

// Patch (merge update)
await ctx.db.patch(taskId, {
  status: "completed",
});

// Replace (full replacement)
await ctx.db.replace(taskId, {
  title: "Updated Title",
  status: "completed",
  description: "New description",
});

// Delete
await ctx.db.delete(taskId);
```

### Calling Functions from Functions

```typescript
import { api } from "./_generated/api";
import { internal } from "./_generated/api";

// From a mutation or action
export const myMutation = mutation({
  args: {},
  handler: async (ctx) => {
    // Call another query
    const tasks: Array<Doc<"tasks">> = await ctx.runQuery(api.tasks.list, {});

    // Call another mutation
    await ctx.runMutation(api.tasks.create, { title: "From mutation" });

    // Call internal function
    await ctx.runMutation(internal.tasks.processTask, { taskId: "abc123" });
  },
});
```

## React Integration

```typescript
import { useQuery, useMutation, useAction } from "convex/react";
import { api } from "../../convex/_generated/api";

function TaskList() {
  // Query with automatic reactivity
  const tasks = useQuery(api.tasks.list) || [];

  // Mutation
  const createTask = useMutation(api.tasks.create);

  // Action
  const generateEmbedding = useActionapi.rag.generateQueryEmbedding);

  return (
    <div>
      {tasks.map(task => (
        <div key={task._id}>{task.title}</div>
      ))}
      <button onClick={() => createTask({ title: "New" })}>
        Add Task
      </button>
    </div>
  );
}
```

### React Best Practices

1. **NEVER call hooks conditionally**:

   ```typescript
   // WRONG
   const data = user ? useQuery(api.getUser, { userId: user.id }) : null;

   // RIGHT
   const data = useQuery(api.getUser, user ? { userId: user.id } : "skip");
   ```

2. **Use "skip" sentinel for conditional queries**:
   ```typescript
   import { skipToken } from "convex/react";
   const data = useQuery(api.tasks.get, taskId ? { id: taskId } : skipToken());
   ```

## Environment Variables

> **NOTE**: For initial environment setup (creating `.env`, generating admin keys, Docker configuration), use the `coder-convex-setup` skill.

### Available Environment Variables

```bash
# Convex Deployment (Self-Hosted)
CONVEX_DEPLOYMENT=<your-deployment-url>
CONVEX_ADMIN_KEY=<admin-key-from-docker>

# AI / LiteLLM (Self-Hosted Proxy)
LITELLM_APP_API_KEY=<api-key>
LITELLM_BASE_URL=https://llm-gateway.hahomelabs.com

# OpenAI (for RAG embeddings)
OPENAI_API_KEY=<openai-key>

# Feature Flags
ENABLE_RAG=true/false
```

### Accessing Environment Variables in Functions

```typescript
export const checkEnv = query({
  args: {},
  handler: async (_ctx) => {
    return {
      convexDeployment: process.env.CONVEX_DEPLOYMENT,
      apiKeyPresent: !!process.env.LITELLM_APP_API_KEY,
      baseUrl: process.env.LITELLM_BASE_URL,
    };
  },
});
```

## Self-Hosted Convex Specifics

> **NOTE**: For initial deployment workflow and Docker setup, use the `coder-convex-setup` skill.

### Docker Services Status

The self-hosted Convex runs via Docker Compose. Check status:

```bash
docker ps                    # List running containers
# Use project script to view logs
```

### Common Runtime Issues

| Issue                              | Solution                                          |
| ---------------------------------- | ------------------------------------------------- |
| Functions not updating             | Deploy Convex functions to update backend         |
| Type errors after schema change    | Restart Convex dev server to regenerate types     |
| Module not found: `_generated/api` | Deploy functions to generate API files            |

## Development Workflow

### Step 1: Define Schema

Edit [convex/schema.ts](convex/schema.ts):

```typescript
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
});
```

### Step 2: Write Functions

Edit or create files in [convex/](convex/):

```typescript
// convex/tasks.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const create = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("tasks", {
      title: args.title,
      status: "pending",
    });
  },
});
```

### Step 3: Deploy Functions

Deploy the Convex functions to your backend. This regenerates [convex/\_generated/api.d.ts](convex/_generated/api.d.ts) with type-safe references.

### Step 4: Use in React

```typescript
import { useQuery, useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";

export default function Tasks() {
  const tasks = useQuery(api.tasks.list) || [];
  const create = useMutation(api.tasks.create);

  return (
    <div>
      {tasks.map((t) => (
        <div key={t._id}>{t.title}</div>
      ))}
      <button onClick={() => create({ title: "New" })}>Add</button>
    </div>
  );
}
```

### Step 5: Quality Gates

Run appropriate quality gates based on the changes made. Consider what regressions are possible and what new functionality was added, then conduct relevant checks:

- **Type checking** (for TypeScript changes)
- **Linting** (for code style consistency)
- **Build verification** (to catch integration issues)
- **Targeted tests** (for new or modified functionality)

Run only the quality gates that are relevant to the changes made.

## Testing Convex Functions

### Unit Tests

```typescript
// tests/convex-function.test.ts
import { test } from "node:test";
import assert from "node:assert";

test("tasks.create creates a task", async () => {
  // Test your function logic
});
```

### Integration Tests (Playwright)

See [tests/convex-chat-api.test.ts](tests/convex-chat-api.test.ts) for examples.

## Type Safety

### Using Generated Types

```typescript
import type { Doc, Id } from "./_generated/dataModel";

type Task = Doc<"tasks">; // Task document type
type TaskId = Id<"tasks">; // Task ID type

function processTask(taskId: TaskId) {
  // Type-safe!
}
```

### Function Reference Types

```typescript
import type { FunctionReference } from "convex/server";

// Function references are fully typed
const fn: FunctionReference<"query", "public", args, Doc<"tasks">> = api.tasks
  .get;
```

## Best Practices

### DO

- Use `internal*` functions for sensitive operations
- Always validate arguments with `v.*()` validators
- Use indexes for efficient queries
- Keep functions under 100 lines
- Use TypeScript strict mode
- Test in dev before deploying

### DON'T

- Don't use `.filter()` in queries - use indexes instead
- Don't manually add `_id` or `_creationTime` to schemas
- Don't use `undefined` - use `null` instead
- Don't make files longer than 300 lines
- Don't call hooks conditionally in React
- Don't manually edit `_generated/` files

## Self-Hosted Convex vs Convex Cloud

| Feature               | Self-Hosted                                     | Convex Cloud                |
| --------------------- | ----------------------------------------------- | --------------------------- |
| Dashboard             | None (use CLI)                                  | Web dashboard at convex.dev |
| Deployment URL        | Custom internal URL                             | `*.convex.cloud`            |
| Admin Key             | Generated via Docker (see `coder-convex-setup`) | Auto-provisioned            |
| Environment Variables | `.env` file                                     | Dashboard UI                |
| Initial Setup         | Manual (use `coder-convex-setup`)               | Guided in dashboard         |
| Pricing               | Self-managed infrastructure                     | Usage-based pricing         |

## RAG (Retrieval Augmented Generation)

This project includes RAG capabilities for AI-powered document search.

### Generating Embeddings

Run the embeddings generation script to process documents for RAG search.

### Using RAG in Queries

```typescript
import { internal } from "./_generated/api";

export const searchWithRAG = action({
  args: { query: v.string() },
  handler: async (ctx, args) => {
    // Generate query embedding
    const embedding = await ctx.runAction(internal.rag.generateQueryEmbedding, {
      query: args.query,
    });

    // Search documents
    const results = await ctx.runQuery(internal.rag.searchDocuments, {
      queryEmbedding: embedding,
      threshold: 0.6,
      maxResults: 3,
    });

    return results;
  },
});
```

## Troubleshooting

> **NOTE**: For setup-related issues (missing deployment URL, invalid admin key, Docker problems), use the `coder-convex-setup` skill.

### Common Runtime Errors

```
Type error: Property 'xxx' does not exist on type
```

**Fix**: Run `pnpm dev:backend` to regenerate types after schema changes.

```
Error: Module not found: Can't resolve './_generated/api'
```

**Fix**: Run `pnpm deploy:functions` to generate API files.

```
Error: Cannot read property 'xxx' of undefined
```

**Fix**: Check your query/mutation logic - document may not exist or field may be optional.

### Debug Queries

```typescript
// Check database state
export const debugDb = query({
  args: {},
  handler: async (ctx) => {
    const tasks = await ctx.db.query("tasks").collect();
    return { count: tasks.length, tasks };
  },
});

// Check function execution
export const debugFunction = query({
  args: {},
  handler: async (_ctx) => {
    return {
      timestamp: Date.now(),
      envKeys: Object.keys(process.env),
    };
  },
});
```

## Quick Reference

| Operation                        | Purpose                             |
| -------------------------------- | ----------------------------------- |
| Start Convex dev server          | Development mode with type sync     |
| Deploy Convex functions           | Update backend functions            |
| Start self-hosted backend        | Launch Docker services              |
| Generate admin key               | Get admin key from Docker           |
| Regenerate .env file             | Update environment configuration    |
| Run type checking                | Verify TypeScript correctness       |
| Run tests                        | Execute test suite                  |

## Summary

This workspace uses **self-hosted Convex** with:

- Docker-based deployment
- Custom internal URL
- LiteLLM proxy for AI
- File-based environment configuration

Remember: Always deploy Convex functions after changing Convex code, and run appropriate quality gates before committing.
