# Contributing to jol-mcp-servers

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Git with GPG signing configured

## Commit Requirements

### Signed Commits

All commits **must** be GPG-signed:

```bash
git commit -S -m "feat(git-server): add diff range support"
```

Unsigned commits will be rejected by CI.

### Conventional Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `security`

### Audit Trail

Every commit must reference:
- A ticket/issue number
- The threat model impact (if introducing new tool or data access)

## Pull Request Process

1. Fork and create a feature branch
2. Run `make lint && make test` locally
3. Submit PR using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)
4. Address review comments
5. Squash-merge after approval from `@journeyoflife-org/platform-core`

## Code Standards

- **Linting**: Ruff for Python
- **Type Checking**: mypy strict mode
- **Security**: bandit + pip-audit in CI
- **Formatting**: Ruff formatter (4-space indent for Python)

## Adding a New MCP Tool

Before adding a tool, you must:

1. Document it in `docs/capability-manifest.md`
2. Perform Article 35 screening in `docs/DPIA-mcp-servers.md`
3. Justify the minimum permissions required
4. Add tests including injection attempt corpus
5. Update the threat model in `docs/threat-model.md`
