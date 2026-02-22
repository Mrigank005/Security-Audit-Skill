# Expected Findings — vulnerable-php-app

Regression test checklist. After running `/security-review` against
`tests/fixtures/vulnerable-php-app/`, verify each finding is detected:

## 🔴 CRITICAL

- [ ] CRITICAL: SQL Injection in api.php (Line 22) — `$_GET['id']` concatenated into query
- [ ] CRITICAL: SQL Injection in api.php (Line 33) — `$_GET['q']` concatenated into LIKE query
- [ ] CRITICAL: Remote Code Execution in api.php (Line 44) — `eval($_POST['code'])`
- [ ] CRITICAL: Hardcoded Database Password in config.php (Line 11) — `SuperSecretDBPass123!`
- [ ] CRITICAL: Hardcoded Stripe API Key in config.php (Line 14) — `sk_live_FAKE_KEY_REPLACE_ME_000`

## 🟠 HIGH

- [ ] HIGH: Local File Inclusion in index.php (Line 13) — `include($_GET['page'] . ".php")`
- [ ] HIGH: Insecure Deserialization in api.php (Line 51) — `unserialize($_GET['data'])`
- [ ] HIGH: Hardcoded Service Token in config.php (Line 17) — JWT token hardcoded

## 🟡 MEDIUM

- [ ] MEDIUM: Debug Mode Enabled in config.php (Line 20) — `APP_DEBUG = true` with `APP_ENV = production`

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 5     |
| HIGH     | 3     |
| MEDIUM   | 1     |
| LOW      | 0     |
| **TOTAL**| **9** |
