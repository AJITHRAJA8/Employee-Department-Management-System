from flask import Blueprint, render_template, request, redirect, url_for, session
import math

from database import con
from helpers import fetch_all_dict, fetch_one_dict

# Create Blueprint
dashboard_bp = Blueprint("dashboard", __name__)


# Dashboard
@dashboard_bp.route('/home')
def home():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Navbar
    username = session['user']

    # Logged-in User Details
    res = con.cursor()
    sql = """
    SELECT username,is_active,last_login,last_logout
    FROM login
    WHERE username=?
    """
    res.execute(sql, (session['user'],))
    user_info = fetch_one_dict(res)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Notification Count
    res = con.cursor()
    sql = """
    SELECT COUNT(*) AS Total_notification
    FROM notifications
    WHERE is_read = 0
    """
    res.execute(sql)
    notification_count = fetch_one_dict(res)

    # Latest Notifications
    res = con.cursor()
    sql = """
    SELECT TOP 5
        notification_id,
        message,
        created_at,
        is_read
    FROM notifications
    ORDER BY created_at DESC
    """
    res.execute(sql)
    notifications = fetch_all_dict(res)

    # Dashboard Table
    res = con.cursor()
    sql = """
    SELECT e.id,
           e.name,
           d.dept_name,
           e.salary,
           e.city
    FROM employee AS e
    INNER JOIN department AS d
        ON e.dept_id = d.dept_id
    ORDER BY e.id
    OFFSET ? ROWS
    FETCH NEXT ? ROWS ONLY
    """
    res.execute(sql, (offset, per_page))
    result = fetch_all_dict(res)

    # Employee Count
    res = con.cursor()
    sql = "SELECT COUNT(*) AS total_employee FROM employee"
    res.execute(sql)
    employee_count = fetch_one_dict(res)

    total_pages = math.ceil(employee_count['total_employee'] / per_page)

    # Department Count
    res = con.cursor()
    sql = "SELECT COUNT(*) AS total_department FROM department"
    res.execute(sql)
    department_count = fetch_one_dict(res)

    # Average Salary
    res = con.cursor()
    sql = """
    SELECT CAST(AVG(salary) AS DECIMAL(10,2)) AS avg_count
    FROM employee
    """
    res.execute(sql)
    avg_salary = fetch_one_dict(res)

    # Highest Salary
    res = con.cursor()
    sql = """
    SELECT MAX(salary) AS max_salary
    FROM employee
    """
    res.execute(sql)
    high_salary = fetch_one_dict(res)

    return render_template(
        "home.html",
        datas=result,
        user_info=user_info,
        username=username,
        page=page,
        total_pages=total_pages,
        employee_count=employee_count,
        department_count=department_count,
        avg_salary=avg_salary,
        high_salary=high_salary,
        notification_count=notification_count,
        notifications=notifications
    )