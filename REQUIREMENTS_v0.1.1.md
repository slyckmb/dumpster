# 🧾 REQUIREMENTS.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.1.1  
**Spec Compliance**: Guardrails 2.2.2  
**Author**: Jake (`Code`)  
**Purpose**: Parse Apple Health exports (`export.zip`) into structured `.csv` and `.json` formats for CLI-based scripting, data analysis, and visualization workflows.

---

## 1. Functional Requirements

- ✅ **F-01**: Unzip `export.zip` and locate `export.xml`
- ✅ **F-02**: Parse `<Record>` entries and extract:
  - `type`, `value`, `start_date`, `end_date`, `unit`, `source_name`, `creation_date`
- ✅ **F-03**: Normalize field names to `snake_case` in all outputs
- ✅ **F-04**: Parse `value` into correct type (`int`, `float`, `str`) based on `type`
- ✅ **F-05**: Convert timestamps to standard ISO 8601:
  - User options: `--utc`, `--local`, or `--iso`
- ✅ **F-06**: Optional filtering:
  - by `type`, `start_date`, `end_date`
- ✅ **F-07**: Output to:
  - `dumpster.csv`, `dumpster.json`, or both
  - Directory specified via `--outdir`
- ✅ **F-08**: CLI interface `dumpster.py` with `click`-based UX
- ✅ **F-09**: Log summary of parsed/skipped elements (e.g., `Record`, `Workout`, `ClinicalRecord`)
- ✅ **F-10**: Fails gracefully:
  - malformed XML
  - missing zip
  - invalid date format

---

## 2. Non-Functional Requirements

- 🧠 **NF-01**: Handles files >100MB efficiently
- 🔁 **NF-02**: Output is reproducible (idempotent)
- 🧪 **NF-03**: Compatible with macOS & Linux
- 📜 **NF-04**: All date values are in ISO 8601 format
- 💾 **NF-05**: CSV output uses `utf-8-sig`, fully quoted fields
- 🚫 **NF-06**: No network usage
- 🧼 **NF-07**: Output files sanitized for clean import to Excel, Notion, Airtable, SQLite

---

## 3. Inputs

| Name         | Type     | Description                                |
|--------------|----------|--------------------------------------------|
| `export.zip` | File     | Apple HealthKit export archive             |
| `export.xml` | XML File | Located inside `export.zip`; main data file |

---

## 4. Outputs

| File            | Format | Description                            |
|------------------|--------|----------------------------------------|
| `dumpster.csv`   | CSV    | Flat structured output                 |
| `dumpster.json`  | JSON   | List of normalized records             |
| `output/`        | Folder | Target directory for exported files    |
| `log_summary.txt`| TXT    | Summary of elements processed/skipped  |

---

## 5. Constraints

- Python 3.7+
- CLI-only tool (no GUI, no API)
- POSIX shell compatible
- Local-only (no cloud uploads or telemetry)
- All parsing logic contained in single script (`dumpster.py`)

---

## 6. Security Requirements

- ✅ `--safe` mode redacts sensitive fields:
  - `source_name`, `creation_date`, any `<MetadataEntry>`
- ✅ No external requests or telemetry
- ✅ Temp files cleaned after run
- ✅ Output directory creation locked to within current working directory
- ✅ Logs redact user identifiers in safe mode

---

## 7. Timestamp Handling

- User must choose one of:
  - `--utc`: Converts all times to UTC (`Z`)
  - `--local`: Preserves Apple's original timezone offset
  - `--iso`: Retains full ISO-8601 string w/ offset
- Timestamps normalized to `datetime.datetime` objects internally
- Output format: `YYYY-MM-DDTHH:MM:SSZ` or with `+/-hh:mm` offset

---

## 8. Metadata Handling

- Default: Unknown or extra XML attributes excluded
- `--include-extra`: Dumps unknown fields into `metadata` dict per record
- `--safe` mode: Strips all metadata
- Future versions may support structured `MetadataEntry` parsing

---

## 9. Data Type Handling

| Field Name     | Type       | Notes                               |
|----------------|------------|-------------------------------------|
| `type`         | `str`      | Record type (unmodified)            |
| `value`        | `int`/`float`/`str` | Cast automatically             |
| `unit`         | `str`      | Measurement unit (as string)        |
| `start_date`   | `datetime` | Parsed, normalized to ISO format    |
| `end_date`     | `datetime` | Same as above                       |
| `source_name`  | `str`      | May contain device/user PII         |
| `creation_date`| `datetime` | Optional — remove with `--safe`     |

---

## 10. Field Normalization Rules

- camelCase → snake_case (`startDate` → `start_date`)
- All keys lowercase
- Invalid or empty values replaced with `null`
- Key renaming handled uniformly across CSV and JSON

---

## 11. CSV Output Policy

- Encoding: `utf-8-sig` (ensures Excel compatibility)
- Quoting: All fields quoted (`QUOTE_ALL`)
- Delimiter: `,` by default; override with `--delimiter`
- Header: Always present
- Timestamps in ISO format

---

## 12. JSON Output Policy

- List of dictionaries
- Keys are normalized
- Optional `metadata` key with extra fields (`--include-extra`)
- Timestamps formatted as ISO strings

---

## 13. CLI Summary Output

At the end of each run:
```
Parsed: 12,480 Records
Skipped: 48 Workouts, 3 ClinicalRecords
Filtered: HKQuantityTypeIdentifierStepCount
Start: 2023-01-01 | End: 2024-01-01
Output: output/dumpster.csv, output/dumpster.json
```

---

## 14. Extensibility

Future support plans:
- [ ] Parse `<Workout>`, `<ClinicalRecord>`, `<ActivitySummary>`
- [ ] Output to SQLite or Parquet
- [ ] CLI subcommand: `dumpster stats` for aggregation/plots
- [ ] Interactive Web UI mode (local only)
- [ ] Native support for `metadataEntry`, `device`

---

## 15. Deliverables

| File                | Description                 |
|---------------------|-----------------------------|
| `dumpster.py`       | Single-file CLI tool        |
| `requirements.txt`  | Dependency list             |
| `README.md`         | Install and usage guide     |
| `REQUIREMENTS.md`   | This document               |
| `log_summary.txt`   | Post-run summary (optional) |

---

## 16. Acceptance Criteria

- [x] Run on real Apple exports from multiple users
- [x] Handles >100MB XML without crash
- [x] CLI flags documented and function as described
- [x] Output imports cleanly into:
  - pandas
  - SQLite
  - Excel / Google Sheets
  - Notion / Airtable
- [x] `--safe` removes all PII/metadata
- [x] Schema/version-proof for unknown attributes

---

🧑‍💻 *Dumpster: Because your health data deserves better than XML trash.*
