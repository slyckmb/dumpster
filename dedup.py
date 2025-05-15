# dedup.py — v0.2.5-dev: Workout deduplication + FIT/XML merge logic

from datetime import datetime, timedelta

MERGE_WINDOW_MINUTES = 5  # time delta threshold for merging

def parse_dt_iso(dtstr):
    """Parses ISO 8601 timestamps into datetime objects."""
    try:
        return datetime.fromisoformat(dtstr.replace("Z", "+00:00"))
    except:
        return None

def should_merge(xml, fit):
    """Determine if XML + FIT workouts refer to the same activity."""
    x_start = parse_dt_iso(xml.get("start_time"))
    f_start = parse_dt_iso(fit.get("start_time"))
    if not x_start or not f_start:
        return False

    delta = abs((x_start - f_start).total_seconds()) / 60
    return delta <= MERGE_WINDOW_MINUTES

def merge_fit_into_apple(xml, fit):
    """Merge FIT fields into Apple XML workout."""
    merged = dict(xml)  # start with XML base
    merged["source"] = "xml+fit"
    merged["file"] = fit.get("file")

    # Add new fields
    if fit.get("cadence"):
        merged["cadence"] = fit["cadence"]
    if fit.get("gps"):
        merged["gps"] = fit["gps"]
    if fit.get("heart"):
        merged["heart"] = fit["heart"]

    return merged
