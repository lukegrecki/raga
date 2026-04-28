# PyPI Publishing via GitHub Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically publish the `ragamala` distribution to PyPI on every GitHub Release via a Trusted-Publishing (OIDC) workflow.

**Architecture:** A single workflow file `.github/workflows/publish.yml` triggered by `release: published`. Three sequential jobs: `test` (matrix-tests, mirrors `ci.yml`), `build` (validates tag/version match, runs `python -m build`, `twine check`), `publish` (OIDC upload via `pypa/gh-action-pypi-publish` in environment `pypi`). No tokens, no secrets. Maintainer docs cover the one-time PyPI Trusted-Publisher pre-flight and the per-release procedure.

**Tech Stack:** GitHub Actions, `actions/checkout@v6`, `actions/setup-python@v6`, `actions/upload-artifact@v4`, `actions/download-artifact@v4`, `pypa/gh-action-pypi-publish@release/v1`, `build`, `twine`, PyPI Trusted Publishing.

**Design reference:** `docs/superpowers/specs/2026-04-28-pypi-publishing-design.md`

---

## File Structure

- **Create:** `.github/workflows/publish.yml` — the publish workflow (test → build → publish).
- **Modify:** `CONTRIBUTING.md` — add a "Releasing" section documenting the per-release procedure and the one-time PyPI Trusted-Publisher pre-flight.

No source code changes. No test code changes. The Python package itself is unaffected.

---

## Task 1: Skeleton workflow with test job

**Files:**
- Create: `.github/workflows/publish.yml`

This task lays down the workflow header, the trigger, and the `test` job (which mirrors `ci.yml`). The `build` and `publish` jobs are added in later tasks so each commit is reviewable in isolation.

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/publish.yml` with this content:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Test
        run: pytest tests/ -v

      - name: Lint
        run: ruff check src/ tests/
```

- [ ] **Step 2: Validate YAML parses**

Run:

```bash
.venv/bin/python -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"
```

Expected: no output, exit code 0.

- [ ] **Step 3: Sanity-check trigger and matrix with grep**

Run:

```bash
grep -n "types: \[published\]" .github/workflows/publish.yml
grep -n '3.11\|3.12\|3.13' .github/workflows/publish.yml
```

