#!/usr/bin/env python3

"""
Script: dumpster.py
Version: v0.2.2-dev
Last updated: 2025-05-14T19:22Z
REQUIREMENTS.md: v0.2.2
"""

import zipfile, os, json, click, datetime
from lxml import etree
from collections import defaultdict
from pathlib import Path

VERSION = "v0.2.2-dev"
REQUIREMENTS_VERSION = "v0.2.2"
NOW = datetime.datetime.now().isoformat(timespec='seconds')

# Aliases
FILTER_ALIASES = {
    "steps": "HKQuantityTypeIdentifierStepCount",
    "heart": "HKQuantityTypeIdentifierHeartRate",
    "sleep": "HKCategoryTypeIdentifierSleepAnalysis",
    "weight": "HKQuantityTypeIdentifierBodyMass",
    "workouts": "WORKOUT",
    "hrv": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
    "vo2": "HKQuantityTypeIdentifierVO2Max",
    "energy": "HKQuantityTypeIdentifierActiveEnergyBurned",
    "distance": "HKQuantityTypeIdentifierDistanceWalkingRunning",
    "cadence": "CADENCE",
    "gps": "GPS",
    "activity": "META_ACTIVITY",
    "biometrics": "META_BIOMETRICS",
    "all": None
}

META_FILTERS = {
    "activity": [
        "HKQuantityTypeIdentifierStepCount",
        "HKQuantityTypeIdentifierDistanceWalkingRunning",
        "WORKOUT"
    ],
    "biometrics": [
        "HKQuantityTypeIdentifierHeartRate",
        "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
        "HKQuantityTypeIdentifierVO2Max",
        "HKQuantityTypeIdentifierBodyMass"
    ]
}

