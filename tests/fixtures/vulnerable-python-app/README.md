# Vulnerable Python App

> ⚠️ **This app is intentionally vulnerable. For testing only.**

This is a deliberately insecure Flask application used to test the
`/security-review` skill. It contains known vulnerabilities across multiple
categories including:

- SQL injection (f-string interpolation in raw queries)
- Unsafe YAML deserialization (yaml.load with user input)
- Path traversal in file download endpoint
- Server-Side Template Injection (SSTI via render_template_string)
- Hardcoded Flask SECRET_KEY
- MD5 password hashing
- Debug mode enabled (Werkzeug debugger exposed)
- Vulnerable dependencies (Pillow, PyYAML)

**DO NOT deploy this application.** It exists solely as a test fixture for
verifying that the security-review skill correctly detects these issues.
