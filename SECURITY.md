# Security Policy

## Reporting a Vulnerability

If you find a security issue in `aip` — the CLI, the npx shim, or the packaging
— please use GitHub's private vulnerability reporting
(**Security → Report a vulnerability**) rather than a public issue.

We will respond within 5 business days.

---

## Security rules the linter enforces

`aip check` flags these patterns in scanned projects:

- Animation assets (Lottie `.json`, Rive `.riv`) loaded from unpinned
  third-party origins — `sec/untrusted-asset`
- Remote scripts or assets without integrity protection
- Secrets or API keys embedded in animation configuration
