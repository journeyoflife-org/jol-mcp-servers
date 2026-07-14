## Description

<!-- Describe the changes in this PR -->

## Type of Change

- [ ] Bug fix
- [ ] New feature / tool
- [ ] Refactor
- [ ] Security fix
- [ ] Documentation

## Threat Model

<!-- REQUIRED: Describe the threat model impact of this change -->
- Does this PR introduce a new tool or data access path? [ ] Yes / [ ] No
- If yes, has the [threat model](../docs/threat-model.md) been updated? [ ] Yes / [ ] N/A
- If yes, has the [capability manifest](../docs/capability-manifest.md) been updated? [ ] Yes / [ ] N/A

## DPIA Gate

- [ ] Article 35 screening completed (if new data processing)
- [ ] No new PII access introduced (or DPIA updated)

## Audit Test

- [ ] New tool invocations are verified in audit log output
- [ ] Injection attempt corpus passes (if applicable)

## Checklist

- [ ] Signed commits (GPG)
- [ ] Conventional commit format
- [ ] `make lint` passes
- [ ] `make test` passes
- [ ] `make scan` passes
- [ ] Documentation updated (if applicable)
- [ ] Tests added for new functionality
