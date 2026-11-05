
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# 1. FOLDER SETUP
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "cleaned_hr_workforce.csv"
)

IMAGE_DIR = os.path.join(BASE_DIR, "images")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

df["hire_date"] = pd.to_datetime(
    df["hire_date"], errors="coerce"
)

print("=" * 55)
print("ADVANCED HR WORKFORCE ANALYSIS")
print("=" * 55)

print("Dataset shape:", df.shape)
print("Total employees:", len(df))

# --------------------------------------------------
# 3. LOCATION ANALYSIS
# --------------------------------------------------

for column in ["city", "state", "country"]:
    result = (
        df[column]
        .value_counts()
        .rename_axis(column)
        .reset_index(name="employee_count")
    )

    result.to_csv(
        os.path.join(REPORT_DIR, f"{column}_distribution.csv"),
        index=False
    )

print("\nLocation analysis completed!")

# --------------------------------------------------
# 4. MARITAL STATUS ANALYSIS
# --------------------------------------------------

marital_analysis = (
    df["marital_status"]
    .value_counts()
    .rename_axis("marital_status")
    .reset_index(name="employee_count")
)

marital_analysis.to_csv(
    os.path.join(REPORT_DIR, "marital_status_analysis.csv"),
    index=False
)

# --------------------------------------------------
# 5. HIRING TRENDS
# --------------------------------------------------

df["hire_year"] = df["hire_date"].dt.year
df["hire_month"] = df["hire_date"].dt.month

hiring_yearly = (
    df.groupby("hire_year", dropna=True)
    .size()
    .reset_index(name="employees_hired")
)

hiring_monthly = (
    df.groupby(["hire_year", "hire_month"], dropna=True)
    .size()
    .reset_index(name="employees_hired")
)

hiring_yearly.to_csv(
    os.path.join(REPORT_DIR, "hiring_trends_yearly.csv"),
    index=False
)

hiring_monthly.to_csv(
    os.path.join(REPORT_DIR, "hiring_trends_monthly.csv"),
    index=False
)

# --------------------------------------------------
# 6. SALARY BY JOB ROLE
# --------------------------------------------------

role_salary = (
    df.groupby("position")
    .agg(
        employee_count=("emp_id", "count"),
        average_basic_salary=("basic_salary", "mean"),
        average_gross_salary=("gross_salary", "mean"),
        average_bonus=("performance_bonus", "mean"),
        role_benchmark=("base_salary", "mean")
    )
    .reset_index()
    .sort_values("average_gross_salary", ascending=False)
)

role_salary.to_csv(
    os.path.join(REPORT_DIR, "salary_by_job_role.csv"),
    index=False
)

# --------------------------------------------------
# 7. SALARY BENCHMARK COMPARISON
# --------------------------------------------------

df["salary_difference"] = (
    df["basic_salary"] - df["base_salary"]
)

df["salary_vs_benchmark"] = np.select(
    [
        df["salary_difference"] > 0,
        df["salary_difference"] < 0
    ],
    [
        "Above Benchmark",
        "Below Benchmark"
    ],
    default="Equal to Benchmark"
)

benchmark_analysis = (
    df.groupby("salary_vs_benchmark")
    .size()
    .reset_index(name="employee_count")
)

benchmark_analysis.to_csv(
    os.path.join(REPORT_DIR, "salary_benchmark_analysis.csv"),
    index=False
)

# --------------------------------------------------
# 8. PERFORMANCE BONUS ANALYSIS
# --------------------------------------------------

bonus_department = (
    df.groupby("dept_name")
    .agg(
        average_bonus=("performance_bonus", "mean"),
        total_bonus=("performance_bonus", "sum"),
        employee_count=("emp_id", "count")
    )
    .reset_index()
    .sort_values("average_bonus", ascending=False)
)

bonus_department.to_csv(
    os.path.join(REPORT_DIR, "bonus_by_department.csv"),
    index=False
)

bonus_rating = (
    df.groupby("performance_rating")
    .agg(
        average_bonus=("performance_bonus", "mean"),
        employee_count=("emp_id", "count")
    )
    .reset_index()
)

bonus_rating.to_csv(
    os.path.join(REPORT_DIR, "bonus_by_performance_rating.csv"),
    index=False
)

# --------------------------------------------------
# 9. PF AND ESI DEDUCTION ANALYSIS
# --------------------------------------------------

