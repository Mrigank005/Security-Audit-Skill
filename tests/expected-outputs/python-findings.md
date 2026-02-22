# Expected Findings — vulnerable-python-app

Regression test checklist. After running `/security-review` against
`tests/fixtures/vulnerable-python-app/`, verify each finding is detected:

## 🔴 CRITICAL

- [ ] CRITICAL: SQL Injection in app/routes/users.py (Line 24) — f-string in `SELECT * FROM users WHERE id =`
- [ ] CRITICAL: SQL Injection in app/routes/users.py (Line 43) — f-string in `SELECT ... WHERE username LIKE`
- [ ] CRITICAL: Server-Side Template Injection in app/utils/render.py (Lines 17–19) — user input passed as template to `render_template_string()`
- [ ] CRITICAL: Server-Side Template Injection in app/utils/render.py (Lines 27–29) — f-string into `render_template_string()`
- [ ] CRITICAL: Path Traversal in app/routes/users.py (Lines 64–69) — unsanitized filename in `send_file()`

## 🟠 HIGH

- [ ] HIGH: Hardcoded Flask SECRET_KEY in app/routes/auth.py (Line 12) — `dev-secret`
- [ ] HIGH: Unsafe YAML Deserialization in app/routes/users.py (Line 56) — `yaml.load()` with `FullLoader`
- [ ] HIGH: MD5 Password Hashing in app/routes/auth.py (Lines 28, 53) — `hashlib.md5()`
- [ ] HIGH: Vulnerable Dependency Pillow==9.0.0 — multiple CVEs, buffer overflow

## 🟡 MEDIUM

- [ ] MEDIUM: Debug Mode Enabled in app/__init__.py (Line 19) — `app.run(debug=True)`
- [ ] MEDIUM: Vulnerable Dependency PyYAML==5.4 — arbitrary code execution via `yaml.load()`

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 5     |
| HIGH     | 4     |
| MEDIUM   | 2     |
| LOW      | 0     |
| **TOTAL**| **11**|
