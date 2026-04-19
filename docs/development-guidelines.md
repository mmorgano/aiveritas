# AIVeritas Development Guidelines

## Purpose

This document defines the coding rules and development workflow for AIVeritas.
Use it as the reference during implementation, review, and maintenance.

## Core Principles

Apply the Zen of Python pragmatically:

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Readability counts.
- Errors should never pass silently.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one obvious way to do it.
- If the implementation is hard to explain, it is a bad idea.
- If the implementation is easy to explain, it may be a good idea.

## Project Rules

- Use Python 3.12+ features only when they improve clarity.
- Use type hints everywhere in application and test code.
- Use Google-style docstrings for public modules, functions, and classes.
- Keep all comments in English.
- After every code writing session or code review, run `make lint` and improve the `pylint` result before proceeding.
- Prefer small, focused functions over large multi-purpose functions.
- Raise explicit exceptions with actionable messages.
- Keep JSON report schemas consistent across modules.
- Prefer deterministic outputs over smart but unclear behavior.
- Do not introduce hidden side effects in helper functions.
- Keep validation logic modular and easy to extend.

## Code Style

- Prefer descriptive names over short abbreviations.
- Keep functions readable without relying on inline comments.
- Use constants only when they improve clarity or reduce duplication.
- Avoid premature abstraction.
- Avoid deep nesting when a guard clause is clearer.
- Prefer plain dictionaries only when a dedicated model would be excessive.

## Validation and Quality Gates

Run these checks before committing:

```bash
make lint
make test
make check
```

Quality gates:

- `pylint` must pass for `src` and `tests`.
- After each code change or review pass, rerun `pylint` and reduce warnings unless a documented exception is justified.
- `pytest` must pass.
- New features should include or update tests.
- Schema changes must preserve report consistency.

## Pylint Policy

`pylint` is used as a consistency gate, not as a goal by itself.

- Fix warnings when they improve clarity or correctness.
- Avoid disabling warnings unless there is a concrete reason.
- Keep configuration centralized in `pyproject.toml`.
- If a rule causes noise for this codebase, document the reason before disabling it.

## Review Checklist

Before opening a PR or finalizing a change, verify:

- The code is easy to read without additional explanation.
- Error messages are explicit and useful.
- The report schema remains stable and predictable.
- CLI behavior matches documentation.
- `make lint` has been executed after the latest code write or review cycle.
- Tests cover the main success and failure paths.
