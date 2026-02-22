# Expected Findings — vulnerable-node-app

Regression test checklist. After running `/security-review` against
`tests/fixtures/vulnerable-node-app/`, verify each finding is detected:

## 🔴 CRITICAL

- [ ] CRITICAL: SQL Injection in src/routes/users.js (Line 22) — `req.params.id` interpolated into query
- [ ] CRITICAL: SQL Injection in src/routes/users.js (Line 68) — `req.params.term` interpolated into LIKE query
- [ ] CRITICAL: Command Injection in src/utils/helpers.js (Line 11) — `exec()` called with user-controlled input
- [ ] CRITICAL: Hardcoded Database Password in src/config/database.js (Line 6) — `SuperSecretDBPass123!`

## 🟠 HIGH

- [ ] HIGH: Hardcoded JWT Secret in src/routes/auth.js (Line 27) — `supersecret123`
- [ ] HIGH: JWT Token Has No Expiry in src/routes/auth.js (Lines 30–33) — `expiresIn` missing
- [ ] HIGH: MD5 Password Hashing in src/routes/auth.js (Lines 13, 45) — `crypto.createHash('md5')`
- [ ] HIGH: Missing Authentication on DELETE endpoint in src/routes/users.js (Lines 52–59)
- [ ] HIGH: IDOR in src/routes/users.js (Lines 35–44) — no ownership check on PUT

## 🟡 MEDIUM

- [ ] MEDIUM: Weak Random Number Generation in src/utils/helpers.js (Lines 23–27) — `Math.random()` for tokens
- [ ] MEDIUM: Vulnerable Dependency lodash@4.17.20 — CVE-2021-23337 (prototype pollution)

## 🔵 LOW

- [ ] LOW: Outdated Dependency axios@0.27.2 — CVE-2023-45857

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4     |
| HIGH     | 5     |
| MEDIUM   | 2     |
| LOW      | 1     |
| **TOTAL**| **12**|
