---
name: setup-graphql-operation
description: Create a new GraphQL operation file with proper role-based naming convention and scaffolding
argument-hint: [operation-name] [role]
updated: 2025-01-13
---

# /setup-graphql-operation

Create a new GraphQL operation file with proper role-based naming and scaffolding.

## Usage

```
/setup-graphql-operation [operation-name] [role]
```

**Arguments:**
- `operation-name` (required): Name of the GraphQL operation (camelCase)
- `role` (optional): Permission role (defaults to project's default role)

## Examples

```bash
# Create a user role query
/setup-graphql-operation getUserProfile user

# Create an admin role mutation
/setup-graphql-operation deleteAllUsers admin

# Create a public role query
/setup-graphql-operation getSiteConfig public
```

## What This Command Does

1. Prompts for operation type (query, mutation, subscription)
2. Creates file at `src/graphql/{operationName}.{role}.graphql`
3. Adds scaffolding based on operation type
4. Runs codegen to generate types and hooks

## Operation Templates

### Query Template

```graphql
# src/graphql/{operationName}.{role}.graphql
query {OperationName}($id: ID!) {
  item(id: $id) {
    id
    name
    createdAt
  }
}
```

### Mutation Template

```graphql
# src/graphql/{operationName}.{role}.graphql
mutation {OperationName}($input: InputType!) {
  createItem(input: $input) {
    id
    success
    errors
  }
}
```

### Subscription Template

```graphql
# src/graphql/{operationName}.{role}.graphql
subscription {OperationName}($id: ID!) {
  itemUpdated(id: $id) {
    id
    name
    updatedAt
  }
}
```

## After Scaffolding

1. Update the operation with your specific fields and variables
2. Run codegen: `pnpm codegen` (or your project's codegen command)
3. Import and use the generated hook in your component

## Related Skills

- `graphql-workflow` - Complete GraphQL development workflow
