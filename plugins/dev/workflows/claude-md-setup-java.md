# CLAUDE.md Setup Workflow - Java

Generates `CLAUDE.md` for Java projects (Maven, Gradle, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `pom.xml` or `build.gradle` is detected
- For any Java project using Maven or Gradle
- For Spring Boot, Jakarta EE, or other Java frameworks

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Detect build system
cat pom.xml 2>/dev/null || cat build.gradle 2>/dev/null || cat build.gradle.kts

# Check for lockfiles
ls -la | grep -E "(gradle\.lockfile|maven\.lock)"

# Detect framework
ls -la | grep -E "(spring-boot|jakarta|javax)"

# Check for testing setup
ls -la src/test/ 2>/dev/null

# Check for common Java configs
ls -la | grep -E "(settings\.gradle|mvnw|gradlew)"
```

**Extract Technologies:**

- From `pom.xml`: All dependencies in `<dependencies>` section
- From `build.gradle` / `build.gradle.kts`: All `implementation` and `testImplementation` dependencies
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerJava() {
  const files = listFiles('.');

  if (files.includes('pom.xml')) return 'maven';
  if (files.includes('build.gradle') || files.includes('build.gradle.kts')) return 'gradle';
  return null;
}
```

**Version Detection (Skill-Linked):**

```javascript
function extractJavaVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "spring-boot-starter-web"
        displayVersion: tech.version,  // Keep version as-is
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

### Step 4: Match Technologies to Plugins

Match detected dependencies to marketplace plugins using keywords and descriptions.

**Always Include These Plugins:**

- **`dev`** - Core workflows, agents, todos (always relevant)
- **`coder`** - If running in a Coder workspace

### Step 5: Resolve Template Variables

```javascript
function resolveVariables(variables, project) {
  const resolved = {};
  for (const variable of variables) {
    const key = variable.replace(/[\[\]]/g, '').toLowerCase();
    resolved[key] = resolveVariable(key, project);
  }
  return resolved;
}

function resolveVariable(variableName, project) {
  const pm = project.packageManager; // 'maven' or 'gradle'

  const resolvers = {
    'package-manager': () => pm,
    'install-command': () => pm === 'gradle' ? './gradlew build' : 'mvn install',
    'test-command': () => pm === 'gradle' ? './gradlew test' : 'mvn test',
    'dev-command': () => detectJavaDevCommand(project, pm),
    'build-command': () => pm === 'gradle' ? './gradlew build' : 'mvn package',
    'lint-command': () => pm === 'gradle' ? './gradlew checkstyleMain' : 'mvn checkstyle:check',
    'clean-command': () => pm === 'gradle' ? './gradlew clean' : 'mvn clean',
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function detectJavaDevCommand(project, pm) {
  // Check for Spring Boot
  if (project.hasSpringBoot()) {
    return pm === 'gradle' ? './gradlew bootRun' : 'mvn spring-boot:run';
  }

  // Generic Java application
  return 'java -jar target/*.jar'; // Maven default path
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from pom.xml or build.gradle]

[Project description]

## Tech Stack
[Detected technologies by category with versions]

## Package Manager
[detected-package-manager] - All commands use this build tool.

## Resolved Variables
[Template variables resolved to project-specific values]

## Critical Rules
[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Marketplace Plugins
[Table of matched plugins]

### Available Skills
[Skills with descriptions from frontmatter]

## Workflows
[Core dev workflows + any from matched plugins]

## Commands
[All relevant commands]

## Quality Gates
[Detected validation commands]

## Development Notes
[User-preserved content]
```

## Example Output

### Spring Boot with Gradle

```markdown
# My Spring Boot App

Spring Boot web application using Gradle.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Java** | 17 | `java-lang` | Language version |
| **Spring Boot** | 3.2 | `java-spring-boot` | Application framework |
| **JUnit** | 5.10 | `java-junit` | Testing framework |

## Package Manager

**gradle** (detected from build.gradle)

## Resolved Variables

| Variable | Value |
|----------|-------|
| `package-manager` | `gradle` |
| `install-command` | `./gradlew build` |
| `test-command` | `./gradlew test` |
| `dev-command` | `./gradlew bootRun` |
| `build-command` | `./gradlew build` |
| `clean-command` | `./gradlew clean` |

## Commands

```bash
./gradlew build         # Build project (downloads dependencies)
./gradlew bootRun       # Run Spring Boot application
./gradlew test          # Run tests
./gradlew clean         # Clean build artifacts
./gradlew checkstyleMain  # Lint code
```
```

### Maven Project

```markdown
# My Java App

Java application using Maven.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Java** | 21 | `java-lang` | Language version |
| **JUnit** | 5.10 | `java-junit` | Testing framework |

## Package Manager

**maven** (detected from pom.xml)

## Commands

```bash
mvn install           # Build and install to local repo
mvn test              # Run tests
mvn package           # Package application
mvn clean             # Clean build artifacts
mvn spring-boot:run   # Run Spring Boot (if applicable)
```
```
