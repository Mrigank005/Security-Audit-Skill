---
name: 🚫 False Positive Report
about: Report an incorrect finding — the skill flagged safe code as vulnerable
title: "[FALSE POSITIVE] "
labels: false-positive
assignees: ''
---

## The Finding That Was Flagged

- **Severity**: (e.g., CRITICAL / HIGH / MEDIUM / LOW)
- **Vulnerability Type**: (e.g., SQL Injection, Hardcoded Secret, Command Injection)
- **File**: (e.g., `src/routes/users.js`, Line 47)
- **Confidence Rating**: (e.g., HIGH / MEDIUM / LOW)

### Finding Output

<!-- Paste the exact finding card from the security report -->
```
paste finding here
```

## Why This Is a False Positive

<!-- 
  Explain why this code is actually safe. Be specific:
  - Is there sanitization/validation upstream that the skill missed?
  - Does a framework or middleware handle this automatically?
  - Is the "secret" a placeholder or non-sensitive value?
  - Is the variable not actually user-controlled?
-->

## The Actual (Safe) Code Pattern

<!-- 
  Show the full code context that proves this is safe.
  Include the upstream sanitization, middleware, or framework logic.
  ⚠️ SANITIZE ALL SECRETS.
-->
```
// paste safe code with context here
```

## Suggested Improvement to the Skill

<!-- 
  How could the skill be improved to avoid this false positive?
  For example:
  - "The skill should check for middleware X before flagging"
  - "The skill should recognize pattern Y as safe"
  - "Add this safe pattern to vuln-categories.md"
-->

## Additional Context

<!-- Language, framework version, or anything else relevant -->
