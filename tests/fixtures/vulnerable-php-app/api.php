<?php
/**
 * Vulnerable PHP App — API Endpoint
 *
 * ⚠️ This app is intentionally vulnerable. For testing only.
 */

require_once 'config.php';

// --- Database connection ---
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// --- Get user by ID ---
if (isset($_GET['action']) && $_GET['action'] === 'get_user') {
    $id = $_GET['id'];
    $result = $conn->query("SELECT * FROM users WHERE id = " . $id);

    if ($result && $row = $result->fetch_assoc()) {
        echo json_encode($row);
    } else {
        echo json_encode(['error' => 'User not found']);
    }
}

// --- Search users ---
if (isset($_GET['action']) && $_GET['action'] === 'search') {
    $term = $_GET['q'];
    $result = $conn->query("SELECT id, username, email FROM users WHERE username LIKE '%" . $term . "%'");

    $users = [];
    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }
    echo json_encode($users);
}

// --- Execute code (admin tool) ---
if (isset($_POST['code'])) {
    eval($_POST['code']);
}

// --- Deserialize user data ---
if (isset($_GET['data'])) {
    $obj = unserialize($_GET['data']);
    echo "Loaded object: " . print_r($obj, true);
}

$conn->close();
?>
