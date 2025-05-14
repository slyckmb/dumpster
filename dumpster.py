#!/usr/bin/env python3

import zipfile, os, json, click, datetime
from lxml import etree
from collections import defaultdict

# ✅ Filter aliases
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
    "cadence": "CADENCE",  # placeholder for .fit
    "gps": "GPS",          # placeholder for .fit
    "activity": "META_ACTIVITY",
    "biometrics": "META_BIOMETRICS",
    "all": None
}

# ✅ Meta filter expansion
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

def extract_xml(zip_path, extract_to='output/raw'):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    return os.path.join(extract_to, 'export.xml')

def parse_xml(xml_path, filter_type=None, start=None, end=None):
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
            workouts.append(workout)

    return records, workouts

def try_cast(value):
    if not value: return None
    try:
        return int(value)
    except:
        try:
            return float(value)
        except:
            return value

def parse_dt(dtstr):
    try:
        return datetime.datetime.strptime(dtstr[:10], "%Y-%m-%d")
    except:
        return None

def normalize_filters(ftype):
    if not ftype or ftype == 'all':
        return None
    if ftype in META_FILTERS:
        return META_FILTERS[ftype]
    return [FILTER_ALIASES.get(ftype, ftype)]

def output_tree(records, workouts, outdir):
    os.makedirs(os.path.join(outdir, 'records'), exist_ok=True)
    os.makedirs(os.path.join(outdir, 'workouts'), exist_ok=True)

    summary = {"record_types": {}, "total_workouts": len(workouts)}
    for rtype, items in records.items():
        fname = os.path.join(outdir, 'records', f"{rtype.split('.')[-1].lower()}.json")
        with open(fname, 'w') as f:
            json.dump(items, f, indent=2)
        summary["record_types"][rtype] = len(items)

    for w in workouts:
        date = w['start_time'][:10]
        wtype = w['type'].split('Type')[-1].lower()
        fname = os.path.join(outdir, 'workouts', f"{date}_{wtype}.json")
        with open(fname, 'w') as f:
            json.dump(w, f, indent=2)

    with open(os.path.join(outdir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

@click.command()
@click.argument('export_zip', type=click.Path(exists=True))
@click.option('--filter-type', help='Filter type (use --list-types to view options)')
@click.option('--start', help='Start date YYYY-MM-DD')
@click.option('--end', help='End date YYYY-MM-DD')
@click.option('--fit-dir', type=click.Path(exists=True), help='Path to folder of .fit files')
@click.option('--structure', type=click.Choice(['tree', 'flat']), default='tree')
@click.option('--summary', is_flag=True, help='Show summary only (no output files)')
@click.option('--safe', is_flag=True, help='Remove personal fields')
@click.option('--list-types', is_flag=True, help='Show all filter types and meta aliases')
def main(export_zip, filter_type, start, end, fit_dir, structure, summary, safe, list_types):
    """DUMPSTER 🗑️ - Human-first Apple Health / .fit parser → JSON"""

    if list_types:
        click.echo("\nAvailable filter types:\n")
        for k, v in FILTER_ALIASES.items():
            if v: click.echo(f"  {k:10} → {v}")
        click.echo("\nMeta filters:\n")
        for k, v in META_FILTERS.items():
            click.echo(f"  {k:10} → {', '.join(v)}")
        return

    filter_list = normalize_filters(filter_type)

    xml_path = extract_xml(export_zip)
    records, workouts = parse_xml(xml_path, filter_type=filter_list, start=start, end=end)

    if summary:
        click.echo(f"\n📊 Parsed: {sum(len(v) for v in records.values())} records")
        click.echo(f"🏃 Workouts: {len(workouts)}")
        click.echo(f"⏳ Dates: {start or 'beginning'} → {end or 'latest'}\n")
        return

    outdir = "output"
    if structure == 'tree':
        output_tree(records, workouts, outdir)
        click.echo(f"✅ Output written to {outdir}/")

if __name__ == '__main__':
    main()
