import pandas as pd
import pyarrow as pa
from utils import convert_to_hive_timestamps
from schemas import SCHEMAS


def clean_d_items(df):
    """Clean D_ITEMS table"""
    cols_to_drop = ["abbreviation", "param_type", "unitname", "category", "conceptid"]
    df = df.drop(columns=cols_to_drop, errors="ignore")

    df["itemid"] = df["itemid"].astype("Int64")

    return pa.Table.from_pandas(
        df[SCHEMAS["d_items"].names], schema=SCHEMAS["d_items"], preserve_index=False
    )


def clean_d_labitems(df):
    """Clean D_LABITEMS table"""
    df = df.drop(columns=["loinc_code"], errors="ignore")

    df["itemid"] = df["itemid"].astype("Int64")

    return pa.Table.from_pandas(
        df[SCHEMAS["d_labitems"].names],
        schema=SCHEMAS["d_labitems"],
        preserve_index=False,
    )


def clean_chartevents(df):
    """Clean CHARTEVENTS table with type-safe merging"""
    df["charttime"] = pd.to_datetime(df["charttime"])

    cols_to_drop = [
        "resultstatus",
        "stopped",
        "error",
        "warning",
        "valueuom",
        "storetime",
    ]
    df = df.drop(columns=cols_to_drop, errors="ignore")

    df["value_merged"] = df["valuenum"].astype(str).fillna(df["value"])

    df["icustay_id"] = df["icustay_id"].astype("Int64")
    df["cgid"] = df["cgid"].astype("Int64")
    df["itemid"] = df["itemid"].astype("Int64")

    df = df.drop(columns=["value", "valuenum"])

    df = convert_to_hive_timestamps(df, ["charttime"])

    return pa.Table.from_pandas(
        df[SCHEMAS["chartevents"].names],
        schema=SCHEMAS["chartevents"],
        preserve_index=False,
    )


def clean_labevents(df):
    """Clean LABEVENTS table"""
    df["charttime"] = pd.to_datetime(df["charttime"])

    df["hadm_id"] = df["hadm_id"].astype("Int64")
    df["itemid"] = df["itemid"].astype("Int64")

    df["value_merged"] = df["valuenum"].fillna(df["value"])
    df = df.dropna(subset=["value_merged"])

    df["value_merged"] = (
        df["value_merged"].astype(str) + " " + df["valueuom"].fillna("")
    )
    df = df.drop(columns=["value", "valuenum", "valueuom"])

    df = convert_to_hive_timestamps(df, ["charttime"])

    return pa.Table.from_pandas(
        df[SCHEMAS["labevents"].names],
        schema=SCHEMAS["labevents"],
        preserve_index=False,
    )


def clean_prescriptions(df):
    """Clean PRESCRIPTIONS table"""
    df["startdate"] = pd.to_datetime(df["startdate"])
    df["enddate"] = pd.to_datetime(df["enddate"], errors="coerce")

    df["icustay_id"] = df["icustay_id"].astype("Int64")
    df["gsn"] = pd.to_numeric(df["gsn"], errors="coerce").astype("Int64")
    df["ndc"] = pd.to_numeric(df["ndc"], errors="coerce").astype("Int64")

    cols_to_impute = [
        "drug_name_poe",
        "drug_name_generic",
        "formulary_drug_cd",
        "form_unit_disp",
    ]
    df = df.fillna({col: "Not recorded" for col in cols_to_impute})

    # df["enddate"] = df["enddate"].fillna(pd.Timestamp.max)

    df = convert_to_hive_timestamps(df, ["startdate", "enddate"])

    return pa.Table.from_pandas(
        df[SCHEMAS["prescriptions"].names],
        schema=SCHEMAS["prescriptions"],
        preserve_index=False,
    )


def clean_patients(df):
    """Clean PATIENTS table"""
    df["dob"] = pd.to_datetime(df["dob"])
    df["dod"] = pd.to_datetime(df["dod"])

    df = df.drop(columns=["dod_hosp", "dod_ssn"], errors="ignore")
    df["expire_flag"] = df["expire_flag"].astype("boolean")

    df = convert_to_hive_timestamps(df, ["dob", "dod"])

    return pa.Table.from_pandas(
        df[SCHEMAS["patients"].names], schema=SCHEMAS["patients"], preserve_index=False
    )


def clean_admissions(df):
    """Clean ADMISSIONS table"""
    df["admittime"] = pd.to_datetime(df["admittime"])
    df["dischtime"] = pd.to_datetime(df["dischtime"])

    demo_cols = ["language", "religion", "marital_status"]
    df = df.fillna({col: "Not recorded" for col in demo_cols})

    df["hospital_expire_flag"] = df["hospital_expire_flag"].astype("boolean")
    df["has_chartevents_data"] = df["has_chartevents_data"].astype("boolean")

    df = df.drop(columns=["deathtime", "edregtime", "edouttime"], errors="ignore")

    df = convert_to_hive_timestamps(df, ["admittime", "dischtime"])

    return pa.Table.from_pandas(
        df[SCHEMAS["admissions"].names],
        schema=SCHEMAS["admissions"],
        preserve_index=False,
    )


def clean_diagnoses_icd(df):
    """Clean DIAGNOSES_ICD table"""
    df["seq_num"] = df["seq_num"].astype("Int64")

    return pa.Table.from_pandas(
        df[SCHEMAS["diagnoses_icd"].names],
        schema=SCHEMAS["diagnoses_icd"],
        preserve_index=False,
    )
