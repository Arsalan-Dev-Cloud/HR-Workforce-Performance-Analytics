
USE hr_workforce_analytics;

-- =====================================================
-- HR WORKFORCE PERFORMANCE ANALYTICS
-- SQL ANALYSIS QUERIES
-- MySQL 8.0
-- =====================================================


-- 1. OVERALL WORKFORCE SUMMARY

SELECT
    COUNT(*) AS total_employees,
    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active_employees,
    SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) AS inactive_employees,
    ROUND(AVG(TIMESTAMPDIFF(YEAR, dob, CURDATE())), 2) AS average_age
FROM employees;


-- 2. EMPLOYEE DISTRIBUTION BY GENDER

SELECT
    gender,
    COUNT(*) AS employee_count,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2
    ) AS percentage
FROM employees
GROUP BY gender
ORDER BY employee_count DESC;


-- 3. EMPLOYEE COUNT BY DEPARTMENT

SELECT
    d.dept_name,
    COUNT(s.emp_id) AS employee_count
FROM departments d
LEFT JOIN salaries s
    ON d.dept_id = s.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY employee_count DESC;


-- 4. SALARY ANALYSIS BY DEPARTMENT

SELECT
    d.dept_name,
    COUNT(s.emp_id) AS employee_count,
    ROUND(AVG(s.basic_salary), 2) AS average_basic_salary,
    ROUND(AVG(s.gross_salary), 2) AS average_gross_salary,
    ROUND(MIN(s.gross_salary), 2) AS minimum_gross_salary,
    ROUND(MAX(s.gross_salary), 2) AS maximum_gross_salary
FROM departments d
INNER JOIN salaries s
    ON d.dept_id = s.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY average_gross_salary DESC;


-- 5. PERFORMANCE RATING BY DEPARTMENT

SELECT
    d.dept_name,
    COUNT(s.emp_id) AS employee_count,
    ROUND(AVG(s.performance_rating), 2) AS average_rating,
    ROUND(MAX(s.performance_rating), 2) AS highest_rating,
    ROUND(MIN(s.performance_rating), 2) AS lowest_rating
FROM departments d
INNER JOIN salaries s
    ON d.dept_id = s.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY average_rating DESC;


-- 6. SALARY ANALYSIS BY JOB ROLE

SELECT
    j.position,
    COUNT(s.emp_id) AS employee_count,
    ROUND(AVG(s.basic_salary), 2) AS average_basic_salary,
    ROUND(AVG(s.gross_salary), 2) AS average_gross_salary
FROM job_roles j
INNER JOIN salaries s
    ON j.role_id = s.role_id
GROUP BY j.role_id, j.position
ORDER BY average_gross_salary DESC;


-- 7. TOP 10 HIGHEST-PAID EMPLOYEES

SELECT
    e.emp_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    d.dept_name,
    j.position,
    s.gross_salary,
    s.performance_rating
FROM employees e
INNER JOIN salaries s
    ON e.emp_id = s.emp_id
INNER JOIN departments d
    ON s.dept_id = d.dept_id
INNER JOIN job_roles j
    ON s.role_id = j.role_id
ORDER BY s.gross_salary DESC
LIMIT 10;


-- 8. EMPLOYEES EARNING ABOVE COMPANY AVERAGE

SELECT
    e.emp_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    d.dept_name,
    s.gross_salary
FROM employees e
INNER JOIN salaries s
    ON e.emp_id = s.emp_id
INNER JOIN departments d
    ON s.dept_id = d.dept_id
WHERE s.gross_salary > (
    SELECT AVG(gross_salary)
    FROM salaries
)
ORDER BY s.gross_salary DESC;


-- 9. EXPERIENCE GROUP ANALYSIS

SELECT
    CASE
        WHEN year_of_exp < 2 THEN '0-1 Years'
        WHEN year_of_exp < 5 THEN '2-4 Years'
        WHEN year_of_exp < 10 THEN '5-9 Years'
        ELSE '10+ Years'
    END AS experience_group,
    COUNT(*) AS employee_count,
    ROUND(AVG(basic_salary), 2) AS average_basic_salary,
    ROUND(AVG(gross_salary), 2) AS average_gross_salary,
    ROUND(AVG(performance_rating), 2) AS average_rating
FROM salaries
GROUP BY experience_group
ORDER BY MIN(year_of_exp);


-- 10. PERFORMANCE RATING DISTRIBUTION

SELECT
    performance_rating,
    COUNT(*) AS employee_count
FROM salaries
GROUP BY performance_rating
ORDER BY performance_rating DESC;


-- 11. CTE: RANK DEPARTMENTS BY AVERAGE GROSS SALARY

WITH department_salary AS (
    SELECT
        d.dept_name,
        COUNT(s.emp_id) AS employee_count,
        AVG(s.gross_salary) AS average_gross_salary
    FROM departments d
    INNER JOIN salaries s
        ON d.dept_id = s.dept_id
    GROUP BY d.dept_id, d.dept_name
)
SELECT
    dept_name,
    employee_count,
    ROUND(average_gross_salary, 2) AS average_gross_salary,
    RANK() OVER (
        ORDER BY average_gross_salary DESC
    ) AS salary_rank
FROM department_salary;


-- 12. WINDOW FUNCTION: SALARY RANKING WITHIN EACH DEPARTMENT

SELECT
    e.emp_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    d.dept_name,
    s.gross_salary,
    RANK() OVER (
        PARTITION BY d.dept_name
        ORDER BY s.gross_salary DESC
    ) AS department_salary_rank
FROM employees e
INNER JOIN salaries s
    ON e.emp_id = s.emp_id
INNER JOIN departments d
    ON s.dept_id = d.dept_id
ORDER BY d.dept_name, department_salary_rank;
