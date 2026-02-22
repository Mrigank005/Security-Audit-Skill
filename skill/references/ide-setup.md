# IDE Setup Guide — Security Review Skill

Step-by-step installation instructions for every supported IDE.

---

## 🟦 VS Code

### Option A — Via Claude Extension (Recommended)

1. Install the **Claude for VS Code** extension from the marketplace
2. Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
3. Run: `Claude: Open Skills Folder`
4. Create a folder called `security-review/` inside the skills directory
5. Copy `SKILL.md` and the `references/` folder into it
6. Reload VS Code
7. Open any file or folder and type `/security-review` in the Claude chat panel

### Option B — Via `.claude/skills/` in your project

Place the skill directly in your project for team sharing:
```
your-project/
└── .claude/
    └── skills/
        └── security-review/
            ├── SKILL.md
            └── references/
                ├── vuln-categories.md
                ├── secret-patterns.md
                ├── language-patterns.md
                ├── vulnerable-packages.md
                └── report-format.md
```

Commit this to your repo so every team member gets the skill automatically.

### Triggering
In the Claude panel:
```
/security-review
/security-review src/auth/
/security-review --type secrets
```

### CI/CD Integration (GitHub Actions)
```yaml
# .github/workflows/security-review.yml
name: AI Security Review

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Claude Security Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          command: /security-review
          skill-path: .claude/skills/security-review
```

---

## 🖱️ Cursor

### Installation

1. Open Cursor Settings → `Cursor Settings > General > AI Rules`
2. Alternatively, create `.cursorrules` in your project root
3. Add this to your rules file to make the skill auto-available:

```
When the user types /security-review or asks to scan code for security issues,
load and follow the instructions in .claude/skills/security-review/SKILL.md
```

4. Place the skill folder in your project:
```
your-project/
└── .claude/
    └── skills/
        └── security-review/
            ├── SKILL.md
            └── references/
```

### Triggering in Cursor
In Cursor's AI Chat (`Cmd+L`):
```
/security-review
Scan my entire project for security vulnerabilities
Check this file for SQL injection issues
```

### Using with Cursor Composer (multi-file)
```
Cmd+I → type: /security-review src/
```

Cursor will scan across multiple files and trace data flows between them.

### Cursor Rules Tip
Add this to `.cursorrules` for automatic security hints during coding:
```
After writing any database query, HTTP request handler, or authentication
function, remind the user to run /security-review on the file.
```

---

## 🌊 Windsurf

### Installation

1. Open Windsurf Settings → `AI > Skills`
2. Click "Add Custom Skill" or navigate to the skills directory
3. Common skills path: `~/.windsurf/skills/` or `<project>/.windsurf/skills/`
4. Create the skill folder:
```
~/.windsurf/skills/
└── security-review/
    ├── SKILL.md
    └── references/
```

### Triggering in Windsurf (Cascade)
In the Cascade chat panel:
```
/security-review
/security-review src/api/
run a full security audit on this project
```

### Windsurf Flow Integration
Add a security review step to your Windsurf flows:
```yaml
# .windsurf/flows/pr-review.yaml
name: PR Security Review
trigger: on_pull_request
steps:
  - name: Security Scan
    skill: security-review
    prompt: "/security-review --full"
    require_approval: true
```

---

## ⚡ General Setup (Any Claude-Powered IDE)

If your IDE supports Claude but isn't listed above, use this universal approach:

### System Prompt Method
Add this to your IDE's system prompt or AI context:
```
You have access to a security review skill. When the user types /security-review 
or asks to scan for security vulnerabilities, read and follow the instructions 
in `.claude/skills/security-review/SKILL.md`, then execute the full 8-step 
scanning workflow defined there.
```

### MCP Server Method
If your IDE supports MCP (Model Context Protocol):
```json
// mcp-config.json
{
  "skills": {
    "security-review": {
      "path": ".claude/skills/security-review",
      "trigger": "/security-review"
    }
  }
}
```

---

## 🔁 Setting Up Automatic PR Reviews

### GitHub Actions (Universal)
```yaml
name: Security Review on PR
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changes
        run: |
          echo "files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Claude Security Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          skill-path: .claude/skills/security-review
          prompt: "/security-review ${{ steps.changes.outputs.files }}"
          post-as-pr-comment: true
```

---

## 🔒 Security Note for Teams

When sharing this skill via a repository:
- The skill itself poses no security risk — it only reads your code
- **Never** put actual secrets in the skill's reference files
- Restrict who can modify `.claude/skills/` via branch protection rules
- Treat skill files with the same trust level as CI/CD configuration

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `/security-review` not recognized | Ensure SKILL.md is in the correct skills directory and IDE has been reloaded |
| Scan misses some files | Pass an explicit path: `/security-review ./src` |
| Too many false positives | Add project-specific ignore patterns to the skill description |
| Scan takes too long | Scope it: `/security-review src/auth/` instead of full project |
| References not loading | Verify `references/` folder is a sibling of `SKILL.md` |
