#!/usr/bin/env python3

import zipfile, os, json, click, datetime, tempfile
from lxml import etree
from collections import defaultdict
from pathlib import Path

from __version__ import VERSION, REQUIREMENTS_VERSION
from dedup import should_merge, merge_fit_into_apple
from fit_loader import load_fit_workouts

@click.command()
@click.version_option(
    version=VERSION,
    prog_name="DUMPSTER",
    message="%(prog)s %(version)s\nSpec: REQUIREMENTS_v" + REQUIREMENTS_VERSION + ".md"
)
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
    click.echo(f"📦 Version: {VERSION}")
    click.echo(f"📥 CLI Args: {export_zip}")
    click.echo(f"🔒 Spec: REQUIREMENTS_v{REQUIREMENTS_VERSION}.md")

    if list_types:
        print_aliases()
        return

    filter_list = normalize_filters(filter_type)
    output_path = resolve_output_path(export_zip, savepath)

    if summary:
        with tempfile.TemporaryDirectory() as tmp:
            xml_path = extract_xml(export_zip, tmp)
            records, workouts = parse_xml(xml_path, filter_type=filter_list, start=start, end=end, safe=safe)
        click.echo("\n[📊 Summary]")
        click.echo(f"Records: {sum(len(v) for v in records.values())}")
        click.echo(f"Workouts: {len(workouts)}")
        return

    xml_path = extract_xml(export_zip, output_path / 'raw')
    records, workouts = parse_xml(xml_path, filter_type=filter_list, start=start, end=end, safe=safe)

    fit_workouts = load_fit_workouts(fit_dir) if fit_dir else []
    merged, leftovers = merge_workouts(workouts, fit_workouts)

    all_workouts = merged + leftovers
    source_counts = {
        "xml": len(workouts),
        "fit": len(fit_workouts),
    }

    if structure == 'flat':
        dump_flat(records, all_workouts, output_path, source_counts, len(merged))
    else:
        output_tree(records, all_workouts, output_path, dryrun, source_counts, len(merged))

    if not dryrun:
        click.echo(f"\n✅ Output written to {output_path}")

def resolve_output_path(zipfile_path, savepath="."):
    base = Path(zipfile_path).stem
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    foldername = f"{base}_{timestamp}"
    return Path(savepath).expanduser().resolve() / foldername

def extract_xml(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    return os.path.join(extract_to, 'export.xml')
def print_aliases():
    from __version__ import FILTER_ALIASES, META_FILTERS
    click.echo("\nAvailable filter types:\n")
    for k, v in FILTER_ALIASES.items():
        if v: click.echo(f"  {k:10} → {v}")
    click.echo("\nMeta filters:\n")
    for k, v in META_FILTERS.items():
        click.echo(f"  {k:10} → {', '.join(v)}")

def normalize_filters(ftype):
    from __version__ import FILTER_ALIASES, META_FILTERS
    if not ftype or ftype == 'all':
        return None
    if ftype in META_FILTERS:
        return META_FILTERS[ftype]
    return [FILTER_ALIASES.get(ftype, ftype)]

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

def redact(record):
    return {
        k: v for k, v in record.items()
        if k not in ("source_name", "creation_date", "device", "file")
    }

def parse_xml(xml_path, filter_type=None, start=None, end=None, safe=False):
    from __version__ import REVERSE_ALIASES
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
            workout = {
                'type': el.get('workoutActivityType'),
                'duration_min': try_cast(el.get('duration')),
                'energy_kcal': try_cast(el.get('totalEnergyBurned')),
                'distance_km': try_cast(el.get('totalDistance')),
                'start_time': el.get('startDate'),
                'end_time': el.get('endDate'),
                'device': el.get('device'),
                'source': 'xml'
            }
            if safe: workout = redact(workout)
            workouts.append(workout)

    return records, workouts

def merge_workouts(xml_list, fit_list):
    merged = []
    fit_unmatched = []

    for fit in fit_list:
        match = None
        for xml in xml_list:
            if should_merge(xml, fit):
                match = xml
                break
        if match:
            merged.append(merge_fit_into_apple(match, fit))
        else:
            fit_unmatched.append(fit)
    return merged, fit_unmatched

def output_tree(records, workouts, outdir, dryrun, source_counts, merged_count):
    outdir = Path(outdir)
    if dryrun:
        click.echo(f"💡 [DRYRUN] Would write to {outdir}")
        return

    (outdir / 'records').mkdir(parents=True, exist_ok=True)
    (outdir / 'workouts').mkdir(parents=True, exist_ok=True)
    (outdir / 'raw').mkdir(parents=True, exist_ok=True)

    summary = {
        "record_types": {},
        "total_workouts": len(workouts),
        "source_counts": source_counts,
        "merged_workouts": merged_count
    }

    for rtype, items in records.items():
        alias = rtype.split('.')[-1].lower()
        with open(outdir / 'records' / f"{alias}.json", 'w') as f:
            json.dump(items, f, indent=2)
        summary["record_types"][alias] = len(items)

    for w in workouts:
        date = w['start_time'][:10]
        wtype = w['type'].split('Type')[-1].lower()
        with open(outdir / 'workouts' / f"{date}_{wtype}.json", 'w') as f:
            json.dump(w, f, indent=2)

    with open(outdir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

def dump_flat(records, workouts, outdir, source_counts, merged_count):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    flat = {
        "records": {},
        "workouts": workouts,
        "summary": {
            "record_types": {},
            "total_workouts": len(workouts),
            "source_counts": source_counts,
            "merged_workouts": merged_count
        }
    }
    for rtype, items in records.items():
        alias = rtype.split('.')[-1].lower()
        flat["records"][alias] = items
        flat["summary"]["record_types"][alias] = len(items)
    with open(outdir / 'dumpster.json', 'w') as f:
        json.dump(flat, f, indent=2)

if __name__ == '__main__':
    main()
