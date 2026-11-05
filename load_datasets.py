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