# Frequently Asked Questions

---

## What languages does this skill support?

The skill currently includes dedicated vulnerability patterns for:

| Language | Frameworks Covered |
|----------|--------------------|
| JavaScript / TypeScript | Node.js, Express, React, Next.js, Vue, Angular |
| Python | Django, Flask, FastAPI |
| Java | Spring Boot |
| PHP | Vanilla PHP, Laravel (partial) |
| Go | Standard library, common HTTP frameworks |
| Ruby | Rails |
| Rust | Cargo ecosystem |

The skill can also analyze **any language** at a general level — it reasons about code
logic, not just pattern matching. But detection accuracy is highest for the languages listed
above, which have dedicated pattern databases in `skill/references/language-patterns.md`.

Want to add a language? See [docs/contributing.md](contributing.md#adding-a-new-language).

---

## Does it work on private/proprietary code?

Yes. The skill runs entirely within your IDE's AI assistant (Claude). Your code is sent to
the Claude API for analysis — the same way any AI coding assistant works. It is **not**
uploaded to any third-party scanning service, dashboard, or database.

Key points:
- Your code is processed by the Claude API under Anthropic's usage policies
- No code is stored permanently by the skill itself
- No results are sent anywhere outside your IDE unless you configure CI/CD integration
- See [Is my code sent to Anthropic?](#is-my-code-sent-to-anthropic) for more details

---

## How is this different from traditional SAST tools like Semgrep or SonarQube?

| Aspect | Traditional SAST | This Skill |
|--------|-----------------|------------|
| **Detection method** | Pattern matching (AST rules, regex) | AI reasoning about code semantics |
| **Cross-file analysis** | Limited or requires configuration | Built-in: traces data flows across files |
| **False positive rate** | Often high — flags patterns without context | Lower — self-verification pass filters noise |
| **Setup** | Install server, configure rules, integrate CI | Drop a folder into your project |
| **Custom rules** | Write DSL/YAML rule definitions | Edit plain English in markdown files |
| **Business logic bugs** | Generally can't detect | Can reason about logic flaws |
| **Patch generation** | Some tools suggest fixes | Every CRITICAL/HIGH finding gets a patch |

**When to use both:** This skill excels at finding contextual vulnerabilities that
pattern-matching misses. Traditional SAST excels at exhaustive, deterministic coverage
at scale. For maximum security, use both.

---

## What does "confidence rating" mean?

Every finding includes a confidence rating that indicates how certain the skill is that
the finding is a genuine vulnerability:

| Confidence | Meaning |
|------------|---------|
| **HIGH** | The vulnerability is unambiguous. No sanitization was found. Exploitable as-is. |
| **MEDIUM** | The vulnerability likely exists but depends on runtime context, configuration, or a call path that couldn't be fully traced. |
| **LOW** | A suspicious pattern was detected but it could be a false positive. Flagged for human review. |

Use confidence to prioritize your review effort. Start with HIGH-confidence findings,
then work through MEDIUM and LOW as time permits.

---

## Why does it show a finding but say confidence is LOW?

This typically happens when:

1. **The pattern looks dangerous but context is ambiguous.** For example, `eval()` is
   called, but the input might come from a trusted source the skill can't verify.

2. **A framework might handle it.** The skill detected a potential XSS sink, but a
   framework's auto-escaping might neutralize it upstream.

3. **The variable path is unclear.** The skill traced user input partway to a sink, but
   lost the trail in a complex call chain or external module.

4. **It's a best-practice violation, not a confirmed exploit.** For example, using
   `Math.random()` for a token — it's weak, but whether it's exploitable depends on
   what the token protects.

LOW-confidence findings are worth reviewing but shouldn't cause alarm on their own.
If you confirm it's safe, consider filing a
[false positive report](https://github.com/YOUR_ORG/security-audit-skill/issues/new?template=false_positive.md)
to improve the skill.

---

## Can I scope the scan to just one file or directory?

Yes. Pass a path argument:

```
/security-review src/auth/login.js        # Single file
/security-review src/routes/              # Single directory
/security-review src/auth/ src/api/       # Multiple paths
```

You can also scope by scan type:

```
/security-review --type secrets           # Only secrets scan
/security-review --type deps              # Only dependency audit
```

If no path is given, the entire project is scanned from the root.

---

## How do I suppress a false positive permanently?

Currently, the skill does not have a built-in suppression mechanism (like
`// nosec` comments). To handle false positives:

1. **File a false positive report** using the
   [issue template](https://github.com/YOUR_ORG/security-audit-skill/issues/new?template=false_positive.md)
   — this helps improve the skill for everyone.

2. **Add the safe pattern** to `skill/references/vuln-categories.md` under the relevant
   category's "Safe patterns" section so the skill learns to recognize it.

3. **Add a code comment** explaining why the pattern is safe:
   ```js
   // Security note: This eval() only processes server-generated AST nodes,
   // never user input. Input is validated in middleware/validateAst.js.
   eval(trustedAstNode);
   ```
   The skill reads comments and will factor them into its confidence rating.

A formal suppression system (inline annotations) is on the roadmap for a future release.

---

## Does it auto-fix vulnerabilities?

**No.** The skill generates patch proposals for CRITICAL and HIGH findings, but it
**never** auto-applies them. Every patch is presented for human review first.

This is by design:
- AI-generated patches may have edge cases or break existing behavior
- Security fixes often need business context (e.g., which users should have access)
- You should understand every change made to security-critical code
- The skill explicitly states: "Review each patch before applying. Nothing has been changed yet."

---

## How do I keep the skill up to date?

The skill is a set of markdown files — updating is as simple as pulling the latest version:

### If installed in your project:
```bash
cd your-project/.claude/skills/security-review
git pull origin main
```

### If installed globally:
Replace the skill files with the latest version from the repository.

### What gets updated:
- New vulnerability patterns in `vuln-categories.md`
- New CVEs in `vulnerable-packages.md`
- New secret patterns in `secret-patterns.md`
- New language support in `language-patterns.md`
- Improvements to the scan workflow in `SKILL.md`

Check `CHANGELOG.md` to see what changed in each release.

---

## Is my code sent to Anthropic?

**Yes — the same way it is for any Claude-powered coding feature.**

When you run `/security-review`, your code is sent to the Claude API for analysis.
This is how the skill works — Claude reads your code to reason about vulnerabilities.

Important details:
- Anthropic's [usage policy](https://www.anthropic.com/policies) governs how your data
  is handled
- On the API tier, Anthropic does **not** train on your data by default
- The skill itself does not store, log, or transmit your code anywhere else
- Scan results stay in your IDE unless you configure CI/CD posting

If your organization has strict data residency or compliance requirements, consult
your security team and Anthropic's enterprise options before using any AI coding tool.

For teams that cannot send code externally, consider running a self-hosted Claude
instance if available through Anthropic's enterprise offerings.