Expected: trigger line printed once; three Python versions printed.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "Add publish workflow skeleton with test job"
```

---

## Task 2: Add the build job with tag/version validation

**Files:**
- Modify: `.github/workflows/publish.yml`

The build job runs after `test` succeeds. It checks out the release tag, asserts the `pyproject.toml` version matches the tag, builds sdist + wheel, runs `twine check`, and uploads `dist/` as an artifact for the `publish` job.

- [ ] **Step 1: Append the `build` job**

Append the following to `.github/workflows/publish.yml` (below the `test` job, still under `jobs:`):

```yaml
  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
        with:
          ref: ${{ github.event.release.tag_name }}

      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"

      - name: Verify tag matches pyproject.toml version
        run: |
          set -euo pipefail
          tag="${{ github.event.release.tag_name }}"
          tag_version="${tag#v}"
          pyproject_version=$(
            python -c "import tomllib, pathlib; \
print(tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project']['version'])"
          )
          echo "Release tag:        $tag"
          echo "Stripped version:   $tag_version"
          echo "pyproject version:  $pyproject_version"
          if [ "$tag_version" != "$pyproject_version" ]; then
            echo "::error::Tag $tag (=$tag_version) does not match pyproject.toml version $pyproject_version"
            exit 1
          fi

      - name: Install build tooling
        run: pip install build twine

      - name: Build sdist and wheel
        run: python -m build

      - name: Check distribution metadata
        run: twine check dist/*

      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          if-no-files-found: error
          retention-days: 7
```

- [ ] **Step 2: Validate YAML still parses**

Run:

```bash
.venv/bin/python -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"
```

Expected: no output, exit code 0.

- [ ] **Step 3: Smoke-test the version-extraction command locally**

Run (this mirrors the inline Python in the workflow):

```bash
.venv/bin/python -c "import tomllib, pathlib; print(tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project']['version'])"
```

Expected: prints `0.1.0` (the current version in `pyproject.toml`).

- [ ] **Step 4: Smoke-test the tag-comparison logic locally**

Run (simulates the workflow's version-mismatch guard with a fake tag):

```bash
bash -c '
set -euo pipefail
tag="v0.1.0"
tag_version="${tag#v}"
pyproject_version=$(.venv/bin/python -c "import tomllib, pathlib; print(tomllib.loads(pathlib.Path(\"pyproject.toml\").read_text())[\"project\"][\"version\"])")
[ "$tag_version" = "$pyproject_version" ] && echo "match" || { echo "mismatch"; exit 1; }
'
```

Expected: prints `match`, exit code 0.

Then run the negative case:

```bash
bash -c '
set -euo pipefail
tag="v9.9.9"
tag_version="${tag#v}"
pyproject_version=$(.venv/bin/python -c "import tomllib, pathlib; print(tomllib.loads(pathlib.Path(\"pyproject.toml\").read_text())[\"project\"][\"version\"])")
[ "$tag_version" = "$pyproject_version" ] && echo "match" || { echo "mismatch"; exit 1; }
'
```

Expected: prints `mismatch`, exit code 1.

- [ ] **Step 5: Smoke-test `python -m build` and `twine check` locally**

Run:

```bash
.venv/bin/pip install build twine
rm -rf dist/
.venv/bin/python -m build
.venv/bin/twine check dist/*
```

Expected: `dist/` contains a wheel and an sdist; `twine check` reports `PASSED` for both.

Then clean up the build artifacts so they're not committed:

```bash
rm -rf dist/ build/ src/ragamala.egg-info/ 2>/dev/null || true
```

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "Add build job with tag/version validation and twine check"
```

---

## Task 3: Add the publish job (OIDC, environment `pypi`)

**Files:**
- Modify: `.github/workflows/publish.yml`

The publish job downloads the `dist/` artifact and uploads it to PyPI via OIDC. No `password` argument is passed to the action — that triggers the Trusted-Publisher path. The job runs in the `pypi` GitHub environment, which scopes the OIDC trust and supports optional protection rules.

- [ ] **Step 1: Append the `publish` job**

Append the following to `.github/workflows/publish.yml` (below the `build` job, still under `jobs:`):

```yaml
  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write

    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 2: Validate YAML still parses**

Run:

```bash
.venv/bin/python -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"
```

Expected: no output, exit code 0.

- [ ] **Step 3: Verify the structural invariants**

Run:

```bash
.venv/bin/python <<'PY'
import yaml
wf = yaml.safe_load(open('.github/workflows/publish.yml'))
jobs = wf['jobs']
assert set(jobs) == {'test', 'build', 'publish'}, jobs
assert jobs['build']['needs'] == 'test'
assert jobs['publish']['needs'] == 'build'
assert jobs['publish']['environment'] == 'pypi'
assert jobs['publish']['permissions'] == {'id-token': 'write'}
# OIDC path: the publish action must NOT receive a password/token arg
publish_steps = jobs['publish']['steps']
pub = next(s for s in publish_steps if s.get('uses', '').startswith('pypa/gh-action-pypi-publish'))
assert 'with' not in pub or 'password' not in pub.get('with', {}), pub
print("ok")
PY
```

Expected: prints `ok`, exit code 0.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "Add publish job using PyPI Trusted Publishing (OIDC)"
```

---

## Task 4: Document the release procedure and pre-flight in CONTRIBUTING.md

**Files:**
- Modify: `CONTRIBUTING.md` (append a new section at the end)

The workflow itself is now complete. The remaining work is human-facing documentation: the one-time PyPI pre-flight (which a maintainer must perform before the first successful release) and the repeatable per-release procedure.

- [ ] **Step 1: Append a "Releasing" section to `CONTRIBUTING.md`**

Append the following to the end of `CONTRIBUTING.md` (after the existing "Testing changes" section):

````markdown
## Releasing

Releases are published to PyPI automatically by `.github/workflows/publish.yml`
on every GitHub Release. The PyPI distribution name is `ragamala`; the import
name remains `raga`.

### One-time pre-flight (maintainer)

These steps must be completed once before the first release. They are not part
of the workflow.

1. On PyPI, configure a **pending Trusted Publisher** for the project:
   - Project name: `ragamala`
   - Owner: `lukegrecki`
   - Repository: `raga`
   - Workflow filename: `publish.yml`
   - Environment: `pypi`
2. In GitHub repo settings, create an **environment** named `pypi`. No secrets
   are required. Optionally add deployment protection rules (branch/tag
   restrictions or required reviewers).

### Per-release procedure

1. Move the entries under `## [Unreleased]` in `CHANGELOG.md` to a new
   `## [X.Y.Z] - YYYY-MM-DD` section.
2. Bump `version = "X.Y.Z"` in `pyproject.toml`.
3. Commit on `main` and push:

   ```bash
   git add CHANGELOG.md pyproject.toml
   git commit -m "Release vX.Y.Z"
   git push origin main
   ```

4. Create a GitHub Release with tag `vX.Y.Z`:

   ```bash
   gh release create vX.Y.Z --generate-notes
   ```

5. The `Publish to PyPI` workflow runs automatically. On success, the new
   version appears on PyPI within a couple of minutes.

### Notes

- The workflow refuses to publish if the release tag (with leading `v`
  stripped) does not match the `version` field in `pyproject.toml`. If it
  fails on this check, fix the version in `pyproject.toml` (or delete and
  recreate the release with the correct tag) and try again.
- PyPI versions are immutable. To recover from a broken release, bump to the
  next patch version rather than re-uploading.
````

- [ ] **Step 2: Verify the new section is present and well-formed**

Run:

```bash
grep -n "^## Releasing$" CONTRIBUTING.md
grep -n "pending Trusted Publisher" CONTRIBUTING.md
grep -n "gh release create" CONTRIBUTING.md
```

Expected: each pattern matches exactly once.

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "Document PyPI release procedure and Trusted-Publisher pre-flight"
```

---

## Task 5: Final review of the assembled workflow

**Files:**
- Read-only: `.github/workflows/publish.yml`, `CONTRIBUTING.md`

Final pass to confirm the assembled workflow is internally consistent before this branch is merged. No edits expected; if any fail, return to the relevant task and fix.

- [ ] **Step 1: Re-validate the full workflow**

Run:

```bash
.venv/bin/python <<'PY'
import yaml
wf = yaml.safe_load(open('.github/workflows/publish.yml'))
assert wf['name'] == 'Publish to PyPI'
assert wf['on']['release']['types'] == ['published']
jobs = wf['jobs']
assert list(jobs) == ['test', 'build', 'publish'], list(jobs)
# test job
assert jobs['test']['strategy']['matrix']['python-version'] == ['3.11', '3.12', '3.13']
# build job
assert jobs['build']['needs'] == 'test'
build_steps = [s.get('name') or s.get('uses') for s in jobs['build']['steps']]
assert any('Verify tag matches' in (n or '') for n in build_steps), build_steps
assert any(s.get('uses', '').startswith('actions/upload-artifact') for s in jobs['build']['steps'])
# publish job
assert jobs['publish']['needs'] == 'build'
assert jobs['publish']['environment'] == 'pypi'
assert jobs['publish']['permissions'] == {'id-token': 'write'}
pub_steps = jobs['publish']['steps']
assert any(s.get('uses', '').startswith('actions/download-artifact') for s in pub_steps)
pub = next(s for s in pub_steps if s.get('uses', '').startswith('pypa/gh-action-pypi-publish'))
assert 'password' not in pub.get('with', {}) and 'repository-url' not in pub.get('with', {})
print("ok")
PY
```

Expected: prints `ok`, exit code 0.

- [ ] **Step 2: Confirm no untracked PyPI build leftovers**

Run:

```bash
git status --porcelain
```

Expected: empty output (working tree clean). If `dist/`, `build/`, or
`src/ragamala.egg-info/` appear, delete them — they were left by the local
smoke test in Task 2 and should not be committed.

- [ ] **Step 3: No commit needed**

This task is verification-only. If anything failed, return to the relevant earlier task and amend.
