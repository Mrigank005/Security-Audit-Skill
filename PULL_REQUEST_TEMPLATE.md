## What does this PR change?

<!-- Provide a clear description of the changes and their purpose -->

## Type of Change

<!-- Check all that apply -->

- [ ] 🔍 **New vulnerability pattern** — added detection for a new vuln type
- [ ] 🌐 **New language support** — added patterns for a new language or framework
- [ ] 📦 **CVE update** — added or updated entries in the vulnerable packages watchlist
- [ ] 🐛 **Bug fix** — corrected a false positive, false negative, or broken behavior
- [ ] 📝 **Documentation** — updated docs, README, or reference files
- [ ] 🧪 **Test fixture** — added or updated test fixtures
- [ ] 🏗️ **Infrastructure** — CI/CD, GitHub Actions, repo structure

## Testing Done

<!-- Describe how you verified your changes work correctly -->

- [ ] Ran `/security-review` against a test fixture: <!-- which one? -->
- [ ] Compared findings against `tests/expected-outputs/` checklist
- [ ] Verified no regressions on existing fixtures
- [ ] Tested in IDE: <!-- which IDE and version? -->

## Checklist

- [ ] The skill still triggers correctly on `/security-review`
- [ ] All reference files (`skill/references/`) are up to date
- [ ] CHANGELOG.md has been updated with this change
- [ ] Documentation updated (if applicable)
- [ ] No real secrets, credentials, or sensitive data included
- [ ] Commit messages follow conventional format (e.g., `feat:`, `fix:`, `docs:`)
