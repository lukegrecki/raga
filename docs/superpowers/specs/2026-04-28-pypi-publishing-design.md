# PyPI Publishing via GitHub Actions — Design

**Date:** 2026-04-28
**Status:** Approved, ready for implementation plan

## Goal

Publish the `ragamala` distribution to PyPI on every GitHub Release,
automatically and securely, without managing long-lived credentials.

The PyPI **distribution name** is `ragamala` (chosen because `raga` is
already taken). The Python **import name** (`raga`), the source directory
(`src/raga/`), the GitHub repo (`raga`), and the CLI commands (`raga`,
`tala`) are unaffected.

## Trigger

GitHub Release publication (`on: release: { types: [published] }`).

The release tag is the source of truth for the version. The workflow refuses
to publish if the tag does not match the version in `pyproject.toml`.

## Authentication

PyPI Trusted Publishing (OIDC). No API tokens, no GitHub secrets.

The publish job runs in a GitHub environment named `pypi` and requests an
OIDC token (`permissions: id-token: write`). PyPI is configured with a
trusted publisher binding the project to this repo + workflow + environment.

## Version management

Manual bump in `pyproject.toml`, with a workflow-level guard:

- Maintainer edits `version = "X.Y.Z"` in `pyproject.toml` and updates
  `CHANGELOG.md`, commits to `main`.
- Maintainer creates a GitHub Release with tag `vX.Y.Z`.
- Workflow validates: extracted `pyproject.toml` version `==` stripped tag.
  Fails loudly on mismatch.

`hatch-vcs` and similar dynamic-version schemes are explicitly rejected:
release cadence is low and the manual bump keeps `pyproject.toml` readable.

## Workflow structure

`.github/workflows/publish.yml` with three sequential jobs:

### Job 1: `test`

- Matrix: Python 3.11, 3.12, 3.13 on `ubuntu-latest`.
- Mirrors `ci.yml`: `pip install -e ".[dev]"`, `pytest tests/ -v`,
  `ruff check src/ tests/`.
- Acts as the publish gate. If any matrix cell fails, no build, no publish.

### Job 2: `build`

- `needs: test`. Single `ubuntu-latest` runner.
- Checks out the release tag.
- Tag/version validation step: extracts version from `pyproject.toml`,
  compares against `${{ github.ref_name }}` (stripped of leading `v`).
- `pip install build twine` → `python -m build` → produces sdist + wheel
  in `dist/`.
- `twine check dist/*` for metadata and README-render sanity.
- Uploads `dist/` as a workflow artifact for the publish job.

### Job 3: `publish`

- `needs: build`. Single `ubuntu-latest` runner.
- `environment: pypi` (scopes the OIDC trust; supports optional manual
  approval gate via environment protection rules).
- `permissions: id-token: write` at job level.
- Downloads the `dist/` artifact.
- Uses `pypa/gh-action-pypi-publish@release/v1` with no token argument
  (OIDC-only path).

## Pre-flight (one-time, manual)

These steps are **prerequisites**, not part of the workflow:

1. Configure a **pending Trusted Publisher** on PyPI:
   - Project name: `ragamala`
   - Owner: `lukegrecki`
   - Repository: `raga`
   - Workflow filename: `publish.yml`
   - Environment: `pypi`
3. Create a GitHub environment named `pypi` in repo settings. No secrets.
   Optionally add deployment protection rules (branch/tag restrictions or
   required reviewers).

## Release procedure (per release)

1. Update `CHANGELOG.md` (move Unreleased entries under the new version).
2. Bump `version` in `pyproject.toml`.
3. Commit on `main`, push.
4. `gh release create vX.Y.Z --generate-notes` (or use the GitHub UI).
5. Workflow runs. On success, version is on PyPI within a couple of minutes.

## Out of scope

- TestPyPI dry-run step. The package is pure Python with a simple
  `hatchling` build; the wheel was already verified locally. PyPI
  immutability is mitigated by the cheap version-bump escape hatch.
- Dynamic versioning via `hatch-vcs` or similar.
- API token authentication or any PyPI-related GitHub secret.
- Platform-specific wheel matrices (pure Python).
- Automated changelog generation beyond `gh release --generate-notes`.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Tag/version drift | Validation step fails the build before publish |
| Publishing a broken commit | `test` job gates `build` and `publish` |
| Leaked PyPI credentials | OIDC — no long-lived credentials exist |
| Re-publishing a yanked version | Bump to next patch version; PyPI is immutable by design |
| Name collision on first publish | Resolved — chose `ragamala` (`raga` was taken) |
