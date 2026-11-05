import pandas as pd
from pathlib import Path

# ==========================================
# PHASE 2: DATA CLEANING
# PHASE 3: DATA INTEGRATION
# ==========================================

print("\n========== LOADING RAW DATASETS ==========")

# Project directories
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create processed folder if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
emp_info = pd.read_csv(RAW_DIR / "emp_info.csv")
emp_salary = pd.read_csv(RAW_DIR / "emp_salary.csv")
department = pd.read_csv(RAW_DIR / "department.csv")
job_roles = pd.read_csv(RAW_DIR / "job_roles.csv")

print("All datasets loaded successfully!")


# ==========================================
# 1. STANDARDISE COLUMN NAMES
# ==========================================

print("\n========== STANDARDISING COLUMN NAMES ==========")

datasets = [emp_info, emp_salary, department, job_roles]

for df in datasets:
    df.columns = df.columns.str.strip().str.lower()

# Correct the spelling in the salary dataset
emp_salary.rename(
    columns={"performace_rating": "performance_rating"},
    inplace=True
)

print("Column names standardised successfully!")


# ==========================================
# 2. CLEAN TEXT VALUES
# ==========================================

print("\n========== CLEANING TEXT VALUES ==========")

for df in datasets:
    text_columns = df.select_dtypes(include=["object", "str"]).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

print("Text values cleaned successfully!")


# ==========================================
# 3. CONVERT DATE COLUMNS
# ==========================================

print("\n========== CONVERTING DATE COLUMNS ==========")

emp_info["dob"] = pd.to_datetime(
    emp_info["dob"],
    format="%d-%m-%Y",
    errors="coerce"
)

emp_info["hire_date"] = pd.to_datetime(
    emp_info["hire_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

if emp_info[["dob", "hire_date"]].isna().any().any():
    raise ValueError("Invalid dates found during date conversion.")

print("Date columns converted successfully!")


# ==========================================
# 4. VALIDATE PRIMARY KEYS
# ==========================================

print("\n========== VALIDATING IDENTIFIERS ==========")

if emp_info["emp_id"].duplicated().any():
    raise ValueError("Duplicate employee IDs found.")

if emp_salary["emp_id"].duplicated().any():
    raise ValueError("Duplicate employee IDs in salary dataset.")

if department["dept_id"].duplicated().any():
    raise ValueError("Duplicate department IDs found.")

if job_roles["role_id"].duplicated().any():
    raise ValueError("Duplicate job role IDs found.")

print("All primary identifiers are unique!")


# ==========================================
# PHASE 3: DATA INTEGRATION
# ==========================================

print("\n========== MERGING DATASETS ==========")

# Merge employee information with salary data
hr_data = pd.merge(
    emp_info,
    emp_salary,
    on="emp_id",
    how="inner",
    validate="one_to_one"
)

# Add department information
hr_data = pd.merge(
    hr_data,
    department,
    on="dept_id",
    how="left",
    validate="many_to_one"
)

# Add job role information
hr_data = pd.merge(
    hr_data,
    job_roles,
    on="role_id",
    how="left",
    validate="many_to_one"
)

print("All four datasets merged successfully!")


# ==========================================
# 5. VALIDATE MERGED DATA
# ==========================================

print("\n========== VALIDATING MERGED DATA ==========")

print("Total integrated employee records:", len(hr_data))

if len(hr_data) != len(emp_info):
    raise ValueError("Employee records were lost during merging.")

if hr_data[["dept_name", "position"]].isna().any().any():
    raise ValueError("Missing department or job role information after merging.")

print("Merged dataset validation successful!")


# ==========================================
# 6. FEATURE ENGINEERING
# ==========================================

print("\n========== CREATING NEW HR FEATURES ==========")

# Combine first and last names
hr_data["full_name"] = (
    hr_data["first_name"] + " " + hr_data["last_name"]
)

# Calculate employee age
today = pd.Timestamp.today().normalize()

hr_data["age"] = (
    (today - hr_data["dob"]).dt.days / 365.2425
).floordiv(1).astype("int64")

# Calculate years of service
hr_data["years_of_service"] = (
    (today - hr_data["hire_date"]).dt.days / 365.2425
).floordiv(1).astype("int64")

print("Full name, age and years of service created!")


# ==========================================
# 7. SALARY CALCULATION VALIDATION
# ==========================================

print("\n========== VALIDATING GROSS SALARY ==========")

# Check the apparent salary formula using the source columns.
# Do not overwrite the original gross_salary column.

calculated_gross = (
    hr_data["basic_salary"]
    - hr_data["pf_deduction"]
    - hr_data["esi_deduction"]
    + hr_data["performance_bonus"]
)

salary_mismatches = (
    calculated_gross - hr_data["gross_salary"]
).abs().gt(0.01)

print("Gross salary calculation mismatches:", salary_mismatches.sum())


# ==========================================
# 8. FINAL DATA QUALITY CHECK
# ==========================================

print("\n========== FINAL DATA QUALITY ==========")

print("Final dataset shape:", hr_data.shape)

print("\nMissing values:")
print(hr_data.isnull().sum().sum())

print("\nDuplicate rows:", hr_data.duplicated().sum())

print("\nFinal columns:")
print(hr_data.columns.tolist())


# ==========================================
# 9. SAVE PROCESSED DATASET
# ==========================================

OUTPUT_FILE = PROCESSED_DIR / "cleaned_hr_workforce.csv"

hr_data.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== PROJECT OUTPUT ==========")

print("Cleaned dataset saved successfully!")
print("Output location:", OUTPUT_FILE)

print("\n========== PHASE 2 AND PHASE 3 COMPLETED ==========")