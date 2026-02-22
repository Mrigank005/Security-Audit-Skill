<?php
/**
 * Vulnerable PHP App — Index / Router
 *
 * ⚠️ This app is intentionally vulnerable. For testing only.
 */

require_once 'config.php';

$page = isset($_GET['page']) ? $_GET['page'] : 'home';
include($_GET['page'] . ".php");

?>
<!DOCTYPE html>
<html>
<head><title>Vulnerable PHP App</title></head>
<body>
  <h1>Welcome</h1>
  <p>This is an intentionally vulnerable PHP application.</p>
</body>
</html>