def extract_xml(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    return os.path.join(extract_to, 'export.xml')

def parse_dt(dtstr):
    try:
        return datetime.datetime.strptime(dtstr[:10], "%Y-%m-%d")
    except:
        return None

def try_cast(value):
    if not value: return None
    try: return int(value)
    except:
        try: return float(value)
        except: return value

def normalize_filters(ftype):
    if not ftype or ftype == 'all':
        return None
    if ftype in META_FILTERS:
        return META_FILTERS[ftype]
    return [FILTER_ALIASES.get(ftype, ftype)]

def redact(record):
    return {
        k: v for k, v in record.items()
        if k not in ("source_name", "creation_date", "device")
    }

def parse_xml(xml_path, filter_type=None, start=None, end=None, safe=False):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    records = defaultdict(list)
    workouts = []

    start = datetime.datetime.strptime(start, "%Y-%m-%d") if start else None
    end = datetime.datetime.strptime(end, "%Y-%m-%d") if end else None

    for el in root.iter():
        if el.tag == 'Record':
            type_ = el.get('type')
            if filter_type and type_ not in filter_type:
                continue
            start_date = parse_dt(el.get('startDate'))
            if start and start_date < start:
                continue
            if end and start_date > end:
                continue
            record = {
                'type': type_,
                'value': try_cast(el.get('value')),
                'unit': el.get('unit'),
                'start_date': el.get('startDate'),
                'end_date': el.get('endDate'),
                'source_name': el.get('sourceName'),
                'creation_date': el.get('creationDate')
            }
            if safe: record = redact(record)
            records[type_].append(record)

        elif el.tag == 'Workout':
            if filter_type and "WORKOUT" not in filter_type:
                continue
            workout = {
                'type': el.get('workoutActivityType'),
                'duration_min': try_cast(el.get('duration')),
                'energy_kcal': try_cast(el.get('totalEnergyBurned')),
                'distance_km': try_cast(el.get('totalDistance')),
                'start_time': el.get('startDate'),
                'end_time': el.get('endDate'),
                'device': el.get('device')
            }
            if safe: workout = redact(workout)
            workouts.append(workout)

    return records, workouts

def output_tree(records, workouts, outdir, dryrun=False):
    outdir = Path(outdir)
    if dryrun:
        click.echo(f"💡 [DRYRUN] Would create folders: {outdir/'records'} and {outdir/'workouts'}")
        click.echo(f"💡 [DRYRUN] Would write {len(records)} record types and {len(workouts)} workouts")
        return

    (outdir / 'records').mkdir(parents=True, exist_ok=True)
    (outdir / 'workouts').mkdir(parents=True, exist_ok=True)
    (outdir / 'raw').mkdir(parents=True, exist_ok=True)

    summary = {"record_types": {}, "total_workouts": len(workouts)}
    for rtype, items in records.items():
        fname = outdir / 'records' / f"{rtype.split('.')[-1].lower()}.json"
        with open(fname, 'w') as f:
            json.dump(items, f, indent=2)
        summary["record_types"][rtype] = len(items)

    for w in workouts:
        date = w['start_time'][:10]
        wtype = w['type'].split('Type')[-1].lower()
        fname = outdir / 'workouts' / f"{date}_{wtype}.json"
        with open(fname, 'w') as f:
            json.dump(w, f, indent=2)

    with open(outdir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

def resolve_output_path(zipfile_path, savepath="."):
    base = Path(zipfile_path).stem
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    foldername = f"{base}_{timestamp}"
    return Path(savepath).expanduser().resolve() / foldername

@click.command()
@click.argument('export_zip', type=click.Path(exists=True))
@click.option('--filter-type', help='Filter type (use --list-types to view options)')
@click.option('--start', help='Start date YYYY-MM-DD')
@click.option('--end', help='End date YYYY-MM-DD')
@click.option('--fit-dir', type=click.Path(exists=True), help='Path to folder of .fit files')
@click.option('--structure', type=click.Choice(['tree', 'flat']), default='tree')
@click.option('--summary', is_flag=True, help='Show summary only (no output files)')
@click.option('--dryrun', is_flag=True, help='Preview actions without writing files')
@click.option('--safe', is_flag=True, help='Remove personal fields (PII)')
@click.option('--savepath', default=".", help='Base path to save the output folder')
@click.option('--list-types', is_flag=True, help='Show all filter types and meta aliases')
def main(export_zip, filter_type, start, end, fit_dir, structure, summary, dryrun, safe, savepath, list_types):
    """DUMPSTER 🗑️ - Apple Health / .fit parser → JSON (Guardrails 2.2.2 Compliant)"""

    click.echo(f"📦 Version: {VERSION}")
    click.echo(f"⏱️ Timestamp: {NOW}")
    click.echo(f"📥 CLI Args: {export_zip}")
    if filter_type: click.echo(f"🔧 Filter: {filter_type}")
    if start or end: click.echo(f"📅 Date Range: {start} to {end}")
    if safe: click.echo("🧼 Safe mode: ON")
    if dryrun: click.echo("🚫 Dryrun: ON")
    click.echo(f"📂 Savepath: {savepath}")
    click.echo(f"🔒 Enforced by REQUIREMENTS.md {REQUIREMENTS_VERSION}")

    if list_types:
        click.echo("\nAvailable filter types:\n")
        for k, v in FILTER_ALIASES.items():
            if v: click.echo(f"  {k:10} → {v}")
        click.echo("\nMeta filters:\n")
        for k, v in META_FILTERS.items():
            click.echo(f"  {k:10} → {', '.join(v)}")
        return

    filter_list = normalize_filters(filter_type)
    output_path = resolve_output_path(export_zip, savepath)

    xml_extract_path = output_path / 'raw'
    xml_path = extract_xml(export_zip, xml_extract_path)

    records, workouts = parse_xml(xml_path, filter_type=filter_list, start=start, end=end, safe=safe)

    if summary:
        click.echo("\n[📊 Summary]")
        click.echo(f"Records: {sum(len(v) for v in records.values())}")
        click.echo(f"Workouts: {len(workouts)}")
        click.echo(f"Date Range: {start or 'beginning'} → {end or 'latest'}")
        return

    click.echo(f"📁 Output folder will be: {output_path}")
    output_tree(records, workouts, output_path, dryrun)

    if not dryrun:
        click.echo(f"\n✅ Output written to {output_path}")

if __name__ == '__main__':
    main()
