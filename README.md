# HR Workforce Performance Analytics

An end-to-end HR analytics project that analyzes employee information, salary, departmental performance, and workforce distribution using Python, MySQL, and Power BI.

## Project Overview

This project transforms raw HR datasets into meaningful workforce insights through data cleaning, integration, exploratory data analysis, SQL analysis, and interactive Power BI visualization.

## Technologies Used

- **Python 3.14**
- **Pandas & NumPy** – Data processing and analysis
- **Matplotlib & Seaborn** – Data visualization
- **MySQL 8.0** – Relational database and SQL analysis
- **SQLAlchemy & PyMySQL** – Python-MySQL integration
- **Power BI Desktop** – Interactive dashboard

## Project Structure

```text
HR-Workforce-Performance-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── images/
│   ├── 01_employee_status.png
│   ├── 02_gender_distribution.png
│   ├── 03_department_distribution.png
│   ├── 04_qualification_distribution.png
│   ├── 05_average_salary_by_department.png
│   ├── 06_performance_by_department.png
│   ├── 07_age_distribution.png
│   └── 08_experience_vs_salary.png
│
├── notebooks/
├── powerbi/
│   └── hr_workforce_dashboard.pbix
│
├── reports/
│   ├── eda_summary.txt
│   ├── employee_count_by_department.csv
│   ├── rating_by_department.csv
│   └── salary_by_department.csv
│
├── sql/
│   └── hr_analysis_queries.sql
│
├── load_datasets.py
├── clean_and_integrate.py
├── eda_analysis.py
├── import_to_mysql.py
├── check_files.py
├── requirements.txt
├── flow.txt
├── README.md
└── LICENSE
```

## Source Datasets

The project uses four HR datasets:

1. `emp_info.csv` – Employee personal and employment information.
2. `emp_salary.csv` – Salary, deductions, experience, and performance information.
3. `department.csv` – Department details.
4. `job_roles.csv` – Job role information.

The raw CSV datasets are excluded from Git tracking through `.gitignore`.

## Project Workflow

### 1. Data Loading and Validation

- Loaded all four source datasets using Pandas.
- Checked missing values and duplicate records.
- Validated employee, department, and job role identifiers.
- Checked numeric values and date consistency.

### 2. Data Cleaning and Integration

- Standardized column names.
- Cleaned text values.
- Converted date columns.
- Integrated the four datasets using employee, department, and role identifiers.
- Created additional features:
  - Full name
  - Age
  - Years of service
- Validated gross salary calculations.
- Exported the integrated dataset to `data/processed/cleaned_hr_workforce.csv`.

### 3. Exploratory Data Analysis (EDA)

Created eight visualizations covering:

- Employee status distribution
- Gender distribution
- Department distribution
- Qualification distribution
- Average salary by department
- Performance by department
- Employee age distribution
- Experience versus salary

### 4. MySQL Database Integration

Created the `hr_workforce_analytics` database with four relational tables:

- departments
- job_roles
- employees
- salaries

Imported and verified 20,018 records across the four tables.

### 5. SQL Analysis

Developed 12 SQL queries covering:

- Overall workforce summary
- Gender distribution
- Employee count by department
- Salary analysis by department
- Performance analysis by department
- Salary analysis by job role
- Top 10 highest-paid employees
- Employees earning above average salary
- Experience group analysis
- Performance rating distribution
- Department salary ranking using CTE
- Employee salary ranking using window functions

SQL scripts are available in the `sql/` directory.

### 6. Power BI Dashboard

Created an interactive HR Workforce Performance Analytics dashboard containing eight KPI cards and five visualizations.

**Key Performance Indicators:**
- Total Employees
- Active Employees
- Inactive Employees
- Average Gross Salary
- Average Performance Rating
- Total Payroll
- Total Departments
- Active Employee Percentage

**Dashboard Visualizations:**
- Employee Status
- Employees by Department
- Average Salary by Department
- Performance by Department
- Gender Distribution

Power BI dashboard file: `powerbi/hr_workforce_dashboard.pbix`

## Key Project Findings

| Metric | Result |
|---|---:|
| Total Employees | 10,000 |
| Active Employees | 8,488 |
| Inactive Employees | 1,512 |
| Average Age | 41.27 years |
| Average Experience | 5.92 years |
| Average Gross Salary | 75,550.08 |
| Average Performance Rating | 3.78 |
| Total Departments | 9 |
| Total Job Roles | 16 |

**Additional Findings:**
- Product has the highest employee count, with 1,166 employees.
- Customer Service has the highest average gross salary.
- HR has the highest average performance rating.
- No missing values or duplicate employee identifiers were found in the source datasets.

## Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/Arsalan-Dev-Cloud/HR-Workforce-Performance-Analytics.git

cd HR-Workforce-Performance-Analytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Source Datasets

Place the four source CSV files inside `data/raw/`.

### 4. Run Data Loading and Validation

```bash
python load_datasets.py
```

### 5. Clean and Integrate Data

```bash
python clean_and_integrate.py
```

### 6. Perform Exploratory Data Analysis

```bash
python eda_analysis.py
```

### 7. Import Data into MySQL

Ensure the MySQL database and required tables have been created, then run:

```bash
python import_to_mysql.py
```

The script requests the MySQL password.

### 8. Execute SQL Analysis

Open MySQL and execute:

```sql
USE hr_workforce_analytics;

SOURCE E:/HR-Workforce-Performance-Analytics/sql/hr_analysis_queries.sql;
```

### 9. Open the Power BI Dashboard

Open `powerbi/hr_workforce_dashboard.pbix` using Power BI Desktop.

## Project Status

**Completed:** Data loading, validation, cleaning, integration, EDA, MySQL integration, SQL analysis, and Power BI dashboard development.

## Author

**Shaikh Mohammad Arsalan Mohsin**

GitHub: [Arsalan-Dev-Cloud](https://github.com/Arsalan-Dev-Cloud)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.