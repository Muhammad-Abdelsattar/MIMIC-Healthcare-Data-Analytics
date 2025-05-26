# Mapping table names to file names
TABLE_FILE_MAP = {
    "patients": "PATIENTS.csv",
    "admissions": "ADMISSIONS.csv",
    "chartevents": "CHARTEVENTS.csv",
    "labevents": "LABEVENTS.csv",
    "prescriptions": "PRESCRIPTIONS.csv",
    "diagnoses_icd": "DIAGNOSES_ICD.csv",
    "d_items": "D_ITEMS.csv",
    "d_labitems": "D_LABITEMS.csv",
}

# Parquet config for pyarrow
PARQUET_CONFIG = {
    "compression": "SNAPPY",
    "coerce_timestamps": "us",
    "use_deprecated_int96_timestamps": True,
    "allow_truncated_timestamps": True,
    "version": "2.6",
    "use_dictionary": True,
    "flavor": "spark",
}

# Tables to process
TABLES_TO_PROCESS = [
    "patients",
    "admissions",
    "chartevents",
    "labevents",
    "prescriptions",
    "diagnoses_icd",
    "d_items",
    "d_labitems",
]
