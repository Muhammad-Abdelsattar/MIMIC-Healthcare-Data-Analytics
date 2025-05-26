USE mimic_dwh;

-- Patients Dimension
CREATE EXTERNAL TABLE patients (
  row_id BIGINT,
  subject_id BIGINT,
  gender STRING,
  dob TIMESTAMP,
  dod TIMESTAMP,
  expire_flag BOOLEAN
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/patients';

-- Admissions Dimension
CREATE EXTERNAL TABLE admissions (
  row_id BIGINT,
  subject_id BIGINT,
  hadm_id BIGINT,
  admittime TIMESTAMP,
  dischtime TIMESTAMP,
  admission_type STRING,
  admission_location STRING,
  discharge_location STRING,
  insurance STRING,
  language STRING,
  religion STRING,
  marital_status STRING,
  ethnicity STRING,
  diagnosis STRING,
  hospital_expire_flag BOOLEAN,
  has_chartevents_data BOOLEAN
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/admissions';

-- Items Dimension (Clinical Events)
CREATE EXTERNAL TABLE d_items (
  row_id BIGINT,
  itemid BIGINT,
  label STRING,
  dbsource STRING,
  linksto STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/d_items';

-- Lab Items Dimension
CREATE EXTERNAL TABLE d_labitems (
  row_id BIGINT,
  itemid BIGINT,
  label STRING,
  fluid STRING,
  category STRING
) STORED AS PARQUET
LOCATION '/user/hive/warehouse/mimic_dwh.db/d_labitems';
