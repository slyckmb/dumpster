# REQUIREMENTS_v0.2.6.md

## 1. Versioning & Purpose

- **Version**: `v0.2.6`
- **Spec For**: Apple Health + .FIT parallel export with strict conversion fidelity
- **Status**: 📜 Canonical
- **Scope**: Hardening + non-destructive storage of XML and FIT data formats
- **Derived From**: `v0.2.5` with additions for robustness and future support

---

## 2. Canonical Guardrails

- **This document is canonical** — it supersedes all prior `.md` specs.
- **No deltas** — every requirement needed to build this version is restated here.
- Follows the **Guardrails 2.2.2** protocol (see `guardrails_bundle_v2.2.2.md`).
- All CLI and behavior must conform unless specifically flagged as deprecated or future.

### 🤖 GPT Implementation Guardrail

- GPT must minimize changes to the existing codebase when implementing this spec.
- Changes must **align with current architecture** and avoid unnecessary rewrites.
- GPT must **verify that it has the latest codebase in memory** before applying changes.

---

## 3. CLI Parameters (unchanged from 0.2.5)

| Flag               | Type             | Description                                          | Default        |
|--------------------|------------------|------------------------------------------------------|----------------|
| `--filter-type`    | `TEXT`           | Record filter alias (e.g. `heart`, `steps`, etc.)   | `all`          |
| `--start`          | `YYYY-MM-DD`     | Start date filter                                   | N/A            |
| `--end`            | `YYYY-MM-DD`     | End date filter                                     | N/A            |
| `--structure`      | `tree`/`flat`    | Output style                                        | `tree`         |
| `--summary`        | flag             | Show summary and exit (no files written)            | false          |
| `--dryrun`         | flag             | Simulate behavior without writing files             | false          |
| `--safe`           | flag             | Remove personal identifiers (device/source info)    | false          |
| `--savepath`       | `TEXT` (path)    | Output folder location                              | `./`           |
| `--fit-dir`        | `PATH`           | Folder of `.fit` files                              | N/A            |
| `--list-types`     | flag             | Show all record aliases                             | false          |
| `--version`        | flag             | Show version and spec                               | false          |

---

## 4. File Structure & Storage Behavior

### 4.1 General Output Rules

- Every run creates a new output folder named:
  ```
  {stem_of_input_filename}_{timestamp}
  ```
  Example:
  ```
  test_export_20250514-1430
  ```

- Folder is created inside `--savepath` (or `./` if omitted)

---

### 4.2 Tree Structure (default)

If `--structure tree`, output layout:

```
{savepath}/{auto_folder}/
├── raw/
│   ├── export.xml (if XML present)
│   └── *.fit (copied from input dir)
├── apple_health/
│   ├── summary.json
│   ├── records/
│   └── workouts/
├── fit/
│   ├── summary.json
│   └── workouts/
└── dumpster.json (flat merged view — deprecated)
```

---

### 4.3 Flat Structure

If `--structure flat`, write:
```
{savepath}/{auto_folder}/dumpster.json
```

Format:
```json
{
  "records": { "heart": [...], ... },
  "workouts": [...],
  "summary": { ... }
}
```

---

## 5. FIT Parsing

- Must parse `.fit` files using `fitparse`
- Extract fields:
  - `timestamp`
  - `heart_rate`
  - `cadence`
  - `position_lat` + `position_long`
- Store raw GPS points as `"gps": [[lat, lon], ...]`
- Store cadence as `"cadence": [...]`
- Store heart rate as `"heart": [...]`
- Save as:
  ```
  fit/workouts/{filename_without_ext}.json
  ```

- Tag metadata:
  ```json
  "source": "fit"
  ```

- Fit parsing must be **non-destructive**:
  - No merging with Apple Health XML
  - No transformation
  - If parsing fails, log error and skip file

---

## 6. XML (Apple Health) Parsing

- Parse `export.xml` from Apple Health `.zip`
- Extract `<Record>` and `<Workout>` nodes
- Match filter types using aliases

- Output to:
  ```
  apple_health/records/{alias}.json
  apple_health/workouts/{date}_{type}.json
  ```

- Tag metadata:
  ```json
  "source": "xml"
  ```

- Do not deduplicate or merge with `.fit`

---

## 7. Summary File

- `summary.json` must be created per format (`fit/` and `apple_health/`)
- Must contain:
  ```json
  {
    "record_types": { "heart": 23, ... },
    "total_workouts": 2,
    "source_counts": {
      "xml": 2,
      "fit": 3
    }
  }
  ```

---

## 8. Requirements for Hardening (0.2.6 Milestone)

### 8.1 Apple Health Robustness

- Code must parse *all* content found in Apple `.xml`
- Be defensive:
  - Catch missing attributes
  - Handle unknown tag types gracefully
- Use schema-free fallback logic
- **Must not drop any data** without an error log
- Treat export.xml as unversioned; support common schema evolution

### 8.2 FIT Robustness

- Use current public FIT SDK as baseline:
  https://www.thisisant.com/resources/fit

- Treat `.fit` as semi-structured data
- Parse what’s available, but allow for:
  - GPS-only files
  - No cadence
  - Multiple timestamps
- Fit files may contain different sports — support tagging
- **Do not assume “running”**
- Parser must label what data was found

---

## 9. Feature Deferrals to 0.3.x+

- Merge XML + FIT into single record → ❌ DEFERRED
- AI labeling of workouts → ❌ DEFERRED
- Output chunking or splitting → ❌ DEFERRED
- Weather / eBike overlay → ❌ DEFERRED
- Modular loader support → ❌ DEFERRED (tracked in v0.3.0 roadmap)

---
