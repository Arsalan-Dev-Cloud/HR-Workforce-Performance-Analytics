
import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"


# ==========================================
# 2. LOAD CSV DATASETS
# ==========================================

print("\n========== LOADING CSV DATASETS ==========")

departments = pd.read_csv(RAW_DIR / "department.csv")
job_roles = pd.read_csv(RAW_DIR / "job_roles.csv")
employees = pd.read_csv(RAW_DIR / "emp_info.csv")
salaries = pd.read_csv(RAW_DIR / "emp_salary.csv")

print("All four datasets loaded successfully!")


# ==========================================
# 3. CLEAN AND PREPARE DATA
# ==========================================

print("\n========== PREPARING DATA ==========")

# Correct the original dataset's column-name typo
salaries.rename(
    columns={"performace_rating": "performance_rating"},
    inplace=True
)

# Convert dates from DD-MM-YYYY to proper dates
employees["dob"] = pd.to_datetime(
    employees["dob"],
    format="%d-%m-%Y",
    errors="raise"
)

employees["hire_date"] = pd.to_datetime(
    employees["hire_date"],
    format="%d-%m-%Y",
    errors="raise"
)

# Ensure active status is stored as boolean
employees["is_active"] = employees["is_active"].astype(bool)

# Confirm that identifiers are unique
assert employees["emp_id"].is_unique, "Duplicate employee IDs found!"
assert salaries["emp_id"].is_unique, "Duplicate salary employee IDs found!"
assert departments["dept_id"].is_unique, "Duplicate department IDs found!"
assert job_roles["role_id"].is_unique, "Duplicate job role IDs found!"

# Confirm employee and salary IDs match
assert set(employees["emp_id"]) == set(salaries["emp_id"]), (
    "Employee IDs and salary IDs do not match!"
)

print("Data preparation and validation completed!")


# ==========================================
# 4. DATABASE CONNECTION
# ==========================================

print("\n========== MYSQL CONNECTION ==========")

password = getpass.getpass("Enter MySQL root password: ")

database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="hr_workforce_analytics"
)

engine = create_engine(database_url)

# ==========================================
# 5. IMPORT DATA INTO MYSQL
# ==========================================

print("\n========== IMPORTING DATA INTO MYSQL ==========")

table_data = {
    "departments": departments,
    "job_roles": job_roles,
    "employees": employees,
    "salaries": salaries
}

try:
    with engine.begin() as connection:

        # Prevent accidental duplicate imports
        for table_name in table_data:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table_name}`")
            ).scalar_one()

            if count > 0:
                raise RuntimeError(
                    f"Table '{table_name}' already contains {count} records. "
                    "Import cancelled to prevent duplicate data."
                )

        # Import in foreign-key dependency order
        for table_name, dataframe in table_data.items():

            dataframe.to_sql(
                name=table_name,
                con=connection,
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi"
            )

            print(
                f"{table_name}: {len(dataframe)} records imported!"
            )

    print("\nAll datasets imported successfully!")

except Exception as error:
    print("\nIMPORT FAILED!")
    print("Error:", error)
    raise

finally:
    engine.dispose()


# ==========================================
# 6. FINAL IMPORT SUMMARY
# ==========================================

print("\n========== IMPORT SUMMARY ==========")

verification_engine = create_engine(database_url)

with verification_engine.connect() as connection:

    for table_name in table_data:

        count = connection.execute(
            text(f"SELECT COUNT(*) FROM `{table_name}`")
        ).scalar_one()

        print(f"{table_name}: {count} records")

verification_engine.dispose()

print("\nMySQL data integration completed successfully!")
