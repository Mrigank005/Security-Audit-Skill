# How It Works — The 8-Step Scanning Workflow

This document explains exactly what happens when you run `/security-review`.

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    /security-review                                 │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Step 1: Scope         │ ─── Detect languages, frameworks,
              │         Resolution     │     and scan boundaries
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 2: Dependency    │ ─── Check packages against
              │         Audit          │     CVE watchlist
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 3: Secrets &     │ ─── Regex + entropy scan
              │         Exposure Scan  │     for credentials
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 4: Vulnerability │ ─── Deep code reasoning
              │         Deep Scan      │     across all categories
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 5: Cross-File    │ ─── Trace data flows
              │         Data Flow      │     between files
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 6: Self-         │ ─── Re-examine each finding;
              │         Verification   │     filter false positives
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 7: Report        │ ─── Structured output
              │         Generation     │     grouped by severity
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Step 8: Patch         │ ─── Concrete fixes for
              │         Proposals      │     CRITICAL & HIGH findings
              └────────────────────────┘
```

---

## Step 1: Scope Resolution

**What it does:**
Determines which files and directories to scan. Detects the languages and frameworks
in use by examining manifest files (`package.json`, `requirements.txt`, `go.mod`,
`Cargo.toml`, `pom.xml`, `Gemfile`, `composer.json`, etc.).

**References used:**
- `skill/references/language-patterns.md` — loads language-specific vulnerability patterns
  for the detected stack

**Output:**
- List of files in scope
- Detected languages and frameworks
- Loaded language-specific patterns to apply in later steps

**Scope rules:**
- If the user provides a path (`/security-review src/auth/`), only that directory is scanned
- If no path is given, the entire project is scanned from root
- Binary files, `node_modules/`, `.git/`, and build output directories are excluded

---

## Step 2: Dependency Audit

**What it does:**
Checks all declared dependencies against a curated watchlist of packages with known
vulnerabilities (CVEs). This runs first because it's fast — you get quick wins before
the deeper scan.

**References used:**
- `skill/references/vulnerable-packages.md` — CVE watchlist for npm, pip, Maven, Rubygems,
  Cargo, and Go modules

**Files inspected:**
- `package.json` / `package-lock.json` (Node.js)
- `requirements.txt` / `pyproject.toml` / `Pipfile` (Python)
- `pom.xml` / `build.gradle` (Java)
- `Gemfile` / `Gemfile.lock` (Ruby)
- `Cargo.toml` (Rust)
- `go.sum` (Go)

**Output:**
- List of vulnerable packages with CVE identifiers
- Severity rating per package
- Recommended safe version to upgrade to

---

## Step 3: Secrets & Exposure Scan

**What it does:**
Scans ALL files — including config, `.env`, CI/CD definitions, Dockerfiles, and IaC
templates — for exposed credentials, API keys, tokens, and private keys. Uses both
regex pattern matching and Shannon entropy analysis.

**References used:**
- `skill/references/secret-patterns.md` — regex patterns for 15+ providers (AWS, Stripe,
  GitHub, OpenAI, etc.), entropy thresholds, and safe pattern exclusions

**What it catches:**
- Hardcoded API keys and tokens
- Database connection strings with embedded passwords
- Private keys committed to the repo
- `.env` files that should be in `.gitignore`
- Secrets in CI/CD configurations and Docker images

**Output:**
- List of exposed secrets with exact file and line number
- Provider identification (which service the key belongs to)
- Remediation steps including key rotation instructions

---

## Step 4: Vulnerability Deep Scan

**What it does:**
The core of the scan. Reads and reasons about the source code — not just pattern matching,
but understanding context, intent, and data flow within each file.

**References used:**
- `skill/references/vuln-categories.md` — detailed detection guidance for every category:
  injection flaws, auth/access control, data handling, cryptography, business logic
- `skill/references/language-patterns.md` — language-specific dangerous functions and patterns

**Categories scanned:**
| Category | Examples |
|----------|----------|
| Injection Flaws | SQL injection, XSS, command injection, SSRF, LDAP injection |
| Auth & Access Control | IDOR/BOLA, JWT weaknesses, missing auth, CSRF, privilege escalation |
| Data Handling | Insecure deserialization, path traversal, XXE |
| Cryptography | Weak hashing (MD5/SHA1), bad randomness, missing TLS |
| Business Logic | Race conditions, missing rate limits, integer overflow |

**Output:**
- Raw list of potential findings with code snippets
- Each finding tagged with severity and confidence
- These are preliminary — refined in Step 6

---

## Step 5: Cross-File Data Flow Analysis

**What it does:**
After scanning individual files, this step performs a holistic review tracing how data
moves across your entire application. It follows user-controlled input from entry points
(HTTP parameters, headers, request body, file uploads) all the way to sinks (database
queries, `exec` calls, HTML output, file system writes).

**References used:**
- All references from previous steps, plus understanding of the application architecture
  gathered during scope resolution

**What it catches:**
- Vulnerabilities that only appear when looking at multiple files together
- Input validated in one file but used unsafely in another
- Insecure trust boundaries between services or modules
- Second-order injection (data stored safely, then used unsafely later)

**Output:**
- Additional findings that single-file analysis would miss
- Data flow traces showing the path from source to sink

---

## Step 6: Self-Verification Pass

**What it does:**
Every finding from Steps 2–5 is re-examined with fresh eyes. The skill asks itself:
"Is this actually exploitable, or is there sanitization I missed?" This step is critical
for reducing false positives.

**Verification checks:**
1. Re-read the relevant code around each finding
2. Check if a framework or middleware already handles the vulnerability upstream
3. Verify that the flagged input is actually user-controlled
4. Confirm the sink is actually dangerous in this context
5. Downgrade or discard findings that aren't genuine vulnerabilities

**Output:**
- Final severity assigned: CRITICAL / HIGH / MEDIUM / LOW / INFO
- Final confidence assigned: HIGH / MEDIUM / LOW
- Discarded false positives are removed from the report

---

## Step 7: Report Generation

**What it does:**
Compiles all verified findings into a structured security report following the standard
format template.

**References used:**
- `skill/references/report-format.md` — defines the exact output format including the
  header, executive summary table, finding cards, dependency audit section, secrets section,
  and footer

**Report sections:**
1. **Header** — project name, scan date, scope, languages detected
2. **Executive Summary** — findings count by severity at a glance
3. **Findings** — grouped by category, each with location, vulnerable code, risk
   explanation, and recommended fix
4. **Dependency Audit** — vulnerable packages found
5. **Secrets Scan** — exposed credentials found
6. **Scan Coverage** — files scanned, lines analyzed

**Output:**
- The complete formatted security report

---

## Step 8: Patch Proposals

**What it does:**
For every CRITICAL and HIGH severity finding, generates a concrete, minimal code patch.
The patch shows the vulnerable code (before) and fixed code (after) with an explanation
of what changed and why.

**Patch rules:**
- Preserves original code style, variable names, and structure
- Adds an inline comment explaining the security fix
- Shows exact file and line number for each patch
- Nothing is auto-applied — all patches require human review

**Output:**
- Before/after code diffs for each CRITICAL and HIGH finding
- Explicit statement: "Review each patch before applying. Nothing has been changed yet."

---

## Summary

| Step | Purpose | Speed | References Used |
|------|---------|-------|-----------------|
| 1. Scope Resolution | Determine what to scan | Fast | `language-patterns.md` |
| 2. Dependency Audit | Check for known CVEs | Fast | `vulnerable-packages.md` |
| 3. Secrets Scan | Find exposed credentials | Fast | `secret-patterns.md` |
| 4. Vulnerability Deep Scan | Reason about code | Thorough | `vuln-categories.md`, `language-patterns.md` |
| 5. Cross-File Data Flow | Trace input → sink | Thorough | All of the above |
| 6. Self-Verification | Filter false positives | Fast | Re-reads code |
| 7. Report Generation | Format output | Fast | `report-format.md` |
| 8. Patch Proposals | Generate fixes | Moderate | Findings from steps 2–6 |
