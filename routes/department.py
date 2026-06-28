from flask import Blueprint, render_template, request, redirect, url_for, session
from database import con
from helpers import fetch_all_dict, fetch_one_dict, add_notification
from pyodbc import IntegrityError

# Create Blueprint
department_bp = Blueprint("department", __name__)


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


# Department Page
@department_bp.route('/department')
def department():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()
    res.execute("SELECT * FROM department")
    result = fetch_all_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        'department.html',
        datas=result,
        notification_count=notification_count,
        notifications=notifications
    )


# Add Department
@department_bp.route('/add_Department', methods=['GET', 'POST'])
def add_department():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        department_name = request.form['dept_name']

        res = con.cursor()
        res.execute("INSERT INTO department(dept_name) VALUES(?)", (department_name,))
        con.commit()

        add_notification(f"🏛 Department '{department_name}' created.")

        return redirect(url_for('department.department'))

    notification_count, notifications = get_notifications()

    return render_template(
        'add_department.html',
        notification_count=notification_count,
        notifications=notifications
    )


# Update Department
@department_bp.route('/update_department/<int:id>', methods=['GET', 'POST'])
def update_department(id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":

        department_name = request.form['dept_name']

        res = con.cursor()
        res.execute("UPDATE department SET dept_name=? WHERE dept_id=?", (department_name, id))
        con.commit()

        add_notification(f"✏ Department '{department_name}' updated.")

        return redirect(url_for('department.department'))

    res = con.cursor()
    res.execute("SELECT * FROM department WHERE dept_id=?", (id,))
    result = fetch_one_dict(res)

    notification_count, notifications = get_notifications()

    return render_template(
        "update_dept.html",
        data=result,
        notification_count=notification_count,
        notifications=notifications
    )


# Delete Department
@department_bp.route('/delete_dept/<int:id>', methods=['GET', 'POST'])
def delete_dept(id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    try:

        res = con.cursor()
        res.execute("DELETE FROM department WHERE dept_id=?", (id,))
        con.commit()

        add_notification("🗑 Department deleted.")

        return redirect(url_for('department.department'))

    except IntegrityError:

        return """
        <script>
        alert('Cannot delete this department because employees are assigned to it.');
        window.location.href='/department';
        </script>
        """