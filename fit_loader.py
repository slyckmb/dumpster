# fit_loader.py — v0.2.4: .fit file ingestion engine

from fitparse import FitFile
import os

def load_fit_workouts(fit_dir):
    """Parse .fit workouts from fit_dir. Return list of workout dicts."""
    workouts = []
    for file in os.listdir(fit_dir):
        if not file.endswith(".fit"):
            continue
        fpath = os.path.join(fit_dir, file)
        fitfile = FitFile(fpath)

        workout = {
            "type": "HKWorkoutActivityTypeRunning",  # placeholder
            "start_time": None,
            "end_time": None,
            "duration_min": None,
            "cadence": [],
            "gps": [],
            "heart": [],
            "source": "fit",
            "file": file
        }

        for record in fitfile.get_messages():
            if record.name == "record":
                d = record.get_values()
                if "timestamp" in d:
                    if not workout["start_time"]:
                        workout["start_time"] = d["timestamp"].isoformat()
                    workout["end_time"] = d["timestamp"].isoformat()
                if "cadence" in d:
                    workout["cadence"].append(d["cadence"])
                if "position_lat" in d and "position_long" in d:
                    workout["gps"].append((d["position_lat"], d["position_long"]))
                if "heart_rate" in d:
                    workout["heart"].append(d["heart_rate"])

        # Compute derived values
        if workout["start_time"] and workout["end_time"]:
            try:
                delta = fitfile.get_start_time()
                workout["duration_min"] = round((record.get_values()["timestamp"] - delta).total_seconds() / 60, 2)
            except:
                pass

        workouts.append(workout)
    return workouts
