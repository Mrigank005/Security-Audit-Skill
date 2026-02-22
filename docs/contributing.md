# Contributing to Security Review Skill

Thank you for contributing! This guide covers how to add new patterns, languages,
CVEs, IDE support, test fixtures, and more.

---

## Table of Contents

- [Adding a New Vulnerability Pattern](#adding-a-new-vulnerability-pattern)
- [Adding a New Language](#adding-a-new-language)
- [Adding a New CVE](#adding-a-new-cve)
- [Adding Support for a New IDE](#adding-support-for-a-new-ide)
- [Creating a New Test Fixture](#creating-a-new-test-fixture)
- [Running the Skill Against Fixtures](#running-the-skill-against-fixtures)
- [Markdown Style Guide](#markdown-style-guide)
- [Commit Message Conventions](#commit-message-conventions)

---

## Adding a New Vulnerability Pattern

File: `skill/references/vuln-categories.md`

1. Identify the correct category section (Injection, Auth, Crypto, etc.)
2. Add a new subsection using this format:

```markdown
### Vulnerability Name
**What to look for:**
- Bullet points describing the dangerous pattern

**Detection signals (all languages):**
\`\`\`
code pattern showing what's vulnerable
\`\`\`

**Safe patterns:**
\`\`\`
code pattern showing the correct way
\`\`\`

**Escalation checkers:**
- How this vuln can be chained or escalated
```

3. If the pattern is language-specific, also add it to `language-patterns.md`
4. Create or update a test fixture to include the new pattern
5. Run the skill against the fixture to verify detection

---

## Adding a New Language

File: `skill/references/language-patterns.md`

1. Add a new `## Language Name (Framework1, Framework2)` section
2. Include the following subsections:
   - **Critical imports to flag** — dangerous functions in this language
   - **Framework-specific patterns** — patterns unique to popular frameworks
   - **Safe alternatives** — the correct way to write each pattern
3. Follow the existing format used for JavaScript, Python, Java, PHP, Go, Ruby, and Rust
4. Update the supported languages list in:
   - `README.md` (the "What It Scans" table)
   - `docs/faq.md` (the "What languages does this skill support?" answer)
   - `CHANGELOG.md` (under the next release)

### Example entry:

```markdown
## Swift (iOS, Server-Side Swift)

### Critical imports to flag
\`\`\`swift
Process()                     // command execution
NSTask                        // legacy command execution
FileManager.default           // file system access — check for path traversal
\`\`\`

### Vapor specific
\`\`\`swift
// Missing authentication middleware
app.get("admin", "users") { req -> [User] in
    // Should have: .grouped(AuthMiddleware())
    return try await User.query(on: req.db).all()
}
\`\`\`
```

---

## Adding a New CVE

File: `skill/references/vulnerable-packages.md`

1. Find the correct ecosystem section (npm, pip, Maven, Gems, Cargo, Go)
2. Add a new row to the table:

```markdown
| package-name | < safe_version | Brief description (CVE-YYYY-NNNNN) | >= safe_version |
```

3. Include:
   - The exact vulnerable version range
   - The CVE identifier (if available)
   - A one-line description of the vulnerability
   - The minimum safe version

4. For new ecosystems, create a new section following the existing table format

### Where to find CVEs:
- [NVD (NIST)](https://nvd.nist.gov/)
- [GitHub Advisory Database](https://github.com/advisories)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [RustSec Advisory Database](https://rustsec.org/advisories/)
- [Snyk Vulnerability DB](https://security.snyk.io/)

---

## Adding Support for a New IDE

File: `skill/references/ide-setup.md`

1. Add a new `## IDE Name` section
2. Include these subsections:
   - **Installation** — where to place the skill files
   - **Triggering** — how users invoke `/security-review`
   - **IDE-specific tips** — any special configuration needed

3. Follow the format used for VS Code, Cursor, and Windsurf sections

### Template:

```markdown
## 🔷 IDE Name

### Installation

1. Open IDE Settings → ...
2. Navigate to the skills/plugins directory: `~/.ide-name/skills/`
3. Create the skill folder:
\`\`\`
~/.ide-name/skills/
└── security-review/
    ├── SKILL.md
    └── references/
\`\`\`

### Triggering
In the AI chat panel:
\`\`\`
/security-review
/security-review src/
\`\`\`

### IDE-Specific Tips
- Tip 1
- Tip 2
```

---

## Creating a New Test Fixture

Directory: `tests/fixtures/`

1. Create a new folder: `tests/fixtures/vulnerable-<language>-app/`
2. Build a minimal, runnable application with **deliberate** vulnerabilities
3. Mark every vulnerable line with a comment:
   ```
   // VULN: <vulnerability type>
   ```
4. Include a `README.md` that says: "This app is intentionally vulnerable. For testing only."
5. Include realistic dependency files (`package.json`, `requirements.txt`, etc.)
   with deliberately vulnerable version pins
6. Cover at least these categories:
   - One injection flaw (SQLi, XSS, or command injection)
   - One auth/access control issue (IDOR, missing auth, JWT weakness)
   - One hardcoded secret
   - One vulnerable dependency

### Fixture structure example:

```
tests/fixtures/vulnerable-<lang>-app/
├── README.md
├── <dependency-file>
├── src/
│   ├── <main-file>
│   └── <routes-or-handlers>
└── config/
    └── <config-file>
```

7. After creating the fixture, run the skill against it and save results:
   - Report → `examples/example-report-<lang>.md`
   - Expected findings → `tests/expected-outputs/<lang>-findings.md`

---

## Running the Skill Against Fixtures

To verify your changes work correctly:

1. Open the fixture directory in your IDE (VS Code, Cursor, or Windsurf)
2. Run `/security-review tests/fixtures/vulnerable-<lang>-app/`
3. Compare the scan output against `tests/expected-outputs/<lang>-findings.md`
4. Verify:
   - All expected findings are detected (no false negatives)
   - No new false positives introduced
   - Severity and confidence ratings are reasonable
   - Patches are correct and applicable

If you modified a reference file, re-run the skill on **all** fixtures to check
for regressions.

---

## Markdown Style Guide

All `.md` files in this repo should follow these conventions:

### Formatting rules:
- Use `#` headings — one `#` per file, `##` for sections, `###` for subsections
- Use fenced code blocks with language identifiers (` ```js `, ` ```python `, etc.)
- Use `|` tables for structured data (align with spaces for readability)
- Use `---` horizontal rules to separate major sections
- Wrap lines at ~100 characters for readability (not enforced strictly)
- Use blank lines between all block elements (headings, code blocks, lists, tables)

### Content rules:
- Be specific — include file paths, line numbers, and code examples
- Use present tense ("The skill detects..." not "The skill will detect...")
- Keep explanations concise but complete
- Use consistent terminology (see `SKILL.md` for canonical terms)
- Do NOT include real secrets, credentials, or sensitive data — even in examples

### File naming:
- Use lowercase with hyphens: `vuln-categories.md`, not `VulnCategories.md`
- Fixture directories: `vulnerable-<language>-app`
- Expected outputs: `<language>-findings.md`

---

## Commit Message Conventions

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

<optional body>

<optional footer>
```

### Types:
| Type | Use for |
|------|---------|
| `feat` | New vulnerability pattern, new language, new feature |
| `fix` | Correcting a false positive/negative, fixing a bug |
| `docs` | Documentation changes |
| `test` | Adding or updating test fixtures |
| `chore` | Repo maintenance, CI/CD changes |
| `refactor` | Restructuring reference files without changing behavior |

### Scopes:
- `vuln` — changes to `vuln-categories.md`
- `lang` — changes to `language-patterns.md`
- `deps` — changes to `vulnerable-packages.md`
- `secrets` — changes to `secret-patterns.md`
- `ide` — changes to `ide-setup.md`
- `report` — changes to `report-format.md`
- `fixtures` — changes to test fixtures

### Examples:
```
feat(vuln): add detection for GraphQL injection patterns
fix(lang): reduce false positives in React dangerouslySetInnerHTML checks
docs: update FAQ with Windsurf-specific instructions
test(fixtures): add vulnerable Go application fixture
chore(deps): add CVE-2024-1234 to npm watchlist
```
