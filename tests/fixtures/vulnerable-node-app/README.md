# Vulnerable Node App

> ⚠️ **This app is intentionally vulnerable. For testing only.**

This is a deliberately insecure Express.js application used to test the
`/security-review` skill. It contains known vulnerabilities across multiple
categories including:

- SQL injection
- Hardcoded secrets
- Weak cryptography (MD5 password hashing)
- JWT misconfiguration
- IDOR / missing access control
- Command injection
- Insecure random number generation
- Vulnerable dependencies (lodash, axios)

**DO NOT deploy this application.** It exists solely as a test fixture for
verifying that the security-review skill correctly detects these issues.
