import pyarrow as pa

SCHEMAS = {
    "prescriptions": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("hadm_id", pa.int64()),
            ("icustay_id", pa.int64()),
            ("startdate", pa.timestamp("us")),
            ("enddate", pa.timestamp("us")),
            ("drug_type", pa.string()),
            ("drug", pa.string()),
            ("drug_name_poe", pa.string()),
            ("drug_name_generic", pa.string()),
            ("formulary_drug_cd", pa.string()),
            ("gsn", pa.int64()),
            ("ndc", pa.int64()),
            ("prod_strength", pa.string()),
            ("dose_val_rx", pa.string()),
            ("dose_unit_rx", pa.string()),
            ("form_val_disp", pa.string()),
            ("form_unit_disp", pa.string()),
            ("route", pa.string()),
        ]
    ),
    "chartevents": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("hadm_id", pa.int64()),
            ("icustay_id", pa.int64()),
            ("itemid", pa.int64()),
            ("charttime", pa.timestamp("us")),
            ("cgid", pa.int64()),
            ("value_merged", pa.string()),
        ]
    ),
    "patients": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("gender", pa.string()),
            ("dob", pa.timestamp("us")),
            ("dod", pa.timestamp("us")),
            ("expire_flag", pa.bool_()),
        ]
    ),
    "admissions": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("hadm_id", pa.int64()),
            ("admittime", pa.timestamp("us")),
            ("dischtime", pa.timestamp("us")),
            ("admission_type", pa.string()),
            ("admission_location", pa.string()),
            ("discharge_location", pa.string()),
            ("insurance", pa.string()),
            ("language", pa.string()),
            ("religion", pa.string()),
            ("marital_status", pa.string()),
            ("ethnicity", pa.string()),
            ("diagnosis", pa.string()),
            ("hospital_expire_flag", pa.bool_()),
            ("has_chartevents_data", pa.bool_()),
        ]
    ),
    "d_items": pa.schema(
        [
            ("row_id", pa.int64()),
            ("itemid", pa.int64()),
            ("label", pa.string()),
            ("dbsource", pa.string()),
            ("linksto", pa.string()),
        ]
    ),
    "d_labitems": pa.schema(
        [
            ("row_id", pa.int64()),
            ("itemid", pa.int64()),
            ("label", pa.string()),
            ("fluid", pa.string()),
            ("category", pa.string()),
        ]
    ),
    "diagnoses_icd": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("hadm_id", pa.int64()),
            ("seq_num", pa.int64()),
            ("icd9_code", pa.string()),
        ]
    ),
    "labevents": pa.schema(
        [
            ("row_id", pa.int64()),
            ("subject_id", pa.int64()),
            ("hadm_id", pa.int64()),
            ("itemid", pa.int64()),
            ("charttime", pa.timestamp("us")),
            ("flag", pa.string()),
            ("value_merged", pa.string()),
        ]
    ),
}
