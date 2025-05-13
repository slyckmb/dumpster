# 🧾 REQUIREMENTS_v0.1.2.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.1.2  
**Status**: Spec Locked  
**Author**: Jake (aka Code 🥷)  
**Purpose**: Evolve DUMPSTER from a raw XML converter into a **GPT-ready health data engine**, including Apple Health exports and `.fit` workout files, with full UX and LLM optimization.

---

## 1. 🧠 New Capabilities in 0.1.2

| Capability            | Description |
|------------------------|-------------|
| ✅ Structured Output Tree | Folder-based exports (`--structure tree`) |
| ✅ Per-Workout JSONs      | Split each workout into its own file |
| ✅ Auto-Include Biometrics| All relevant records during each workout |
| ✅ Unified JSON Format    | Normalized, GPT-friendly layout |
| ✅ FIT File Support       | Parse `.fit` alongside Apple Health and intelligently merge |
| ✅ Redundancy Handling    | Detect duplicate `.fit` + `.xml` workouts and deduplicate |
| ✅ Output Format Expansion| Adds `jsonl`, `sqlite`, `stdout` |
| ✅ Summary/Log Files      | Adds `summary.json`, `log_summary.txt` |
| ✅ Full CLI Flag Set      | User control over structure, merging, filtering, and file naming |

---

## 2. 🧾 Functional Requirements (New/Changed in 0.1.2)

### 2.1 Output Modes

- `--format [csv|json|both|jsonl|sqlite|stdout]`
- `--structure [flat|tree]` → Enables folder-based output
- `--outdir ./path/` → Output directory
- `--basename your_name` → Customize filenames (`your_name.json`, etc)

### 2.2 Workout Export Structure

If `--structure tree` is set, output folder becomes:

```txt
output/
├── records/
│   ├── steps.json
│   ├── heart_rate.json
│   └── ...
├── workouts/
│   ├── 2024-05-01_run_5k.json
│   └── 2024-05-03_strength.json
├── summary.json
├── log_summary.txt
└── raw/
    └── export.xml
```

### 2.3 Per-Workout File Format

```json
{
  "activity": {
    "type": "run",
    "start_time": "2024-05-01T07:30:00Z",
    "end_time": "2024-05-01T08:05:00Z",
    "duration_min": 35.2,
    "distance_km": 5.3,
    "energy_kcal": 375,
    "device": "Apple Watch Series 7"
  },
  "biometrics": {
    "heart_rate_avg": 141,
    "heart_rate_max": 167,
    "vo2_max": 42.1,
    "steps": 5333,
    "hrv_avg": 49
  },
  "metrics": {
    "heart_rate": [{ "time": "...", "bpm": 135 }],
    "cadence": [{ "time": "...", "rpm": 83 }],
    "position": [{ "time": "...", "lat": 37.77, "lon": -122.41 }]
  },
  "metadata": {
    "sources": ["apple_health", "fit"],
    "filename": "2024-05-01_run_5k.fit"
  }
}
```

---

## 3. 🔄 FIT File Support

### 3.1 Input

- `--fit-dir ./path/` → Directory of `.fit` files
- `--include-fit` → Enable parsing + merging with Apple Health workouts

### 3.2 Redundancy Strategy

- Match `.fit` to Apple workouts by time ± 30s, type, duration
- **Dedup logic**:
  - Skip duplicate metrics (e.g., HR, distance, calories)
  - Merge unique metrics (e.g., GPS, cadence)
- Tag merged records with `source`: `"apple_health"` or `"fit"`

### 3.3 FIT JSON Output Schema

Consistent with Apple format, plus:
- `laps`, `power`, `cadence`, `altitude`, `position`
- Flag: `--fit-dedup-strategy [skip|merge|override]`

---

## 4. 📊 Summary & Logs

### 4.1 Log Summary (`log_summary.txt`)
```
Parsed: 18,340 Records
Workouts: 74 total (61 from Apple, 13 from FIT)
FIT Merge Conflicts: 2 (resolved)
Output: 74 workout JSON files + 6 record summaries
```

### 4.2 Summary JSON

```json
{
  "record_types": {
    "steps": 8912,
    "heart_rate": 3311,
    ...
  },
  "workout_stats": {
    "total_workouts": 74,
    "avg_duration_min": 42.3
  },
  "time_range": {
    "start": "2023-01-01",
    "end": "2025-05-12"
  }
}
```

---

## 5. 🔧 Optional Output Control Flags

| Flag | Description |
|------|-------------|
| `--pretty` | Indent JSON |
| `--summary-only` | Don’t write files — just log stats |
| `--slim` | Don’t include `metrics` block (summary only) |
| `--biometrics steps,hrv,vo2` | Include specific biometrics |
| `--compress` | Zip final output tree |
| `--stdout` | Pipe JSON to terminal or another process |
| `--split-types` | Write one file per record type |

---

## 6. ⚙️ Required Dependencies

| Package | Use |
|---------|-----|
| `lxml` | XML parsing |
| `click` | CLI interface |
| `pandas` | Optional for CSV |
| `fitparse` | Required for `.fit` parsing |
| `sqlite3` | Built-in, if `--sqlite` used |

---

## 7. ✅ Acceptance Criteria

- [x] All files written conform to the new folder structure
- [x] All workouts include full biometric context
- [x] FIT files deduplicated correctly if Apple XML present
- [x] `summary.json` and `log_summary.txt` always produced
- [x] Flags produce expected results, combinations are valid
- [x] Output usable by LLMs, pandas, `jq`, or Notion/Airtable

---

## 8. 🧠 LLM Optimization Goals (Met)

| Feature | Reason |
|---------|--------|
| Per-workout JSONs | One prompt = one event |
| Full biometrics | Rich context for reasoning |
| Normalized keys | GPT parsing accuracy |
| Units explicit | No confusion about kcal vs kJ |
| Metadata fields | Prompting context ("from Apple Watch") |

---

## 🧑‍💻 Final Flag Set (v0.1.2)

```bash
--outdir ./out
--basename my_data
--format csv|json|jsonl|sqlite|both|stdout
--structure flat|tree
--fit-dir ./fits/
--include-fit
--fit-dedup-strategy skip|merge|override
--summary-only
--slim
--biometrics steps,hrv,vo2
--pretty
--compress
--stdout
```

---

🧠 DUMPSTER v0.1.2 isn’t just a converter anymore —  
It’s a **health intelligence pipeline**, ready for anything from `jq` to GPT to clinical research.

