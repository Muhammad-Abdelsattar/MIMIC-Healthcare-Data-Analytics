import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import logging
from processing import *
from config import TABLE_FILE_MAP, PARQUET_CONFIG, TABLES_TO_PROCESS

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function to process all tables and convert them to Parquet format."""
    data_path = Path("./data")
    output_path = Path("./output")
    output_path.mkdir(parents=True, exist_ok=True)

    processor_map = {
        "patients": clean_patients,
        "admissions": clean_admissions,
        "chartevents": clean_chartevents,
        "labevents": clean_labevents,
        "prescriptions": clean_prescriptions,
        "diagnoses_icd": clean_diagnoses_icd,
        "d_items": clean_d_items,
        "d_labitems": clean_d_labitems,
    }

    for table in TABLES_TO_PROCESS:
        try:
            logger.info(f"Processing {table}...")

            csv_path = data_path / TABLE_FILE_MAP[table]
            df = pd.read_csv(csv_path, low_memory=False)

            processor_func = processor_map[table]
            arrow_table = processor_func(df)

            output_file = output_path / f"{table}" / f"{table}.parquet"
            (output_path / f"{table}").mkdir(parents=True, exist_ok=True)

            pq.write_table(arrow_table, output_file, **PARQUET_CONFIG)

            logger.info(f"Successfully processed {table} and saved to {output_file}")

        except Exception as e:
            logger.error(f"Error processing {table}: {str(e)}")


if __name__ == "__main__":
    main()
