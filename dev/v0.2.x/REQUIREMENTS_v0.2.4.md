# 🧾 REQUIREMENTS_v0.2.4.md — DUMPSTER

**Version**: 0.2.4  
**Status**: dev  
**Focus**: `.fit` ingestion, XML+FIT workout merge, source tagging, DRY versioning  
**Guardrails**: 2.2.2 Compliant

---

## ✅ 1. CLI Interface — Full Spec

| Flag             | Type     | Default     | Description |
|------------------|----------|-------------|-------------|
| `export.zip`     | string   | required    | Apple Health export archive |
| `--fit-dir`      | path     | None        | Path to `.fit` files for workout merge |
| `--structure`    | choice   | `tree`      | `tree` or `flat` output |
| `--filter-type`  | string   | `all`       | Filter by alias (e.g. `heart`, `workouts`) |
| `--start`        | date     | None        | Start date (YYYY-MM-DD) |
| `--end`          | date     | None        | End date (YYYY-MM-DD) |
| `--savepath`     | path     | `.`         | Base directory to save output folder |
| `--summary`      | bool     | false       | Show summary only (no writes) |
| `--safe`         | bool     | false       | Remove PII from output |
| `--dryrun`       | bool     | false       | Simulate write only |
| `--list-types`   | bool     | false       | Show supported filter aliases |
| `--version`      | bool     | auto        | Show version and exit |

---

## 🧠 2. `.fit` File Support

### 📥 `--fit-dir` Behavior:
- Accepts path to folder with `.fit` files
- Parses using `fit_loader.py`
- Extracts:
  - `cadence`
  - `gps` (lat/lon traces)
  - `power`
  - heart rate (as fallback source)
- Builds synthetic workout objects if no XML match

---

## 🔁 3. Workout Merge Logic

| Field | Merge Rule |
|-------|------------|
| `type`, `start_time` | Must match (±30s, alias match) |
| `device`, `source_name` | XML preferred |
| `cadence`, `gps`, `power` | From `.fit` |
| `energy_kcal`, `duration_min` | From XML |
| `source` | Set to `"merged"` if dedup occurs |

### If no match:
- `.fit` = `"fit"`
- XML = `"xml"`

---

## 📦 4. Output: Tree Layout

```text
<savepath>/<input_basename>_<timestamp>/
├── raw/
│   ├── export.xml
│   └── *.fit
├── records/
│   ├── heart.json
│   ├── steps.json
│   ├── cadence.json
│   ├── gps.json
│   ├── power.json
├── workouts/
│   ├── 2024-05-01_run.json
│   ├── ...
├── summary.json
```

---

## 🗃️ 5. Output: Flat Layout

```json
{
  "records": {
    "heart": [...],
    "cadence": [...],
    ...
  },
  "workouts": [
    { "type": "run", "source": "merged", ... }
  ],
  "summary": {
    "record_types": {...},
    "total_workouts": 8,
    "merged_workouts": 4,
    "source_counts": {
      "xml": 5,
      "fit": 3
    }
  }
}
```

---

## 🔐 6. Guardrails

| Requirement           | Status |
|-----------------------|--------|
| `--safe` redaction    | ✅     |
| `--dryrun` support    | ✅     |
| Write-free `--summary`| ✅     |
| Timestamped folders   | ✅     |
| Source tagging        | ✅     |
| Dedup heuristics      | ✅     |
| DRY versioning        | ✅     |

---

## 📜 7. Changelog

| Version | Changes |
|---------|---------|
| 0.2.3   | Flat structure, alias filenames, dedup stub |
| **0.2.4** | `.fit` workout merge, active `--fit-dir`, DRY versioning, `cadence`/`gps`/`power` support |

---

**Signed off:** Jake (Code 🥷)  
**Date:** 2025-05-14  
**Applies To:** `dumpster.py v0.2.4-dev`
