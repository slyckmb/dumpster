# __version__.py

VERSION = "v0.2.4-dev"
REQUIREMENTS_VERSION = "0.2.4"

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

# Generate REVERSE_ALIASES for reverse mapping
REVERSE_ALIASES = {v: k for k, v in FILTER_ALIASES.items() if v}
