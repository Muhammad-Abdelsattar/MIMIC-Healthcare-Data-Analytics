# User Manual: MIMIC Healthcare Data Analytics Project

## Introduction
This manual guides users through setting up and using the Hadoop simulation project for data processing and analysis. It covers installation, data preparation, running the data pipeline, and interacting with data stored in Hive.

## System Requirements
To successfully install and run this project, your system must meet the following requirements:
- **Docker:** Ensure Docker is installed and running on your system. You can download it from [https://www.docker.com/get-started](https://www.docker.com/get-started).
- **Docker Compose:** Docker Compose is required to orchestrate the multi-container Docker application. Installation instructions can be found at [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).
- **Python 3.x:** Python version 3.x is necessary for executing the data cleaning scripts.
- **pip:** The Python package installer, `pip`, is needed to install Python dependencies. It typically comes bundled with Python 3.x installations.

## Installation and Setup
Follow these steps to get the project environment up and running on your system:

1.  **Clone the Repository:**
    *   Open your terminal or command prompt.
    *   Clone the project repository using Git. Replace `<repository_url>` with the actual URL of the repository:
        ```bash
        git clone https://github.com/yourusername/your-hadoop-project.git
        ```
    *   Navigate into the cloned project directory. Replace `<project_directory_name>` with the actual name of the directory that was created (usually the same as the repository name):
        ```bash
        cd your-hadoop-project
        ```

2.  **Configure Environment Variables (if necessary):**
    *   The project uses environment files located in the `env/` directory (e.g., `core.env`, `hdfs.env`, `hive.env`). For most local simulation purposes, the default configurations provided in these files should work out-of-the-box.
    *   If you need to customize settings (e.g., specific ports, memory allocations, or other Hadoop configurations), you can modify the relevant files within the `env/` directory *before* starting the cluster. Refer to the comments within those files for guidance on what each variable controls.

3.  **Set up Python Environment for Data Cleaning:**
    *   The data cleaning scripts (located in `data_cleaning/`) require Python and specific libraries.
    *   From the project root directory, install the required Python packages using `pip` and the `requirements.txt` file located in `data_cleaning/`:
        ```bash
        pip install -r data_cleaning/requirements.txt
        ```
        This command will download and install all necessary libraries listed in the `data_cleaning/requirements.txt` file.

4.  **Build and Launch the Hadoop/Hive Cluster:**
    *   Ensure Docker Desktop (or Docker Engine if you are on Linux) is running on your system.
    *   From the project root directory (where the `docker-compose.yml` file is located), run the following command. This command will build the Docker images for the services (if they don't exist locally or if the `docker-compose.yml` file has changed) and then start all services in detached mode (`-d`):
        ```bash
        docker-compose up -d --build
        ```
    *   This process might take some time, especially on the first run, as Docker needs to download the base images specified in the `docker-compose.yml` file and build the project-specific images. Subsequent runs will be faster.

5.  **Verify Cluster Installation:**
    *   Once the `docker-compose up -d --build` command completes and your terminal returns to the prompt, you can check if all containers are running correctly:
        ```bash
        docker-compose ps
        ```
    *   You should see a list of all services defined in the `docker-compose.yml` file (e.g., `namenode`, `datanode`, `resourcemanager`, `nodemanager`, `hive-server`, `hive-metastore`, `postgres-metastore`). Their 'State' should be 'Up' or 'running' (the exact wording might vary slightly depending on your Docker version).
    *   You can also access the web UIs of some Hadoop services to further verify that they are operational. Open the following links in your web browser:
        *   Hadoop NameNode UI: [http://localhost:9870](http://localhost:9870) - Shows HDFS status.
        *   YARN ResourceManager UI: [http://localhost:8088](http://localhost:8088) - Shows cluster resource usage and application status.
    *   If you encounter any issues during this process, or if services are not starting correctly, refer to the 'Troubleshooting' section of this manual for common problems and solutions.

## Data Preparation
This section explains how to prepare your raw data files for processing by the data cleaning pipeline.

1.  **Create the Input Directory:**
    *   The data cleaning pipeline expects raw CSV files to be located in a specific directory within the project structure.
    *   In the root directory of the project, create a folder named `data` if it doesn't already exist. You can do this using the following command in your terminal:
        ```bash
        mkdir -p data
        ```
        (The `-p` flag ensures that the command creates parent directories if they are needed and does not return an error if the `data` directory already exists.)

2.  **Place CSV Files:**
    *   Copy your raw CSV data files into the newly created `data/` directory.
    *   The data cleaning script (`data_cleaning/main.py`) is configured to look for specific filenames for each table it processes. You need to ensure your CSV filenames match these expectations.
    *   The expected filenames are defined in `data_cleaning/config.py` within the `TABLE_FILE_MAP` dictionary. For example, the 'patients' table might expect a file named `PATIENTS.CSV`.
    *   Please consult the `TABLE_FILE_MAP` in `data_cleaning/config.py` and ensure your files in the `data/` directory are named accordingly.
    *   **Example (illustrative, actual values depend on `config.py`):**
        *   `data/PATIENTS.CSV`
        *   `data/ADMISSIONS.CSV`
        *   `data/CHARTEVENTS.CSV`
        *   ...and so on for all tables listed in the `TABLES_TO_PROCESS` variable (also in `config.py`).

3.  **File Encoding and Format:**
    *   Ensure your CSV files are in a standard format (e.g., comma-separated values) and use a common encoding like UTF-8.
    *   The cleaning scripts use pandas `read_csv`, which can handle many variations, but adhering to standards will prevent issues.

## Running the Data Cleaning Pipeline
This section details how to execute the Python-based data cleaning pipeline.

1.  **Prerequisites:**
    *   Ensure you have completed the 'Installation and Setup' steps, particularly setting up the Python environment by running `pip install -r data_cleaning/requirements.txt` from the project root.
    *   Ensure your raw CSV data is correctly placed and named in the `data/` directory (located at the project root) as described in the 'Data Preparation' section.

2.  **Execute the Main Cleaning Script:**
    *   Open your terminal or command prompt.
    *   From the project root directory, run the main Python script to start the cleaning process for all configured tables:
        ```bash
        python data_cleaning/main.py
        ```
    *   The script will process each CSV file specified in its configuration (from `data_cleaning/config.py`), perform various cleaning and transformation operations, and save the output as Parquet files.
    *   You will see log messages in the console indicating the progress of the script (e.g., which table is being processed) and any potential errors or warnings.

3.  **Verify Output:**
    *   Once the `data_cleaning/main.py` script finishes execution, the cleaned data will be stored in Parquet format.
    *   The output files are located inside the `processed_data/` directory, which is created at the project root.
    *   Check the contents of the `processed_data/` directory. You should find subdirectories for each table that was processed (e.g., `processed_data/patients/`, `processed_data/admissions/`). Inside each of these subdirectories, there will be a Parquet file (e.g., `patients.parquet`).
    *   You can list the contents to verify (optional):
        *   For Linux/macOS:
            ```bash
            ls -R processed_data
            ```
        *   For Windows:
            ```bash
            dir /s processed_data
            ```

5.  **Troubleshooting Script Execution:**
    *   If the script fails or encounters errors, carefully check the error messages displayed in the console. Common issues include:
        *   **Missing or incorrectly named input CSV files:** The script might not find the files it expects in the `data/` directory. Double-check the filenames against the `data_cleaning/config.py` specifications and ensure the files are present in `data/`.
        *   **Python package dependencies:** One or more required Python libraries might be missing or not installed correctly. Ensure that `pip install -r requirements.txt` (run from the `data_cleaning` directory) completed without errors.
        *   **CSV file content issues:** There might be problems with the actual content of your CSV files, such as unexpected formatting that the script cannot handle by default, or encoding issues if the files are not UTF-8.
    *   Review the script's log output and any error messages for specific clues about what went wrong.

## Loading Data into Hive
This section guides you through loading your processed Parquet data into HDFS and then creating the corresponding Hive tables.

### 1. Prerequisites
*   Ensure the Hadoop/Hive cluster is running. You can verify this by running `docker-compose ps` in your terminal from the project root. All services should be listed with a state like 'Up' or 'running'.
*   Ensure you have successfully run the data cleaning pipeline as described in "Running the Data Cleaning Pipeline." The processed Parquet files should be available in the `processed_data/` directory at the project root.

### 2. Transfer Processed Data to HDFS
The Hive tables will be configured to read data from HDFS. The following steps describe how to copy your processed Parquet files (assumed to be in `./processed_data/` with subdirectories for each table, e.g., `./processed_data/patients/patients.parquet`) into the HDFS running inside the Docker containers.

**a. Create the main HDFS database directory:**
   This command creates the base directory in HDFS where your Hive database (e.g., `mimic_dwh`) will store its tables.
   ```bash
   docker exec namenode hdfs dfs -mkdir -p /user/hive/warehouse/mimic_dwh.db
   ```

**b. Copy the entire `processed_data` directory to the NameNode container:**
   This copies all your processed table subdirectories and Parquet files to a temporary location within the NameNode container's filesystem.
   ```bash
   docker cp ./processed_data namenode:/tmp/
   ```

**c. Put all table data from the NameNode's temporary location into HDFS:**
   This command takes all the subdirectories (each representing a table) from `/tmp/processed_data/` inside the NameNode container and puts them into the HDFS database directory created in step (a). Hive tables will then be configured to read from these HDFS subdirectories (e.g., `/user/hive/warehouse/mimic_dwh.db/patients/`, `/user/hive/warehouse/mimic_dwh.db/admissions/`).
   ```bash
   docker exec namenode hdfs dfs -put /tmp/processed_data/* /user/hive/warehouse/mimic_dwh.db/
   ```

**d. (Optional but recommended) Remove the temporary directory from the NameNode container:**
   This helps free up space in the NameNode container's local filesystem.
   ```bash
   docker exec namenode rm -r /tmp/processed_data
   ```
**Important Note:** This HDFS loading strategy assumes that your Hive `CREATE EXTERNAL TABLE` statements (in your HQL scripts) will specify the `LOCATION` for each table as a subdirectory within `/user/hive/warehouse/mimic_dwh.db/`. For example, the `patients` table should have its `LOCATION` set to `/user/hive/warehouse/mimic_dwh.db/patients/`.

### 3. Run HQL Scripts to Define Hive Schema and Tables
Once your data is in HDFS, you need to run HQL scripts to create the database and table definitions in Hive. These definitions tell Hive where to find the data in HDFS and how to interpret it.

**a. Copy HQL Scripts to Hive Server Container:**
   The HQL scripts are in the `hive-hql/` directory on your local machine. If you haven't already or if they have changed, copy them into the `hive-server` container:
   ```bash
   docker cp ./hive-hql hive-server:/tmp/
   ```

**b. Execute HQL Scripts:**
   Execute each HQL script using the `hive -f` command via `docker exec` from your host machine's terminal. This command executes the HQL statements within the specified file.
   ```bash
   docker exec hive-server hive -f /tmp/hive-hql/create_dwh.sql
   docker exec hive-server hive -f /tmp/hive-hql/create_dim_tables.sql
   docker exec hive-server hive -f /tmp/hive-hql/create_fact_tables.sql
   ```
   Verify that the scripts ran without error messages in your terminal. These scripts will create the database, define the table schemas, and point to the HDFS locations where you loaded the Parquet files.

Your data should now be loaded into HDFS and accessible via Hive queries.

## Accessing Data in Hive
This section explains how to connect to the Hive Command Line Interface (CLI) and run basic queries to explore your data.

1.  **Connect to Hive CLI:**
    *   To interactively query your data, connect to the Hive Command Line Interface (CLI) by running the following command in your terminal:
        ```bash
        docker exec -it hive-server hive
        ```
    *   This command starts an interactive session within the `hive-server` container, placing you at the Hive CLI prompt (e.g., `hive>`).

2.  **Basic Hive Commands:**
    *   Once connected to the Hive CLI, you can issue HiveQL queries. Here are some basic commands to get started:
    *   Replace `<database_name>` (e.g., `mimic_dwh`) and `<table_name>` with your actual database and table names.

    *   **Show Databases:**
        ```sql
        SHOW DATABASES;
        ```

    *   **Use Your Database:**
        ```sql
        USE <database_name>;
        ```
        **Example:**
        ```sql
        USE mimic_dwh;
        ```

    *   **Show Tables in the Current Database:**
        ```sql
        SHOW TABLES;
        ```

    *   **Describe a Table (to see its schema):**
        ```sql
        DESCRIBE FORMATTED <table_name>;
        ```
        **Example:**
        ```sql
        DESCRIBE FORMATTED patients;
        ```

    *   **Count Rows in a Table:**
        ```sql
        SELECT COUNT(*) FROM <table_name>;
        ```
        **Example:**
        ```sql
        SELECT COUNT(*) FROM patients;
        ```

    *   **View Sample Data from a Table:**
        ```sql
        SELECT * FROM <table_name> LIMIT 10;
        ```
        **Example:**
        ```sql
        SELECT * FROM patients LIMIT 10;
        ```

3.  **Running More Complex Queries:**
    *   You can run any valid HiveQL query to analyze your data. For example, if you have `admissions` and `patients` tables:
        ```sql
        SELECT p.subject_id, p.gender, a.admission_type, a.diagnosis
        FROM patients p
        JOIN admissions a ON p.subject_id = a.subject_id
        LIMIT 20;
        ```
    *   Refer to the HiveQL language manual for more advanced querying capabilities.

4.  **Exiting Hive CLI:**
    *   When you are finished querying, type `exit;` or `quit;` and press Enter to leave the Hive CLI.

## Troubleshooting
This section lists common problems users might encounter and provides guidance on how to diagnose and resolve them.

### 1. Docker and Docker Compose Issues

*   **Problem:** `docker-compose up` fails or containers don't start.
    *   **Diagnosis:**
        *   Check if Docker Desktop (or Docker Engine) is running.
        *   Run `docker-compose ps` to see the current state of all containers.
        *   Check the logs for specific services that are failing or not starting: `docker-compose logs <service_name>` (e.g., `docker-compose logs namenode`, `docker-compose logs hive-server`). Look for error messages.
        *   Ensure that no other processes on your host machine are using the network ports defined in the `docker-compose.yml` file (e.g., 9870 for NameNode, 8088 for YARN ResourceManager, 10000 for HiveServer2).
    *   **Solution:**
        *   Ensure your system has sufficient resources (RAM, disk space) allocated to Docker.
        *   Try a clean restart of the services: `docker-compose down` followed by `docker-compose up -d --build`. The `--build` flag will ensure images are rebuilt if necessary.
        *   If you've recently modified the `docker-compose.yml` file, double-check its syntax for errors.

*   **Problem:** "Port already allocated" or "Bind for 0.0.0.0:XXXX failed: port is already allocated."
    *   **Diagnosis:** Another application or service on your host machine is using a network port that one of the Docker containers needs.
    *   **Solution:**
        *   Identify the conflicting service on your host that is using the specified port (e.g., using `netstat -tulnp | grep XXXX` on Linux/macOS, or `resmon.exe` on Windows) and stop it if possible.
        *   Alternatively, modify the port mapping in the `docker-compose.yml` file. For example, if port `10000` is in use, change `ports: ["10000:10000"]` for the `hive-server` service to something like `ports: ["10001:10000"]`. If you do this, remember to use the new host port (e.g., `10001`) when connecting from your local machine (e.g., Beeline URL `jdbc:hive2://localhost:10001`).
        *   After modifying `docker-compose.yml`, run `docker-compose up -d --build` to apply the changes.

### 2. Data Cleaning Script (`data_cleaning/main.py`) Issues

*   **Problem:** Script fails with `FileNotFoundError`.
    *   **Diagnosis:** The Python script cannot locate the input CSV files it expects.
    *   **Solution:**
        *   Ensure you are running the `python main.py` command from *within* the `data_cleaning/` directory.
        *   Verify that the `data/` directory exists at the project root level (i.e., `your-hadoop-project/data/`).
        *   Double-check that your raw CSV files are placed directly inside the `data/` directory.
        *   Crucially, ensure the filenames of your CSVs *exactly* match the keys defined in the `TABLE_FILE_MAP` dictionary within `data_cleaning/config.py`. This includes capitalization, as filenames can be case-sensitive.

*   **Problem:** Script fails with `ModuleNotFoundError` or `ImportError`.
    *   **Diagnosis:** Required Python libraries (dependencies) are not installed in the Python environment you are using.
    *   **Solution:**
        *   Make sure you have successfully run `pip install -r requirements.txt` from *within* the `data_cleaning/` directory. Check that this command completed without any errors.
        *   If you are using Python virtual environments (e.g., venv, conda), ensure the correct virtual environment is activated before running the script.

*   **Problem:** Script runs but produces errors related to data types (e.g., `ValueError: could not convert string to float`) or specific CSV content.
    *   **Diagnosis:** The content of your CSV files might have unexpected formats, special characters, incorrect delimiters, unusual encoding, or values that the cleaning functions in `cleaning.py` are not designed to handle.
    *   **Solution:**
        *   Examine the error message closely. It usually indicates the problematic file, column, and sometimes the value causing the issue.
        *   Inspect the relevant CSV file, particularly around the area indicated by the error.
        *   You might need to manually clean the problematic parts of the CSV file or, if the issue is systematic across many files or rows, adjust the Python cleaning functions in `data_cleaning/cleaning.py` to handle such cases more robustly.

### 3. HDFS and Data Loading Issues

*   **Problem:** `hdfs dfs` commands fail (e.g., `docker exec namenode hdfs dfs -ls /` results in "Connection refused" or similar).
    *   **Diagnosis:** The HDFS NameNode or DataNode containers might not be running correctly, or there's a network configuration issue within the Docker environment preventing communication.
    *   **Solution:**
        *   Verify that the `namenode` and `datanode` containers are running using `docker-compose ps`.
        *   Check the logs for these containers: `docker-compose logs namenode` and `docker-compose logs datanode`. Look for startup errors or repeated error messages.
        *   Ensure that the `CORE_CONF_fs_defaultFS` environment variable in `docker-compose.yml` for Hadoop services is correctly set to `hdfs://namenode:9000`.

*   **Problem:** Cannot put files into HDFS, or files are copied but are not visible/usable in Hive tables.
    *   **Diagnosis:** HDFS paths might be incorrect, HDFS directories might not exist, or there could be a mismatch between the HDFS path where data is loaded and the `LOCATION` specified in Hive table definitions.
    *   **Solution:**
        *   Double-check the full HDFS paths used in your `hdfs dfs -mkdir -p ...` and `hdfs dfs -put ...` commands.
        *   Ensure these HDFS paths *exactly* match the paths specified in the `LOCATION` clause of your `CREATE EXTERNAL TABLE` statements in your HQL files (e.g., `hive-hql/create_dim_tables.sql`, `hive-hql/create_fact_tables.sql`).
        *   Confirm that you have created the HDFS parent directories for your tables (e.g., `/user/hive/warehouse/mimic_dwh.db/patients/`) *before* trying to put files into them.

### 4. Hive/Beeline Issues

*   **Problem:** Cannot connect to HiveServer2 with Beeline (e.g., "Connection refused" when using `jdbc:hive2://localhost:10000`).
    *   **Diagnosis:** The `hive-server` container is not running, not accessible on the expected port, or the `hive-metastore` (and its backend database, e.g., `postgres-metastore`) is having issues.
    *   **Solution:**
        *   Verify that the `hive-server`, `hive-metastore`, and `postgres-metastore` (or your specific metastore DB container) are all running using `docker-compose ps`.
        *   Check the logs for these services: `docker-compose logs hive-server`, `docker-compose logs hive-metastore`, and `docker-compose logs postgres-metastore`.
        *   Ensure that the Beeline connection string `jdbc:hive2://localhost:10000` is correct and that port `10000` is correctly mapped to the host in the `ports` section of the `hive-server` service in `docker-compose.yml`.

*   **Problem:** HQL scripts (`.sql` files) fail to execute in Beeline, or tables are not created/populated as expected.
    *   **Diagnosis:** Potential syntax errors in your HQL scripts, incorrect HDFS paths in `LOCATION` clauses, or issues with data compatibility with the defined table schema.
    *   **Solution:**
        *   Carefully read the error messages provided by Beeline. They often pinpoint the exact HQL statement and type of error.
        *   Verify the HQL syntax for your `CREATE DATABASE`, `CREATE EXTERNAL TABLE`, etc., statements.
        *   Ensure that the HDFS paths specified in `CREATE EXTERNAL TABLE ... LOCATION '...'` clauses are absolutely correct and point to the HDFS directories where your Parquet files reside.
        *   If you are creating managed tables and loading data (e.g., `LOAD DATA INPATH ...`), ensure the data format (e.g., Parquet) and schema align with the table definition.

*   **Problem:** Hive queries run very slowly or fail with resource-related errors.
    *   **Diagnosis:** Could be insufficient resources allocated to Docker, inefficiently written queries, or missing table statistics for query optimization.
    *   **Solution:**
        *   Ensure Docker has been allocated sufficient resources (RAM, CPU) in Docker Desktop settings.
        *   Analyze your HiveQL queries for potential optimizations (e.g., filter pushdown, proper join conditions).
        *   For larger datasets, consider generating table and column statistics, which can help the Hive optimizer create better execution plans:
            ```sql
            USE <your_database_name>;
            ANALYZE TABLE <your_table_name> COMPUTE STATISTICS;
            ANALYZE TABLE <your_table_name> COMPUTE STATISTICS FOR COLUMNS;
            ```

### 5. General Advice

*   **Check the Logs:** When in doubt, the first step is almost always to check the logs for the relevant service. Use the command: `docker-compose logs <service_name>`. For example, if `namenode` seems to be an issue, run `docker-compose logs namenode`.
*   **Restart Services:** Restarting the Docker containers can sometimes resolve transient issues or apply configuration changes. Use: `docker-compose down && docker-compose up -d --build`.

## Shutting Down the Cluster
This section explains how to stop and remove the Docker containers for the Hadoop/Hive cluster.

1.  **Command to Stop and Remove Containers:**
    *   When you are finished working with the Hadoop/Hive cluster and want to stop all associated Docker containers, navigate to the project root directory in your terminal (the directory where your `docker-compose.yml` file is located).
    *   Run the following command:
        ```bash
        docker-compose down
        ```

2.  **Explanation of the Command:**
    *   This command stops and removes the containers, networks, and default (anonymous) volumes defined in your `docker-compose.yml` file.
    *   If you defined named volumes in your `docker-compose.yml` (like `hadoop_namenode`, `hadoop_datanode`, `postgres_metastore_data`, etc.) and want to remove them as well (which will delete their persisted data, like HDFS data and the Hive metastore database), you can use:
        ```bash
        docker-compose down -v
        ```
    *   **Caution:** Be very cautious with `docker-compose down -v` as it will delete any data stored in the named volumes. This includes:
        *   All data in your HDFS (files you've put into the simulated Hadoop file system).
        *   All metadata in your Hive Metastore (table definitions, database schemas, etc., stored in the PostgreSQL backend).
        If you want to keep this data for future sessions, use `docker-compose down` without the `-v` flag. The containers will be removed, but the data in named volumes will persist and will be available when you next run `docker-compose up`.
