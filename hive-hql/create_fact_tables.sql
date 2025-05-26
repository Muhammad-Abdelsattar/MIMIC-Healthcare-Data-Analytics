-- Chart Events Fact Table
CREATE EXTERNAL TABLE chartevents (
  row_id BIGINT,
  subject_id BIGINT,
  hadm_id BIGINT,
  icustay_id BIGINT,
  itemid BIGINT,
  charttime TIMESTAMP,
  cgid BIGINT,
  value_merged STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/chartevents';

-- Lab Events Fact Table
CREATE EXTERNAL TABLE labevents (
  row_id BIGINT,
  subject_id BIGINT,
  hadm_id BIGINT,
  itemid BIGINT,
  charttime TIMESTAMP,
  flag STRING,
  value_merged STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/labevents';

-- Prescriptions Fact Table
CREATE EXTERNAL TABLE prescriptions (
  row_id BIGINT,
  subject_id BIGINT,
  hadm_id BIGINT,
  icustay_id BIGINT,
  startdate TIMESTAMP,
  enddate TIMESTAMP,
  drug_type STRING,
  drug STRING,
  drug_name_poe STRING,
  drug_name_generic STRING,
  formulary_drug_cd STRING,
  gsn BIGINT,
  ndc BIGINT,
  prod_strength STRING,
  dose_val_rx STRING,
  dose_unit_rx STRING,
  form_val_disp STRING,
  form_unit_disp STRING,
  route STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/prescriptions';

-- Diagnoses Fact Table
CREATE EXTERNAL TABLE diagnoses_icd (
  row_id BIGINT,
  subject_id BIGINT,
  hadm_id BIGINT,
  seq_num BIGINT,
  icd9_code STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/diagnoses_icd';
