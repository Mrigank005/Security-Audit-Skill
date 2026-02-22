# Vulnerable PHP App

> ⚠️ **This app is intentionally vulnerable. For testing only.**

This is a deliberately insecure PHP application used to test the
`/security-review` skill. It contains known vulnerabilities across multiple
categories including:

- SQL injection (direct `$_GET` input in `mysql_query()`)
- Local File Inclusion (`include($_GET['page'])`)
- Remote Code Execution (`eval($_POST['code'])`)
- Insecure deserialization (`unserialize()` with user input)
- Hardcoded database credentials
- Hardcoded API key (Stripe)
- Debug mode enabled in production

**DO NOT deploy this application.** It exists solely as a test fixture for
verifying that the security-review skill correctly detects these issues.
