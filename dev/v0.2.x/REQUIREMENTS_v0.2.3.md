# 🧾 REQUIREMENTS_v0.2.3.md — Project: `DUMPSTER`

**Version**: 0.2.3  
**Release Name**: Output Enhancement  
**Supersedes**: v0.2.2  
**Status**: LOCKED  
**Guardrails**: 2.2.2 Fully Compliant

---

## 🧠 1. CLI Interface — Flags & Arguments

### ✅ Positional Argument

| Argument     | Required | Description                           |
|--------------|----------|---------------------------------------|
| `export.zip` | ✅        | Apple Health export ZIP archive       |

---

### ✅ Named Flags

| Flag            | Type   | Default     | Description |
|-----------------|--------|-------------|-------------|
| `--filter-type` | string | `"all"`     | Filter by short alias (`steps`, `heart`, etc.) |
| `--start`       | date   | `None`      | Filter start date (YYYY-MM-DD) |
| `--end`         | date   | `None`      | Filter end date (YYYY-MM-DD) |
| `--fit-dir`     | path   | `None`      | Optional path to `.fit` files (MVP stub only) |
| `--structure`   | choice | `"tree"`    | Output layout: `"tree"` or `"flat"` |
| `--savepath`    | path   | `"."`       | Folder to place output folder inside |
| `--summary`     | bool   | `False`     | Show summary stats only, no write |
| `--safe`        | bool   | `False`     | Remove personal identifiers from output |
| `--dryrun`      | bool   | `False`     | Log actions without writing files |
| `--list-types`  | bool   | `False`     | Show available aliases and meta filters |
| `--help`        | bool   |             | Print usage text |

---

## 📛 2. Filter Aliases

### 🧠 Aliases Map to Apple Types

| Alias     | Type |
|-----------|------|
| `steps`   | `HKQuantityTypeIdentifierStepCount` |
| `heart`   | `HKQuantityTypeIdentifierHeartRate` |
| `hrv`     | `HKQuantityTypeIdentifierHeartRateVariabilitySDNN` |
| `vo2`     | `HKQuantityTypeIdentifierVO2Max` |
| `weight`  | `HKQuantityTypeIdentifierBodyMass` |
| `energy`  | `HKQuantityTypeIdentifierActiveEnergyBurned` |
| `distance`| `HKQuantityTypeIdentifierDistanceWalkingRunning` |
| `sleep`   | `HKCategoryTypeIdentifierSleepAnalysis` |
| `workouts`| Apple `<Workout>` records |
| `cadence` | `.fit` placeholder |
| `gps`     | `.fit` placeholder |

### 🧬 Meta Aliases

| Alias        | Includes |
|--------------|----------|
| `activity`   | `steps`, `distance`, `workouts` |
| `biometrics` | `heart`, `hrv`, `vo2`, `weight` |
| `all`        | Default: no filtering |

---

## 📂 3. Output Folder Logic

### 🔹 Default Path

Output folder created using:
```
basename(export.zip) + _ + YYYYMMDD-HHMM
```

If no `--savepath` is given, folder lands in current directory.

**Example:**
```bash
dumpster.py apple_export.zip
→ ./apple_export_20250514-1640/
```

```bash
dumpster.py apple_export.zip --savepath /mnt/data
→ /mnt/data/apple_export_20250514-1640/
```

---

## 📁 4. Output Structure Modes

### 🧱 Tree Mode (`--structure tree`) [Default]

```text
output_folder/
├── summary.json
├── records/
│   ├── heart.json
│   ├── steps.json
│   └── ...
├── workouts/
│   ├── 2024-04-01_run.json
│   └── ...
└── raw/
    └── export.xml
```

### 📦 Flat Mode (`--structure flat`)

```text
output_folder/
└── dumpster.json
```

### Flat JSON Format

```json
{
  "records": {
    "heart": [...],
    "steps": [...]
  },
  "workouts": [...],
  "summary": {
    "record_types": { "heart": 12, "steps": 96 },
    "total_workouts": 4
  }
}
```

---

## 🧼 5. Safe Mode

If `--safe` is enabled:

- Removes:
  - `source_name`
  - `creation_date`
  - `device`
- Applies to:
  - All records
  - All workouts

---

## 🧪 6. Summary Mode

### With `--summary`:
- Parses data to memory
- No files or folders written
- Uses `tempfile.TemporaryDirectory()`
- Output format:
```text
📦 Version: v0.2.3
📥 Source: test_export.zip
⏱️ Timestamp: 2025-05-14T16:42:10Z

[📊 Summary]
Records: 221
Workouts: 6
Date Range: 2023-01-01 → 2025-01-01
```

---

## 🧩 7. Record & Workout Filename Conventions

| Type | Logic |
|------|-------|
| Records | Alias-based name (e.g. `heart.json`, `steps.json`) |
| Workouts | Format: `YYYY-MM-DD_<type>.json`, where `<type>` is normalized alias |
| Fallback | If alias not found, lowercased type shortname is used |

---

## 🛠️ 8. `.fit` Merge Placeholder

- `--fit-dir` is parsed but not processed
- No merge, dedup, or usage occurs yet
- Required for future `.fit` support (v0.2.4+)

---

## 🧠 9. Workout Dedup Strategy (Prep for v0.2.4)

### Objective:
Merge `.fit` workouts into Apple `<Workout>` records where appropriate.

### Matching Heuristics:
- Same `type` (normalized alias)
- `start_time` within ±30 seconds
- Overlap ≥80% in `duration` or `distance`

### Dedup Actions:
- Prefer Apple for `device`, `calories`
- Prefer `.fit` for `cadence`, `gps`, `splits`

---

## 🔐 10. Guardrails Compliance

| Requirement                    | Status |
|--------------------------------|--------|
| Safe mode (`--safe`)          | ✅ |
| Dryrun mode (`--dryrun`)      | ✅ |
| No writes in summary mode     | ✅ |
| Folder naming traceable       | ✅ |
| Output structure predictable  | ✅ |
| REQUIREMENTS citation         | ✅ |
| Filename aliases              | ✅ |
| Future `.fit` support stubbed | ✅ |

---

## 🧾 11. Changelog

| Version | Notes |
|---------|-------|
| 0.2.2   | `--savepath`, timestamped folders, summary fix |
| **0.2.3** | Alias-based filenames, `--structure flat`, `.fit` merge spec |

---

**Signed off:** Jake (Code 🥷)  
**Date:** 2025-05-14  
**Applies To:** `dumpster.py v0.2.3+`
