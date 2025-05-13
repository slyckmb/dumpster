# 🧾 REQUIREMENTS.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.1.x  
**Spec Compliance**: Guardrails 2.2.2  
**Author**: Jake (aka Code 🥷)  
**Purpose**: Parse Apple Health exports (`export.zip` containing `export.xml`) into clean `.csv` and `.json` data formats for command-line and scripting workflows.

---

## 1. Functional Requirements

- ✅ **F-01**: Unzip `export.zip` and locate `export.xml`
- ✅ **F-02**: Parse `<Record>` entries and extract:
  - `type`, `value`, `startDate`, `endDate`, `unit`, `sourceName`, `creationDate`
- ✅ **F-03**: Optional filtering:
  - by `type` (e.g. steps, heart rate)
  - by date range (`--start`, `--end`)
- ✅ **F-04**: Output as `.csv`, `.json`, or both
- ✅ **F-05**: Create output directory if not present
- ✅ **F-06**: Provide CLI interface (`dumpster.py`)
- ✅ **F-07**: Errors must be handled gracefully:
  - corrupt ZIP
  - missing `export.xml`
  - invalid dates

---

## 2. Non-Functional Requirements

- 🧠 **NF-01**: Handles files >100MB
- 🔁 **NF-02**: Repeatable output; same input = same output
- 🧪 **NF-03**: Compatible with macOS & Linux
- 📜 **NF-04**: Outputs use ISO 8601 UTC timestamps
- 🚫 **NF-05**: No GUI or interactive components
- 🔍 **NF-06**: Should not require internet or cloud

---

## 3. Inputs

| Name       | Type     | Description |
|------------|----------|-------------|
| `export.zip` | File | Apple HealthKit export archive |
| `export.xml` | XML | Inside zip, main structured data file |

---

## 4. Outputs

| File                      | Format | Description |
|---------------------------|--------|-------------|
| `dumpster.csv`            | CSV    | Flat output with headers |
| `dumpster.json`           | JSON   | List of records |
| `output/`                 | Folder | Optional target dir for generated files |

---

## 5. Constraints

- Requires Python 3.7+
- CLI only — no GUI
- POSIX shell compatible
- Project must remain offline-safe (no net dependencies)
- Uses only open-source Python libs: `lxml`, `click`, `pandas` (optional)

---

## 6. Security Requirements

- ❌ No network calls
- ✅ CLI flag `--safe` to drop PII fields (`sourceName`, `creationDate`)
- ✅ Temp files removed after use
- ✅ All output constrained to local filesystem (no writing outside `--outdir`)

---

## 7. Extensibility

Planned future enhancements:
- [ ] Support `Workout`, `ClinicalRecord`, `ActivitySummary` nodes
- [ ] Optional SQLite backend
- [ ] Generate visual plots from step count or HR data
- [ ] Web UI (local-only) for data exploration
- [ ] CSV import to Airtable, Notion, etc.

---

## 8. Deliverables

| File                | Description |
|---------------------|-------------|
| `dumpster.py`       | Main CLI script |
| `requirements.txt`  | Python package manifest |
| `README.md`         | Usage, examples |
| `REQUIREMENTS.md`   | This doc |
| `dev/v0.1x/`        | Dev working area |

---

## 9. Acceptance Criteria

- [x] Run on 3+ different Apple exports
- [x] Handles bad/missing XML cleanly
- [x] Output files validated for correct format
- [x] Meets all F and NF requirements
- [x] Runs offline, in CLI, on Python 3.7+

---

🧑‍💻 *Dumpster isn't just parsing trash — it's making raw health data usable.*  
🧠 Ready to ship.

