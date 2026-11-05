
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# PHASE 4: EXPLORATORY DATA ANALYSIS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_hr_workforce.csv"
IMAGE_DIR = BASE_DIR / "images"
REPORT_DIR = BASE_DIR / "reports"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load integrated dataset
df = pd.read_csv(DATA_FILE, parse_dates=["dob", "hire_date"])

sns.set_theme(style="whitegrid")

print("\n========== HR WORKFORCE EDA ==========")
print("Dataset loaded:", df.shape)


# ==========================================
# 1. WORKFORCE OVERVIEW
# ==========================================

total_employees = len(df)
active_employees = int(df["is_active"].sum())
inactive_employees = total_employees - active_employees

average_age = df["age"].mean()
average_experience = df["year_of_exp"].mean()
average_salary = df["gross_salary"].mean()
average_rating = df["performance_rating"].mean()

print("\n========== WORKFORCE OVERVIEW ==========")
print("Total employees:", total_employees)
print("Active employees:", active_employees)
print("Inactive employees:", inactive_employees)
print("Average age:", round(average_age, 2))
print("Average experience:", round(average_experience, 2))
print("Average gross salary:", round(average_salary, 2))
print("Average performance rating:", round(average_rating, 2))


# ==========================================
# 2. EMPLOYEE STATUS DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 6))

status_counts = (
    df["is_active"]
    .map({True: "Active", False: "Inactive"})
    .value_counts()
)

plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Active vs Inactive Employees")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "01_employee_status.png", dpi=300)
plt.close()


# ==========================================
# 3. GENDER DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df,
    x="gender",
    order=df["gender"].value_counts().index
)

plt.title("Employee Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "02_gender_distribution.png", dpi=300)
plt.close()


# ==========================================
# 4. DEPARTMENT DISTRIBUTION
# ==========================================

plt.figure(figsize=(11, 6))

department_counts = (
    df["dept_name"]
    .value_counts()
    .sort_values(ascending=False)
)

sns.barplot(
    x=department_counts.values,
    y=department_counts.index
)

plt.title("Employees by Department")
plt.xlabel("Number of Employees")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "03_department_distribution.png", dpi=300)
plt.close()


# ==========================================
# 5. QUALIFICATION DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 6))

qualification_counts = df["qualification"].value_counts()

sns.barplot(
    x=qualification_counts.values,
    y=qualification_counts.index
)

plt.title("Employee Qualification Distribution")
plt.xlabel("Number of Employees")
plt.ylabel("Qualification")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "04_qualification_distribution.png", dpi=300)
plt.close()


# ==========================================
# 6. AVERAGE SALARY BY DEPARTMENT
# ==========================================

salary_by_department = (
    df.groupby("dept_name", as_index=False)["gross_salary"]
    .mean()
    .sort_values("gross_salary", ascending=False)
)

plt.figure(figsize=(11, 6))

sns.barplot(
    data=salary_by_department,
    x="gross_salary",
    y="dept_name"
)

plt.title("Average Gross Salary by Department")
plt.xlabel("Average Gross Salary")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "05_average_salary_by_department.png", dpi=300)
plt.close()


# ==========================================
# 7. PERFORMANCE RATING BY DEPARTMENT
# ==========================================

rating_by_department = (
    df.groupby("dept_name", as_index=False)["performance_rating"]
    .mean()
    .sort_values("performance_rating", ascending=False)
)

plt.figure(figsize=(11, 6))

sns.barplot(
    data=rating_by_department,
    x="performance_rating",
    y="dept_name"
)

plt.title("Average Performance Rating by Department")
plt.xlabel("Average Performance Rating")
plt.ylabel("Department")
plt.xlim(0, 5)
plt.tight_layout()
plt.savefig(IMAGE_DIR / "06_performance_by_department.png", dpi=300)
plt.close()


# ==========================================
# 8. AGE DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 6))

sns.histplot(
    data=df,
    x="age",
    bins=20,
    kde=True
)

plt.title("Employee Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "07_age_distribution.png", dpi=300)
plt.close()


# ==========================================
# 9. EXPERIENCE VS GROSS SALARY
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="year_of_exp",
    y="gross_salary",
    alpha=0.5
)

plt.title("Work Experience vs Gross Salary")
plt.xlabel("Years of Experience")
plt.ylabel("Gross Salary")
plt.tight_layout()
plt.savefig(IMAGE_DIR / "08_experience_vs_salary.png", dpi=300)
plt.close()


# ==========================================
# 10. EXPORT ANALYSIS TABLES
# ==========================================

salary_by_department.to_csv(
    REPORT_DIR / "salary_by_department.csv",
    index=False
)

rating_by_department.to_csv(
    REPORT_DIR / "rating_by_department.csv",
    index=False
)

department_counts.rename(
    "employee_count"
).to_csv(
    REPORT_DIR / "employee_count_by_department.csv"
)


# ==========================================
# 11. SAVE SUMMARY REPORT
# ==========================================

summary = f"""
HR WORKFORCE PERFORMANCE ANALYTICS
EXPLORATORY DATA ANALYSIS SUMMARY

Total Employees: {total_employees}
Active Employees: {active_employees}
Inactive Employees: {inactive_employees}

Average Age: {average_age:.2f}
Average Experience: {average_experience:.2f} years
Average Gross Salary: {average_salary:.2f}
Average Performance Rating: {average_rating:.2f}

Total Departments: {df['dept_name'].nunique()}
Total Job Roles: {df['position'].nunique()}

Highest Employee Count Department:
{department_counts.index[0]} ({department_counts.iloc[0]} employees)

Highest Average Salary Department:
{salary_by_department.iloc[0]['dept_name']}

Highest Average Performance Rating Department:
{rating_by_department.iloc[0]['dept_name']}
"""

with open(REPORT_DIR / "eda_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print("\n========== EDA COMPLETED ==========")
print(summary)

print("Visualisations saved in:", IMAGE_DIR)
print("Analysis reports saved in:", REPORT_DIR)
print("\nAll EDA tasks completed successfully!")

