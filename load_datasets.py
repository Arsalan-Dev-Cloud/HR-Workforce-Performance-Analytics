import pandas as pd

# Load employee information
emp_info = pd.read_csv(
    "data/raw/emp_info.csv"
)

# Load employee salary information
emp_salaries = pd.read_csv(
    "data/raw/emp_salary.csv"
)

# Load department information
department = pd.read_csv(
    "data/raw/department.csv"
)

# Load job role information
job_roles = pd.read_csv(
    "data/raw/job_roles.csv"
)

print("All four datasets loaded successfully!")

# Display first five rows of each dataset
print("\nEMPLOYEE INFORMATION:")
print(emp_info.head())

print("\nEMPLOYEE SALARIES:")
print(emp_salaries.head())

print("\nDEPARTMENT INFORMATION:")
print(department.head())

print("\nJOB ROLES:")
print(job_roles.head())

print("\n========== DATASET SHAPES ==========")

print("Employee Information:", emp_info.shape)
print("Employee Salaries:", emp_salaries.shape)
print("Departments:", department.shape)
print("Job Roles:", job_roles.shape)


print("\n========== DATASET COLUMNS ==========")

print("\nEmployee Information Columns:")
print(emp_info.columns)

print("\nEmployee Salaries Columns:")
print(emp_salaries.columns)

print("\nDepartment Columns:")
print(department.columns)

print("\nJob Roles Columns:")
print(job_roles.columns)

print("\n========== EMPLOYEE INFORMATION DATA TYPES ==========")
print(emp_info.dtypes)

print("\n========== EMPLOYEE SALARIES DATA TYPES ==========")
print(emp_salaries.dtypes)

print("\n========== DEPARTMENT DATA TYPES ==========")
print(department.dtypes)

print("\n========== JOB ROLES DATA TYPES ==========")
print(job_roles.dtypes)

print("\n========== MISSING VALUES ==========")

print("\nEmployee Information:")
print(emp_info.isnull().sum())

print("\nEmployee Salaries:")
print(emp_salaries.isnull().sum())

print("\nDepartments:")
print(department.isnull().sum())

print("\nJob Roles:")
print(job_roles.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")

print("\nEmployee Information:")
print(emp_info.duplicated().sum())

print("\nEmployee Salaries:")
print(emp_salaries.duplicated().sum())

print("\nDepartments:")
print(department.duplicated().sum())

print("\nJob Roles:")
print(job_roles.duplicated().sum())


# ==========================================
# PHASE 1: COMPLETE DATA QUALITY CHECKS
# ==========================================

print("\n========== 1. MISSING VALUES ==========")

datasets = {
    "Employee Information": emp_info,
    "Employee Salaries": emp_salaries,
    "Departments": department,
    "Job Roles": job_roles
}

for name, df in datasets.items():
    print(f"\n{name}:")
    print(df.isnull().sum())


print("\n========== 2. DUPLICATE ROWS ==========")

for name, df in datasets.items():
    print(f"{name}: {df.duplicated().sum()}")


print("\n========== 3. DUPLICATE IDENTIFIERS ==========")

print("Employee IDs in employee information:",
      emp_info["emp_id"].duplicated().sum())

print("Employee IDs in employee salaries:",
      emp_salaries["emp_id"].duplicated().sum())

print("Department IDs:",
      department["dept_id"].duplicated().sum())

print("Job Role IDs:",
      job_roles["role_id"].duplicated().sum())


print("\n========== 4. UNIQUE IDENTIFIER COUNTS ==========")

print("Unique employees:", emp_info["emp_id"].nunique())
print("Unique salary employee IDs:", emp_salaries["emp_id"].nunique())
print("Unique departments:", department["dept_id"].nunique())
print("Unique job roles:", job_roles["role_id"].nunique())


print("\n========== 5. INVALID DEPARTMENT REFERENCES ==========")

invalid_dept = emp_salaries[
    ~emp_salaries["dept_id"].isin(department["dept_id"])
]

print("Invalid department references:", len(invalid_dept))


print("\n========== 6. INVALID JOB ROLE REFERENCES ==========")

invalid_roles = emp_salaries[
    ~emp_salaries["role_id"].isin(job_roles["role_id"])
]

print("Invalid job role references:", len(invalid_roles))


print("\n========== 7. EMPLOYEE ID MATCHING ==========")

employees_without_salary = emp_info[
    ~emp_info["emp_id"].isin(emp_salaries["emp_id"])
]

salary_without_employee = emp_salaries[
    ~emp_salaries["emp_id"].isin(emp_info["emp_id"])
]

print("Employees without salary records:", len(employees_without_salary))
print("Salary records without employee records:", len(salary_without_employee))


print("\n========== 8. INVALID NUMERIC VALUES ==========")

print("Experience below zero:",
      (emp_salaries["year_of_exp"] < 0).sum())

print("Basic salary zero or below:",
      (emp_salaries["basic_salary"] <= 0).sum())

print("Negative PF deductions:",
      (emp_salaries["pf_deduction"] < 0).sum())

print("Negative ESI deductions:",
      (emp_salaries["esi_deduction"] < 0).sum())

print("Negative performance bonuses:",
      (emp_salaries["performance_bonus"] < 0).sum())

print("Performance rating outside 0-5:",
      (~emp_salaries["performace_rating"].between(0, 5)).sum())


print("\n========== 9. DATE VALIDATION ==========")

dob_dates = pd.to_datetime(
    emp_info["dob"],
    format="%d-%m-%Y",
    errors="coerce"
)

hire_dates = pd.to_datetime(
    emp_info["hire_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("Invalid date of birth:", dob_dates.isna().sum())
print("Invalid hire dates:", hire_dates.isna().sum())

print("Hire dates before date of birth:",
      (hire_dates < dob_dates).sum())


print("\n========== 10. ACTIVE EMPLOYEE SUMMARY ==========")

print(emp_info["is_active"].value_counts(dropna=False))


print("\n========== DATA QUALITY CHECKS COMPLETED ==========")
