# 📜 REQUIREMENTS_v0.2.5.md

**Milestone:** `v0.2.5-dev`  
**Scope:** Finalize support for `.fit` workouts with XML merge, restore lost canonical requirements from earlier 0.2.x versions, and resolve FIT merge fidelity.

---

## 🧠 Canonical Guardrails

This document is the source of truth for all behavior in this build.  
It is **not delta-based** and **fully self-contained**.

---

## 🎯 Goals

- Load `.fit` workout files via `--fit-dir`
- Merge with Apple Health `<Workout>`s when applicable
- Distinguish source of all workouts (`xml`, `fit`, `xml+fit`)
- Ensure parity with `v0.2.3` features
- Retain safe/summary/flat/tree behaviors

---

## 🚀 CLI Interface

| Flag              | Type                     | Description |
|-------------------|--------------------------|-------------|
| `export_zip`      | Path (arg)               | Apple Health export `.zip` file |
| `--filter-type`   | Alias / ID               | Filter data to a specific type or group |
| `--start`         | Date `YYYY-MM-DD`        | Lower bound for date filtering |
| `--end`           | Date `YYYY-MM-DD`        | Upper bound for date filtering |
| `--fit-dir`       | Path                     | Directory containing `.fit` files |
| `--structure`     | `tree` or `flat`         | Output format (default: `tree`) |
| `--savepath`      | Path                     | Where to save output folder (default: `.`) |
| `--summary`       | Flag                     | Print summary only (no output written) |
| `--dryrun`        | Flag                     | Preview output folder name without writing |
| `--safe`          | Flag                     | Strip PII fields from all output |
| `--list-types`    | Flag                     | Show valid filter types and meta aliases |
| `--version`       | Flag                     | Show current tool + requirements version |

---

## 📦 Filter Type Aliases

These values are passed to `--filter-type`.

### 🔹 Core Aliases

| Alias     | Maps to Apple Field |
|-----------|---------------------|
| `steps`   | `HKQuantityTypeIdentifierStepCount` |
| `heart`   | `HKQuantityTypeIdentifierHeartRate` |
| `sleep`   | `HKCategoryTypeIdentifierSleepAnalysis` |
| `weight`  | `HKQuantityTypeIdentifierBodyMass` |
| `hrv`     | `HKQuantityTypeIdentifierHeartRateVariabilitySDNN` |
| `vo2`     | `HKQuantityTypeIdentifierVO2Max` |
| `energy`  | `HKQuantityTypeIdentifierActiveEnergyBurned` |
| `distance`| `HKQuantityTypeIdentifierDistanceWalkingRunning` |
| `workouts`| `<Workout>` elements |
| `cadence` | `.fit`-only field |
| `gps`     | `.fit`-only field |

### 🔸 Meta Filters

| Alias        | Description |
|--------------|-------------|
| `activity`   | Movement-related (steps, distance, workouts) |
| `biometrics` | Health markers (HR, HRV, VO2, weight) |
| `all`        | Load everything (default) |

---

## 🗂️ Output Structure

### `tree` (default):

```
test_output/
└── v0.2.5-dev_20250515-0900/
    └── test_export_20250515-0900/
        ├── raw/
        │   └── export.xml
        ├── records/
        │   ├── steps.json
        │   ├── heart.json
        │   └── vo2.json
        ├── workouts/
        │   ├── 2024-04-01_running_merged.json
        │   ├── 2024-04-02_cycling_fit.json
        │   └── 2024-04-03_strength_xml.json
        ├── summary.json
        └── dumpster.json
```

### `flat`:

Single file: `dumpster.json` with 3 keys:
```json
{
  "records": { "heart": [...], "steps": [...] },
  "workouts": [...],
  "summary": { ... }
}
```

---

## 🧪 Summary Output

When `--summary` is used:

```txt
📊 Parsed: 520 records
🏃 Workouts: 6
📅 Date Range: 2023-01-01 → 2025-05-01
```

### In summary.json:

```json
{
  "record_types": {
    "heart": 320,
    "steps": 200
  },
  "total_workouts": 6,
  "source_counts": {
    "xml": 4,
    "fit": 4
  },
  "merged_workouts": 2
}
```

---

## 🧰 Merge Logic

### Matching Criteria

- Same activity type (e.g. `running`)
- Start time difference ≤ 2 minutes
- Duration difference ≤ 10%

### Merge Behavior

- Combine XML and FIT attributes
- Prefer FIT data if duplicate (e.g. distance)
- Set:
```json
"source": "xml+fit"
```

---

## 🧪 Safe Mode Behavior

When `--safe` is used, these fields are removed:

| Field          | Applies to |
|----------------|------------|
| `source_name`  | Record     |
| `creation_date`| Record     |
| `device`       | Workout    |
| `file`         | Workout    |

---

## 🧱 Output File Naming

| Type     | Pattern |
|----------|---------|
| Record   | `{alias}.json` |
| Workout  | `YYYY-MM-DD_<type>_<source>.json` |
| Flat     | `dumpster.json` |
| Raw XML  | `raw/export.xml` |
| Summary  | `summary.json` |

---

## 🛡️ GPT Compliance Note

This requirements document is **canonical and self-contained**.  
It adheres to Guardrails v2.2.2 and must be interpreted as a **complete source of truth**.  
Do not treat it as a changelog or delta document.

> ✅ All previous applicable requirements from versions `v0.2.0` → `v0.2.4` have been carried forward or replaced with explicitly updated logic.  
> 🚫 No behavior, field, flag, or structure should be assumed unless it appears here.

All implementations, test plans, and downstream tools **must follow** this document exactly as written.  
Changes to structure or meaning **require a new version**.

---

## 📌 Change Log

| Version | Changes |
|---------|---------|
| v0.2.0  | Simplified tree/flat output; dropped CSV/SQLite |
| v0.2.1  | Added `--savepath`, canonical output folders |
| v0.2.2  | Alias-based filenames, clean filters |
| v0.2.3  | Summary refactor, `source` tagging |
| v0.2.4  | Initial `.fit` support, merge scaffolding |
| v0.2.5  | ✅ Fully merged FIT/XML, tag-aware workouts, restored lost specs |

---