deduction_analysis = (
    df.groupby("dept_name")
    .agg(
        average_pf=("pf_deduction", "mean"),
        average_esi=("esi_deduction", "mean"),
        total_pf=("pf_deduction", "sum"),
        total_esi=("esi_deduction", "sum")
    )
    .reset_index()
)

deduction_analysis.to_csv(
    os.path.join(REPORT_DIR, "deduction_analysis.csv"),
    index=False
)

# --------------------------------------------------
# 10. PERFORMANCE AND BONUS CORRELATION
# --------------------------------------------------

performance_bonus_correlation = df[
    ["performance_rating", "performance_bonus"]
].corr().iloc[0, 1]

print(
    "\nPerformance rating and bonus correlation:",
    round(performance_bonus_correlation, 3)
)

# --------------------------------------------------
# 11. STATISTICAL ANALYSIS
# --------------------------------------------------

numeric_columns = [
    "age",
    "years_of_service",
    "year_of_exp",
    "basic_salary",
    "pf_deduction",
    "esi_deduction",
    "performance_rating",
    "performance_bonus",
    "gross_salary",
    "base_salary"
]

statistics = df[numeric_columns].describe().round(2)

statistics.to_csv(
    os.path.join(REPORT_DIR, "advanced_statistical_summary.csv")
)

# --------------------------------------------------
# 12. CORRELATION MATRIX
# --------------------------------------------------

correlation = df[numeric_columns].corr()

correlation.to_csv(
    os.path.join(REPORT_DIR, "correlation_matrix.csv")
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("HR Workforce Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_DIR, "09_correlation_heatmap.png"),
    dpi=300
)

plt.close()

# --------------------------------------------------
# 13. ADDITIONAL VISUALIZATIONS
# --------------------------------------------------

# Hiring trends
plt.figure(figsize=(10, 5))
plt.plot(
    hiring_yearly["hire_year"],
    hiring_yearly["employees_hired"],
    marker="o"
)
plt.title("Employee Hiring Trends by Year")
plt.xlabel("Year")
plt.ylabel("Employees Hired")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    os.path.join(IMAGE_DIR, "10_hiring_trends.png"),
    dpi=300
)
plt.close()

# Salary by job role
plt.figure(figsize=(12, 7))
sns.barplot(
    data=role_salary,
    x="average_gross_salary",
    y="position"
)
plt.title("Average Gross Salary by Job Role")
plt.xlabel("Average Gross Salary")
plt.ylabel("Job Role")
plt.tight_layout()
plt.savefig(
    os.path.join(IMAGE_DIR, "11_salary_by_job_role.png"),
    dpi=300
)
plt.close()

# Bonus by department
plt.figure(figsize=(12, 6))
sns.barplot(
    data=bonus_department,
    x="average_bonus",
    y="dept_name"
)
plt.title("Average Performance Bonus by Department")
plt.xlabel("Average Bonus")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(
    os.path.join(IMAGE_DIR, "12_bonus_by_department.png"),
    dpi=300
)
plt.close()

# Employee distribution by state (top 10)
state_top10 = (
    df["state"]
    .value_counts()
    .head(10)
    .reset_index()
)
state_top10.columns = ["state", "employee_count"]

plt.figure(figsize=(12, 6))
sns.barplot(
    data=state_top10,
    x="employee_count",
    y="state"
)
plt.title("Top 10 States by Employee Count")
plt.xlabel("Employee Count")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(
    os.path.join(IMAGE_DIR, "13_employee_distribution_by_state.png"),
    dpi=300
)
plt.close()

# --------------------------------------------------
# 14. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 55)
print("ADVANCED ANALYSIS RESULTS")
print("=" * 55)

print("Unique cities:", df["city"].nunique())
print("Unique states:", df["state"].nunique())
print("Unique countries:", df["country"].nunique())

print(
    "Highest hiring year:",
    int(hiring_yearly.loc[
        hiring_yearly["employees_hired"].idxmax(), "hire_year"
    ])
    if not hiring_yearly.empty else "Not available"
)

print(
    "Highest average salary role:",
    role_salary.iloc[0]["position"]
    if not role_salary.empty else "Not available"
)

print(
    "Average PF deduction:",
    round(df["pf_deduction"].mean(), 2)
)

print(
    "Average ESI deduction:",
    round(df["esi_deduction"].mean(), 2)
)

print(
    "Average performance bonus:",
    round(df["performance_bonus"].mean(), 2)
)

print("\nAll advanced analyses completed!")
print("Reports saved in:", REPORT_DIR)
print("Charts saved in:", IMAGE_DIR)
