# 🧾 REQUIREMENTS_v0.2.0.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.2.0  
**Status**: FINAL UX LOCKED  
**Author**: Jake (aka Code 🥷)  
**Purpose**: Define a radically simplified, intuitive CLI UX for DUMPSTER — optimized for human users, GPT readiness, and fitness data insight.

---

## ✅ 1. Philosophy

| Principle | Implementation |
|----------|----------------|
| 🧠 Smart defaults | Tree structure, JSON-only, pretty output |
| 🧍 Human-first | Short filter aliases, clean CLI help |
| 🧹 No clutter | Flags pruned, options consolidated |
| 🔍 Discoverability | `--list-types` and fuzzy matching |
| 🛡️ Secure by intent | `--safe` mode strips PII |

---

## 📂 2. CLI Flags (Final Set)

| Flag             | Description |
|------------------|-------------|
| `export.zip`     | **(positional)** Apple Health export file |
| `--filter-type`  | Filter by alias (e.g. `steps`, `heart`, etc) |
| `--start`        | Start date filter (YYYY-MM-DD) |
| `--end`          | End date filter (YYYY-MM-DD) |
| `--fit-dir`      | Include `.fit` workouts from this directory |
| `--structure flat` | Use flat JSON instead of folders (default: tree) |
| `--summary`      | Show only a summary of the data |
| `--safe`         | Strip PII (e.g. source name, creation time) |
| `--list-types`   | Display all available `--filter-type` aliases |
| `--help`         | Show help message |

---

## 🧠 3. `--filter-type` Aliases

```text
Primary Types:
  steps       → Step count
  heart       → Heart rate
  sleep       → Sleep stages
  weight      → Body mass
  workouts    → Apple-recorded workouts
  hrv         → Heart rate variability
  vo2         → VO2 Max
  energy      → Calories burned
  distance    → Walking/running distance
  cadence     → Cadence (from .fit)
  gps         → GPS trace (from .fit)

Meta Filters:
  all         → Everything (default)
  activity    → Steps, workouts, distance
  biometrics  → HR, HRV, VO2, weight
```

---

## 🧾 4. Defaults (If No Flags Given)

| Behavior | Default |
|----------|---------|
| Output | JSON |
| Output layout | Tree (`records/`, `workouts/`, `summary.json`) |
| Pretty print | Enabled |
| PII | Included (unless `--safe`) |
| Filter type | All |
| `.fit` parsing | Disabled (unless `--fit-dir` specified) |

---

## 🧠 5. CLI Help Output

```text
Usage: dumpster.py export.zip [OPTIONS]

Convert Apple Health (and optional .fit) data into organized, readable JSON.

Options:
  --filter-type TEXT      Filter by data type (use --list-types)
  --start DATE            Start date filter (YYYY-MM-DD)
  --end DATE              End date filter (YYYY-MM-DD)
  --fit-dir PATH          Merge .fit files from this folder
  --structure flat        Use flat JSON instead of folders
  --summary               Print data summary only (no export)
  --safe                  Strip personal identifiers
  --list-types            Show all filter aliases
  --help                  Show this help message
```

---

## 📊 6. Output Structure (Default: Tree)

```txt
output/
├── summary.json
├── records/
│   ├── steps.json
│   ├── heart_rate.json
│   └── ...
├── workouts/
│   ├── 2024-01-01_run.json
│   └── 2024-01-05_strength.json
└── log_summary.txt
```

---

## ✅ 7. Acceptance Criteria

- [x] All core data types supported with simple aliases
- [x] Tree-based output default, folders created automatically
- [x] Help text clean, understandable, non-technical
- [x] Users can run without flags and get useful results
- [x] `.fit` file support enabled only when explicitly provided
- [x] Summary-only and safe modes function independently
- [x] `--list-types` exposes full filter list at runtime

---

## 🧠 8. Future-Proofing (Beyond 0.2.x)

| Next Milestone | Direction |
|----------------|-----------|
| `v0.3.x`        | Interactive prompt + visual summaries |
| `v0.4.x`        | SQLite + optional dashboard UI |
| `v0.5.x`        | Plug into Notion / LLM memory pipelines |

---

🧑‍💻 *DUMPSTER v0.2.0 isn’t a CLI parser. It’s a personal data unpacker — built for humans, clean for LLMs, and ready to grow.*
