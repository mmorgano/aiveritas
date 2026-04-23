# Contributing to AIVeritas

Thank you for contributing to AIVeritas.
This file defines the default development workflow for code changes, reviews, and pull requests.

## Engineering Expectations

- Follow the Zen of Python pragmatically.
- Prefer readability over cleverness.
- Apply TDD for new features and bug fixes when practical.
- Use `pytest` for automated tests.
- Run `pylint` after each coding or review cycle and improve the result when possible.
- Use type hints in application and test code.
- Use Google-style docstrings for public modules, functions, and classes.
- Keep comments in English.
- Keep modules small and responsibilities clear.

## Development Workflow

1. Write or update tests first when the change affects behavior.
2. Implement the smallest change needed.
3. Run `make test`.
4. Run `make lint`.
5. Refactor while keeping tests green.
6. Run `make frontend-test` when changing the local demo interface or before full-repository release work.
7. Run `make review-check` before opening or updating a pull request.

## Project Commands

Use these commands from the repository root:

```bash
make bootstrap
make generate-samples
make lint
make test
make frontend-test
make review-check
make check
make ci
```

The optional local session workflow is intentionally private and should not be committed as project history.

## Coding Rules

- Keep code simple, explicit, and readable.
- Prefer focused functions and clear error messages.
- Keep report schemas stable and predictable.
- Avoid broad refactors unless they are required to support the change safely.
- Update architecture or decision documents when a change materially affects system structure.

Detailed project rules are documented in [docs/development-guidelines.md](/home/morgmau/projects/aiveritas/docs/development-guidelines.md).

## Quality Gates

- `pytest` must pass.
- `pylint` must pass, or any justified exception must be documented.
- Frontend tests should pass when the secondary demo interface is changed.
- After each code writing session, run `make lint`.
- After each review pass, run `make lint` again and improve the result when possible.
- New behavior should be covered by tests before the change is considered complete.

## Private Working Notes

- Local session notes under `SESSIONS/` are private workflow aids, not repository artifacts.
- Do not commit raw session logs.
- If a session produces a durable outcome, update the changelog, sprint record, backlog, or ADRs instead.

## Pull Requests

- Keep pull requests small and focused.
- Describe the reason for the change, not only the implementation details.
- Mention any schema changes or CLI behavior changes explicitly.
- Add or update tests for behavior changes.
- Update `README.md` or project documentation when workflow or usage changes.

## Coding Agents

- Follow the same engineering rules as human contributors.
- Do not treat documentation as optional when behavior, architecture, or process changes.
- Prefer incremental edits over broad speculative rewrites.
- When reviewing code, prioritize correctness risks, regressions, missing tests, and schema consistency.
