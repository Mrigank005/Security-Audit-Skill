# 🔐 Security Review Agent Skill

An open-source AI-native security scanner for agentic IDEs — inspired by Claude Code Security.
Drop it into any project and run `/security-review` to get a full vulnerability report
with patch proposals.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/contributing.md)

---

## Quick Start

1. Copy the `skill/` folder into your project's Claude skills directory:
   ```
   your-project/
   └── .claude/
       └── skills/
           └── security-review/
               ├── SKILL.md
               └── references/
   ```

2. In your IDE's Claude chat, type:
   ```
   /security-review
   ```

3. Review the findings and apply patches as needed.

> See [skill/references/ide-setup.md](skill/references/ide-setup.md) for detailed
> setup instructions for VS Code, Cursor, Windsurf, and other IDEs.

---

## What It Scans

| Category | Examples |
|----------|---------|
| 🔴 Injection Flaws | SQL injection, XSS, command injection, SSRF |
| 🟠 Auth & Access | IDOR, JWT bugs, broken auth, CSRF, privilege escalation |
| 🟡 Secrets | API keys, passwords, tokens, cloud credentials |
| 🔵 Dependencies | CVEs in npm, pip, Maven, Rubygems packages |
| ⚪ Cryptography | Weak hashing, bad randomness, insecure TLS |
| ⚙️ Business Logic | Race conditions, missing rate limits, integer overflow |

## Supported Languages

JavaScript/TypeScript · Python · Java · PHP · Go · Ruby · Rust

## Supported IDEs

- ✅ VS Code
- ✅ Cursor
- ✅ Windsurf
- ✅ Any Claude-powered IDE

---

## Commands

```bash
/security-review                  # Full project scan
/security-review src/auth/        # Scan specific directory
/security-review --type secrets   # Secrets only
/security-review --type deps      # Dependency audit only
```

---

## How It Works

The skill follows an 8-step workflow:

1. **Scope Resolution** — Detect languages & frameworks
2. **Dependency Audit** — Check for CVEs in packages
3. **Secrets Scan** — Find exposed credentials & API keys
4. **Vulnerability Deep Scan** — Reason across your codebase
5. **Cross-File Analysis** — Trace data flows between files
6. **Self-Verification** — Filter false positives
7. **Report Generation** — Structured findings by severity
8. **Patch Proposals** — Concrete fixes for every CRITICAL/HIGH issue

> ⚠️ Nothing is auto-applied. Every patch requires your approval.

For a detailed breakdown of each step, see [docs/how-it-works.md](docs/how-it-works.md).

---

## Repository Structure

```
├── skill/                            ← The skill itself (copy this into your project)
│   ├── SKILL.md                      ← Main skill definition
│   └── references/
│       ├── vuln-categories.md        ← Deep dive: every vulnerability type
│       ├── secret-patterns.md        ← Regex + entropy patterns for secrets
│       ├── language-patterns.md      ← JS, Python, Java, PHP, Go, Ruby, Rust
│       ├── vulnerable-packages.md    ← CVE watchlist for npm/pip/Maven/Gems
│       ├── report-format.md          ← Output template
│       └── ide-setup.md             ← Setup for VS Code, Cursor, Windsurf
├── docs/                             ← Documentation
│   ├── how-it-works.md               ← Detailed 8-step workflow explanation
│   ├── contributing.md               ← Contribution guide
│   └── faq.md                        ← Frequently asked questions
├── examples/                         ← Example scan reports
│   ├── example-report-nodejs.md      ← Node.js scan with 12 findings
│   ├── example-report-python.md      ← Python scan with 11 findings
│   ├── example-report-php.md         ← PHP scan with 9 findings
│   └── example-report-clean.md       ← Clean codebase (0 findings)
├── tests/
│   ├── fixtures/                     ← Intentionally vulnerable test apps
│   │   ├── vulnerable-node-app/      ← Express.js app with SQLi, IDOR, etc.
│   │   ├── vulnerable-python-app/    ← Flask app with SSTI, path traversal, etc.
│   │   └── vulnerable-php-app/       ← PHP app with RCE, LFI, etc.
│   └── expected-outputs/             ← Regression test checklists
├── .github/
│   └── workflows/template-check.yml  ← PR & issue template compliance check
├── ISSUE_TEMPLATE/                   ← Bug report & false positive templates
├── PULL_REQUEST_TEMPLATE.md          ← PR checklist template
├── CHANGELOG.md
├── LICENSE                           ← MIT
└── README.md
```

---

## Example Output

See full reports in the [examples/](examples/) folder. Here's a summary from scanning the
Node.js test fixture:

```
┌────────────────────────────────────────────────┐
│           FINDINGS SUMMARY                     │
├──────────────┬─────────────────────────────────┤
│ 🔴 CRITICAL  │  4 findings                    │
│ 🟠 HIGH      │  5 findings                    │
│ 🟡 MEDIUM    │  2 findings                    │
│ 🔵 LOW       │  1 finding                     │
├──────────────┼─────────────────────────────────┤
│ TOTAL        │  12 findings                   │
└──────────────┴─────────────────────────────────┘
```

---

## Automation

A GitHub Actions workflow at [.github/workflows/template-check.yml](.github/workflows/template-check.yml)
automatically checks that every PR and issue follows the project templates:

- **Pull requests** must include: description, type of change, testing done, and checklist
- **Bug reports** (`[BUG]`) must include: environment, what you ran, expected/actual behavior
- **False positives** (`[FALSE POSITIVE]`) must include: finding details, justification, safe code, suggestion

The workflow comments on non-compliant submissions so contributors know what to fix.

---

## Contributing

We welcome contributions! You can:

- Add new vulnerability patterns
- Add support for new languages or frameworks
- Update the CVE watchlist with new advisories
- Improve detection accuracy (fix false positives/negatives)
- Add new test fixtures

See [docs/contributing.md](docs/contributing.md) for the full guide.

---

## FAQ

See [docs/faq.md](docs/faq.md) for answers to common questions including:

- What languages does this support?
- How is this different from Semgrep or SonarQube?
- Is my code sent to Anthropic?
- Does it auto-fix vulnerabilities?

---

## License

[MIT](LICENSE)
