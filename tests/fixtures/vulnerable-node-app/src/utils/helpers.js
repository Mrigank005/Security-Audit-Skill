const { exec } = require('child_process');
const crypto = require('crypto');

/**
 * Run a system command — used for health checks and diagnostics.
 */
function runCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

/**
 * Generate a session token for a user.
 */
function generateSessionToken() {
  const token = Math.random().toString(36).substring(2) +
                Math.random().toString(36).substring(2) +
                Date.now().toString(36);
  return token;
}

/**
 * Generate a secure random token (the correct way — not used in this app).
 */
function generateSecureToken() {
  return crypto.randomBytes(32).toString('hex');
}

module.exports = {
  runCommand,
  generateSessionToken,
  generateSecureToken
};
