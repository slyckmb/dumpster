# 🗑️ DUMPSTER

**Dumpster** is a command-line tool that transforms raw Apple Health exports (`export.zip`) into clean, structured `.csv` and `.json` formats — perfect for data analysis, scripting, and health hacking.

---

## 🚀 Features

- ✅ Extracts records from `export.xml`
- ✅ Outputs to CSV, JSON, or both
- ✅ Supports filtering by `type` and `date range`
- ✅ Lightweight: no GUI, no bloat
- ✅ Works offline (local-only)
- ✅ Built for hackers, data nerds, and quantified-self enthusiasts

---

## 📦 Install

1. Clone this repo:
   ```bash
   git clone https://github.com/yourname/dumpster.git
   cd dumpster
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧠 Usage

```bash
python dumpster.py export.zip [OPTIONS]
```

### 🔧 Options

| Flag           | Description |
|----------------|-------------|
| `--outdir`     | Output directory (default: `output/`) |
| `--format`     | `csv`, `json`, or `both` (default: `both`) |
| `--filter-type`| Filter by record type (e.g. `HKQuantityTypeIdentifierStepCount`) |
| `--start`      | Filter records after this date (`YYYY-MM-DD`) |
| `--end`        | Filter records before this date (`YYYY-MM-DD`) |
| `--safe`       | Strip personal fields (`sourceName`, `creationDate`) from output |

---

## 📂 Example

```bash
python dumpster.py export.zip \
  --outdir parsed \
  --format both \
  --filter-type HKQuantityTypeIdentifierStepCount \
  --start 2024-01-01 \
  --end 2024-12-31
```

Generates:

```
parsed/
├── dumpster.csv
└── dumpster.json
```

---

## 🧪 Dev & Contributing

1. Create a working dev branch:
   ```bash
   git checkout -b v0.1x-dev
   mkdir -p dev/v0.1x
   ```

2. Run tests (coming soon):
   ```bash
   pytest
   ```

3. Contributions welcome via PR or fork 🤘

---

## 🛡️ License & Security

- Local-only: No network requests, no cloud uploads.
- Privacy-friendly: Use `--safe` to redact fields.

MIT License © 2025 Jake (`Code`) 🥷

---

## 🔗 Related

- Apple Health Export → [Settings > Health > Export All Data]
- Format docs: [https://developer.apple.com/documentation/healthkit](https://developer.apple.com/documentation/healthkit)
- Biohacking/Quantified Self communities

---

🧑‍💻 *Dumpster: Where your health data gets cleaned up and put to work.*
