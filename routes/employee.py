import math
from flask import Blueprint, render_template, request, redirect, url_for, session

from database import con
from helpers import fetch_all_dict, fetch_one_dict, add_notification

# Create Blueprint
employee_bp = Blueprint("employee", __name__)


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


# Employees Page (with pagination)
@employee_bp.route('/employees')
def employees():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Total employee count for pagination
    res = con.cursor()
    res.execute("SELECT COUNT(*) AS total FROM employee")
    total_count = fetch_one_dict(res)
    total_pages = math.ceil(total_count['total'] / per_page)

    # Paginated employee list
    res = con.cursor()
    sql = """
    SELECT employee.id,
           employee.name,
           department.dept_name,
           employee.salary,
           employee.city
    FROM employee
    INNER JOIN department
        ON employee.dept_id = department.dept_id
    ORDER BY employee.id
    OFFSET ? ROWS
    FETCH NEXT ? ROWS ONLY
    """
    res.execute(sql, (offset, per_page))
    result = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "employees.html",
        datas=result,
        page=page,
        total_pages=total_pages,
        notification_count=notification_count,
        notifications=notifications
    )


# Add Employee
@employee_bp.route('/add', methods=['GET', 'POST'])
def add():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":

        em_name = request.form['name']
        em_salary = request.form['salary']
        em_city = request.form['city']
        em_dept_id = request.form['dept_id']

        res = con.cursor()
        sql = """
        INSERT INTO employee(name,salary,city,dept_id)
        VALUES (?,?,?,?)
        """
        res.execute(sql, (em_name, em_salary, em_city, em_dept_id))
        con.commit()

        add_notification(f"👤 Employee '{em_name}' added.")

        return redirect(url_for("dashboard.home"))

    res = con.cursor()
    res.execute("SELECT * FROM department")
    result = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "add.html",
        departments=result,
        notification_count=notification_count,
        notifications=notifications
    )


# Search Employee (no pagination — shows all matches)
@employee_bp.route('/search', methods=['GET', 'POST'])
def search():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.form['search']

    res = con.cursor()
    sql = """
    SELECT employee.id,
           employee.name,
           department.dept_name,
           employee.salary,
           employee.city
    FROM employee
    INNER JOIN department
        ON employee.dept_id = department.dept_id
    WHERE employee.name LIKE ?
    """
    res.execute(sql, ('%' + search + '%',))
    result = fetch_all_dict(res)

    total_pages = 1
    page = 1

    notification_count, notifications = get_notifications()

    return render_template(
        "employees.html",
        datas=result,
        page=page,
        total_pages=total_pages,
        notification_count=notification_count,
        notifications=notifications
    )


# Update Employee
@employee_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    if request.method == "POST":

        employee_name = request.form['name']
        employee_salary = request.form['salary']
        employee_city = request.form['city']
        department_id = request.form['dept_id']

        sql = """
        UPDATE employee
        SET
            name=?,
            salary=?,
            city=?,
            dept_id=?
        WHERE id=?
        """
        res.execute(sql, (employee_name, employee_salary, employee_city, department_id, id))
        con.commit()

        add_notification(f"✏ Employee '{employee_name}' updated.")

        return redirect(url_for("employee.employees"))

    sql = "SELECT * FROM employee WHERE id=?"
    res.execute(sql, (id,))
    employees = fetch_one_dict(res)

    res.execute("SELECT * FROM department")
    departments = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "update.html",
        employee=employees,
        departments=departments,
        notification_count=notification_count,
        notifications=notifications
    )


# Delete Employee
@employee_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    sql = "SELECT name FROM employee WHERE id=?"
    res.execute(sql, (id,))
    employee = fetch_one_dict(res)

    if employee is None:
        return redirect(url_for("employee.employees"))

    sql = "DELETE FROM employee WHERE id=?"
    res.execute(sql, (id,))
    con.commit()

    add_notification(f"🗑 Employee '{employee['name']}' deleted.")

    return redirect(url_for("employee.employees"))