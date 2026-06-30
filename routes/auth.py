from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import con
from helpers import fetch_one_dict

# Create Blueprint
auth_bp = Blueprint("auth", __name__)


# Login Page
@auth_bp.route('/', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        uid = request.form['username']
        pwd = request.form['password']

        res = con.cursor()

        sql = "SELECT * FROM login WHERE username=?"

        value = (uid,)

        res.execute(sql, value)

        user = fetch_one_dict(res)

        if user and check_password_hash(user['password'], pwd):

            session['user'] = uid

            sql = """
            UPDATE login
            SET
                is_active = 1,
                last_login = GETDATE()
            WHERE username = ?
            """

            res.execute(sql, (uid,))
            con.commit()

            return redirect(url_for("dashboard.home"))

        else:

            return render_template(
                "login.html",
                error="Invalid Username or Password",
                username=uid
            )

    return render_template("login.html")


# Register Page
@auth_bp.route('/register_page', methods=['GET', 'POST'])
def register_page():

    if request.method == "POST":

        uid = request.form['username']
        pwd = request.form['password']
        confirm_pwd = request.form['confirm_password']

        if pwd != confirm_pwd:

            return render_template(
                "register.html",
                error="Password and Confirm Password do not match.",
                username=uid
            )

        res = con.cursor()

        sql = "SELECT * FROM login WHERE username=?"

        res.execute(sql, (uid,))

        user = fetch_one_dict(res)

        if user:

            return render_template(
                "register.html",
                error="Username already exists.",
                username=uid
            )

        hash_password = generate_password_hash(pwd)

        sql = "INSERT INTO login(username,password) VALUES(?,?)"

        res.execute(sql, (uid, hash_password))

        con.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# Logout
@auth_bp.route('/logout')
def logout():

    uid = session['user']

    res = con.cursor()

    sql = """
    UPDATE login
    SET
        is_active = 0,
        last_logout = GETDATE()
    WHERE username = ?
    """

    res.execute(sql, (uid,))

    con.commit()

    session.pop('user', None)

    return redirect(url_for("auth.login"))