# ♻️ DUMPSTER Project Rehydration — v0.2.5

This document provides the essential rehydration context to resume development of the `DUMPSTER` tool at **version v0.2.5-dev**.

---

## 📦 Current Build

| Version        | Status   | Description                                      |
|----------------|----------|--------------------------------------------------|
| `v0.2.4-fx5`   | ✅ Stable | Patched XML-only workout output (no FIT bug)     |
| `v0.2.5-dev`   | 🔜 Active | FIT merge implementation milestone               |

---

## 🔧 Required Files

To restore full build context, upload the following:

| File                     | Purpose                               |
|--------------------------|----------------------------------------|
| `dumpster.py`            | Main CLI logic + output handling       |
| `__version__.py`         | Tracks semantic version + spec version |
| `Makefile`               | DRY test runner + QA CLI               |
| `fit_loader.py`          | Loads `.fit` files (WIP support)       |
| `dedup.py`               | Merge matching logic                   |
| `dev/v0.2.x/REQUIREMENTS_v0.2.5.md` | Canonical spec (must match behavior) |
| `test/test_export.zip`   | Test data for QA re-runs               |
| `test/fake_export/export.xml` | Raw XML for fine-grain tests     |
| `test/test.fit` (optional) | .fit file to validate merge logic   |
| `qa_log_*.txt` (optional) | QA logs from prior runs               |

---

## 🧪 Commands to Validate (Rehydrate QA)

```bash
make clean-tests
make test-summary
make test-tree
make test-flat
make test-qa
```

---

## 🧠 Dev Goals for v0.2.5

- [ ] Implement `merge_fit_into_apple()` to deduplicate workouts
- [ ] Tag merged workouts with `source: xml+fit`
- [ ] Enable full `.fit` + XML compatibility
- [ ] Ensure `--fit-dir` merges correctly with filter logic
- [ ] Update summary counts with merged metadata
- [ ] Ensure filenames reflect source correctly (`_xml`, `_fit`, `_merged`)

---

## 🛡️ Canonical Requirement Notice

This project is governed by [Guardrails v2.2.2].  
The requirements document for `v0.2.5` is canonical and complete — no behavior is valid unless it appears there.  
Do not rely on prior versions or changelogs.

---

## 🏁 Rehydrate Command

> Start a new session with:  
> **"Rehydrating DUMPSTER v0.2.5 — here are my current files and build context."**  
> Then upload the listed files.

🧠 This restores versioning, CLI, test logic, QA flows, and output contracts.
