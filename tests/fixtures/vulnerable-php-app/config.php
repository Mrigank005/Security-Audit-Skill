<?php
/**
 * Vulnerable PHP App — Configuration
 *
 * ⚠️ This app is intentionally vulnerable. For testing only.
 */

define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'SuperSecretDBPass123!');
define('DB_NAME', 'vulnerable_app');

define('API_KEY', 'sk_live_FAKE_KEY_REPLACE_ME_000');

define('INTERNAL_TOKEN', 'eyJhbGciOiJIUzI1NiJ9.dG9rZW4');

// Application settings
define('APP_DEBUG', true);
define('APP_ENV', 'production');

?>
