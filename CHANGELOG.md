# Changelog

All notable changes to the Security Review Agent Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-22

### Added
- Initial release of security-review Agent Skill
- Full vulnerability scanning: SQLi, XSS, SSRF, command injection, IDOR, JWT, CSRF
- Secrets detection with regex + entropy heuristics for 15+ providers (AWS, Stripe, GitHub, OpenAI, Twilio, SendGrid, Slack, Google, Cloudflare, Mailgun, Heroku, and more)
- Language support: JavaScript/TypeScript, Python, Java, PHP, Go, Ruby, Rust
- Framework-specific patterns: Express, React, Next.js, Vue, Angular, Django, Flask, FastAPI, Spring Boot, Rails
- Dependency CVE watchlist for npm, pip, Maven, Rubygems, Cargo, Go
- IDE setup guides for VS Code, Cursor, Windsurf, and generic Claude-powered IDEs
- GitHub Actions CI/CD integration template for automated PR scanning
- Test fixtures for Node.js, Python, and PHP with intentionally vulnerable code
- 8-step self-verifying scan workflow with confidence ratings (HIGH/MEDIUM/LOW)
- Human-in-the-loop patch proposals for CRITICAL and HIGH findings
- Structured report format with executive summary, finding cards, and patch diffs
- Comprehensive documentation: how-it-works, contributing guide, FAQ
- Issue templates for bug reports and false positive reporting
- Pull request template with checklist
