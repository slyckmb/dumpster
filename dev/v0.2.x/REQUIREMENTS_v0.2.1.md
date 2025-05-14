# 🧾 REQUIREMENTS_v0.2.1.md — Project: `DUMPSTER`

**Codename**: `DUMPSTER`  
**Version**: 0.2.1  
**Patch Release**: Adds `--outdir` support for custom folder naming  
**REPLACES**: `REQUIREMENTS_v0.2.0.md`  
**Guardrails**: 2.2.2 Compliant

---

## ✅ 1. Philosophy

| Principle | Implementation |
|----------|----------------|
| 🧠 Clarity | All output paths are user-definable |
| 🧍 Human-first | Folder layout easy to follow |
| 🧼 Safe | Output directory is sandboxed and overrideable |
| 🔍 Traceable | Version and path echo logged |
| 🔒 Compliant | All flags printed, summary block formatted |

---

## 📂 2. CLI Flags (Updated)

| Flag             | Description |
|------------------|-------------|
| `export.zip`     | **(positional)** Apple Health export zip |
| `--filter-type`  | Filter by record type alias |
| `--start`        | Filter by start date |
| `--end`          | Filter by end date |
| `--fit-dir`      | Include `.fit` workouts from this folder |
| `--structure flat` | Write flat JSON instead of tree layout |
| `--summary`      | Print summary block only |
| `--safe`         | Redact `source_name`, `creation_date`, `device` |
| `--dryrun`       | Preview actions, do not write files |
| `--list-types`   | Print available `--filter-type` options |
| `--outdir`       | **Override output path** (e.g. `output/v0.2.1-test`) |
| `--help`         | Show usage text |

---

## 🧠 3. `--outdir` Behavior

| Mode | Output Path |
|------|-------------|
| Default | `output/v0.2.1-pre/` |
| With `--outdir` | Whatever path is given (must be a valid folder name) |

If `--dryrun` is active, the folder is logged but not created.

---

## 🧾 4. Example Usages

### Default:
```bash
dumpster export.zip
# → output/v0.2.1-pre/
```

### Labeled:
```bash
dumpster export.zip --outdir output/v0.2.1-test1
```

### Clean preview:
```bash
dumpster export.zip --outdir output/preview --dryrun
```

---

## 📊 5. Output Structure (when tree)

```
output/[version_or_outdir]/
├── summary.json
├── records/
│   └── heart_rate.json
└── workouts/
    └── 2024-04-01_run.json
```

---

## 🧠 6. Logging Format

```
📦 Version: v0.2.1-pre
📥 CLI Args: export.zip
🔧 Flags: --structure tree, --outdir output/v0.2.1-test1
🔒 Enforced by REQUIREMENTS.md v0.2.1

[📊 Summary]
...
```

---

## 🔐 7. Requirements Lock

| Lockfile | Version |
|----------|---------|
| REQUIREMENTS.md | ✅ Required |
| REQUIREMENTS_v0.2.1.md | ✅ Active |
| REQUIREMENTS_v0.2.0.md | ✅ Superseded |

---

**Signed off:** Jake (Code 🥷)  
**Date:** 2025-05-14  
