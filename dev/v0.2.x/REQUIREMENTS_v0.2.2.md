# 🧾 REQUIREMENTS_v0.2.2.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.2.2  
**Patch Summary**: Adds `--savepath` logic using input ZIP basename and timestamp to name output folder  
**REPLACES**: `REQUIREMENTS_v0.2.1.md`, supersedes `--outdir` logic  
**Guardrails**: Fully 2.2.2 Compliant  
**Status**: LOCKED

---

## ✅ 1. Output Path Strategy (Updated)

| Feature | Description |
|--------|-------------|
| 📛 Input-aware | Output folder is based on input ZIP name |
| 🕒 Timestamped | Prevents overwrite and preserves history |
| 📂 Folder-named | No nesting — full tree saved at target location |
| 🌲 Traceable | Folder name always reflects source zip + run time |

---

## 📥 2. CLI Flags (Final)

| Flag             | Description |
|------------------|-------------|
| `export.zip`     | Apple Health export zip file |
| `--filter-type`  | Filter by record alias |
| `--start`        | Start date |
| `--end`          | End date |
| `--fit-dir`      | `.fit` file folder *(stub only)* |
| `--structure`    | `tree` or `flat` output |
| `--summary`      | Show summary block only |
| `--safe`         | Redact PII |
| `--dryrun`       | Preview with no writes |
| `--list-types`   | Show all aliases |
| `--savepath`     | Base folder to write output into (default: `"."`) |
| `--help`         | Show help message |

---

## 🧠 3. Savepath Behavior

### When called as:
```bash
dumpster.py apple_export.zip
```

➡️ Output folder created:
```bash
./apple_export_20250514-1532/
```

### With override:
```bash
dumpster.py apple_export.zip --savepath /mnt/data
```

➡️ Output:
```bash
/mnt/data/apple_export_20250514-1532/
```

---

## 📁 4. Output Structure (Tree Mode)

```txt
[savepath]/[input_basename]_[timestamp]/
├── summary.json
├── records/
├── workouts/
└── raw/
```

---

## 🔧 5. Deprecated Flag

| Deprecated | Reason |
|------------|--------|
| `--outdir` | Replaced by `--savepath` and source-based naming for UX clarity |

---

## 🛡️ 6. Guardrails Fulfilled

| Guardrail Requirement     | Status |
|---------------------------|--------|
| No overwrite risk         | ✅ Timestamped folder prevents collision |
| Predictable traceability  | ✅ Input ZIP name drives folder naming |
| Human-readable structure  | ✅ Folder layout, no nesting |
| Composable automation     | ✅ CI-ready, shell-friendly |
| Flag logging              | ✅ `--savepath` shown in CLI echo |
| REQUIREMENTS citation     | ✅ Logged at runtime |

---

## 🧠 7. Changelog

| Version | Additions |
|---------|-----------|
| 0.2.1   | `--outdir` override logic |
| **0.2.2** | `--savepath` replaces `--outdir`; timestamped folder naming based on input zip |

---

**Signed off:** Jake (Code 🥷)  
**Date:** 2025-05-14  
**Applies To:** `dumpster.py v0.2.2+`
