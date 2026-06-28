from flask import Blueprint, render_template, redirect, url_for, session

from database import con
from helpers import fetch_all_dict, fetch_one_dict

# Create Blueprint
reports_bp = Blueprint("reports", __name__)


# Helper: fetch notification data for navbar
def get_notifications():
    res = con.cursor()
    res.execute("SELECT COUNT(*) AS Total_notification FROM notifications WHERE is_read = 0")
    notification_count = fetch_one_dict(res)

    res = con.cursor()
    res.execute("""
        SELECT TOP 5 notification_id, message, created_at, is_read
        FROM notifications
        ORDER BY created_at DESC
    """)
    notifications = fetch_all_dict(res)

    return notification_count, notifications


# Salary Report
@reports_bp.route('/salary_report')
def salary_report():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()
    sql = """
    SELECT
        employee.id,
        employee.name,
        department.dept_name,
        employee.salary
    FROM employee
    INNER JOIN department
        ON employee.dept_id = department.dept_id
    """
    res.execute(sql)
    datas = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "salary_report.html",
        datas=datas,
        notification_count=notification_count,
        notifications=notifications
    )


# Top Earners
@reports_bp.route('/top_earners')
def top_earners():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()
    sql = """
    SELECT TOP 5
        employee.id,
        employee.name,
        department.dept_name,
        employee.salary
    FROM employee
    INNER JOIN department
        ON employee.dept_id = department.dept_id
    ORDER BY employee.salary DESC
    """
    res.execute(sql)
    datas = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "top_earners.html",
        datas=datas,
        notification_count=notification_count,
        notifications=notifications
    )