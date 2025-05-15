# __version__.py — DRY constants for CLI version and spec tag

VERSION = "v0.2.5-dev"
REQUIREMENTS_VERSION = "0.2.5"

# Filter aliases (human → Apple types)
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

# Meta filter expansions
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

# Reverse alias map (for output filenames)
REVERSE_ALIASES = {
    v: k for k, v in FILTER_ALIASES.items() if v
}
