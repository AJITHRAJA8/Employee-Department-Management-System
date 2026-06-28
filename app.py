from flask import Flask,render_template,url_for,request,redirect,session
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

#Getting File Name
app=Flask(__name__)

#Sql Server Connection
try:
    con = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=AJITH-RAJA\\SQLEXPRESS;"
        "DATABASE=Python_DB;"
        "UID=AJITHRAJA;"
        "PWD=@Ajith@9751;"
        "TrustServerCertificate=yes;"
    )
    print("Connection Successfull")
except Exception as e:
    print(e)

#Helper Function
# Fetch all rows as dictionaries
def fetch_all_dict(cursor):
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return[dict(zip(columns,row)) for row in rows]

## Fetch one row as a dictionary
def fetch_one_dict(cursor):
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()

    if row is None:
        return None
    
    return dict(zip(columns,row))

#Dashboard
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    #Dashboard Table
    res=con.cursor()
    sql="select e.id,e.name,d.dept_name,e.salary,e.city from employee as e" \
    " inner join department as d " \
    " on e.dept_id=d.dept_id"
    res.execute(sql)
    result=fetch_all_dict(res)

    #employee count
    res=con.cursor()
    sql='select count(*) as total_employee from employee'
    res.execute(sql)
    employee_count = fetch_one_dict(res)


    #department count
    res=con.cursor()
    sql='select count(*) as total_department from department'
    res.execute(sql)
    department_count=fetch_one_dict(res)

    #Avg Salary of Employee
    res=con.cursor()
    sql='select round(avg(salary),2) as avg_count from employee'
    res.execute(sql)
    avg_salary=fetch_one_dict(res)

    #High Salary
    res=con.cursor()
    sql='select max(salary) as max_salary from employee'
    res.execute(sql)
    high_salary=fetch_one_dict(res)

    return render_template("home.html", 
                           datas=result,
                           employee_count=employee_count,
                           department_count=department_count,
                           avg_salary=avg_salary,
                           high_salary=high_salary)


#Update EMployee Tabel
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    if request.method=='POST':
        employee_name=request.form['name']
        employee_salary=request.form['salary']
        employee_city=request.form['city']
        department_id=request.form['dept_id']

        sql='update employee set name=?,salary=?,city=?,dept_id=? where id=?'
        value=(employee_name,employee_salary,employee_city,department_id,id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    # Employee Detials
    sql='select * from employee where id=?'
    value=(id,)
    res.execute(sql,value)
    employees=fetch_one_dict(res)

    #All Departments
    res.execute('select * from department')
    department=fetch_all_dict(res)
    return render_template(
            "update.html",
            employee=employees,
            departments=department
        )

#search Employee
@app.route('/search',methods=['GET','POST'])
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    search=request.form['search']
    res=con.cursor()
    sql = (
        "SELECT employee.id, employee.name, department.dept_name, employee.salary, employee.city "
        "FROM employee "
        "INNER JOIN department "
        "ON employee.dept_id = department.dept_id "
        "WHERE employee.name LIKE ?"
    )
    value=('%' +search+ '%',)
    res.execute(sql,value)
    result=fetch_all_dict(res)
    return render_template("employees.html",datas=result)

#Add Employee
@app.route('/add',methods=['GET','POST'])
def add():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method=="POST":
        em_name=request.form['name']
        em_salary=request.form['salary']
        em_city=request.form['city']
        em_dept_id=request.form['dept_id']
        res=con.cursor()
        sql='insert into employee (name,salary,city,dept_id)' \
            'values (?,?,?,?)'
        value=(em_name,em_salary,em_city,em_dept_id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    
    #Select Department
    res=con.cursor()
    sql='select * from department'
    res.execute(sql)
    result=fetch_all_dict(res)
    return render_template('add.html',departments=result)

#Add Department
@app.route('/add_Department',methods=['GET','POST'])
def add_department():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        department_name=request.form['dept_name']
        res=con.cursor()
        sql="insert into department (dept_name) values (?)"
        value=(department_name,)
        res.execute(sql,value)
        con.commit()
        return redirect (url_for('department'))
    return render_template('add_department.html')

#Delete Employee
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    sql="delete from employee where id=?"
    value=(id,)
    res.execute(sql,value)
    con.commit()
    return redirect(url_for('home'))

#Employees Page
@app.route('/employees')
def employees():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    sql = 'SELECT employee.id, employee.name, department.dept_name, employee.salary, employee.city ' \
      'FROM employee INNER JOIN department ' \
      'ON employee.dept_id = department.dept_id'
    res.execute(sql)
    result=fetch_all_dict(res)
    return render_template('employees.html',datas=result)

#department data
@app.route('/department')
def department():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    sql='select * from department'
    res.execute(sql)
    result=fetch_all_dict(res)
    return render_template('department.html',datas=result)

#update Department
@app.route('/update_department/<int:id>',methods=['GET','POST'])
def update_department(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method=="POST":
        department_name=request.form['dept_name']

        res=con.cursor()
        sql='update department set dept_name=? where dept_id=?'
        value=(department_name,id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('department'))
    
    res=con.cursor()
    sql="select * from department where dept_id=?"
    value=(id,)
    res.execute(sql,value)
    result=fetch_one_dict(res)
    return render_template('update_dept.html',data=result)

#delete Department
@app.route('/delete_dept/<int:id>',methods=['GET','POST'])
def delete_dept(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    try:
        res=con.cursor()
        sql='delete from department where dept_id=?'
        value=(id,)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('department'))
    except IntegrityError:
        return """
        <script>
            alert('Cannot delete this department because employees are assigned to it.');
            window.location.href='/department';
        </script>
        """

#salary Report  
@app.route('/salary_report')
def salary_report():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    sql='select employee.id,name,dept_name,salary from employee' \
    ' inner join department on employee.dept_id=department.dept_id'
    res.execute(sql)
    datas=fetch_all_dict(res)
    return render_template('salary_report.html',datas=datas)

#top Earners
@app.route('/top_earners')
def top_earners():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    res=con.cursor()
    sql='select top 5 employee.id,name,dept_name,salary from employee inner join department on employee.dept_id = department.dept_id order by salary desc'
    res.execute(sql)
    datas=fetch_all_dict(res)
    return render_template('top_earners.html',datas=datas)

#LogIn Page
@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        uid = request.form['username']
        pwd = request.form['password']
        res=con.cursor()
        sql='select * from login where username=?'
        value=(uid,)
        res.execute(sql,value)
        user = fetch_one_dict(res)

        if user and check_password_hash(user['password'],pwd):
            session['user'] = uid
            return redirect(url_for('home'))
        else:
            return "Invalid Username or Password"
    return render_template('login.html')

#register page
@app.route('/resister_page',methods=['GET','POST'])
def register_page():
    if request.method=='POST':
        uid=request.form['username']
        pwd=request.form['password']
        confirm_pwd=request.form['confirm_password']

        if pwd != confirm_pwd:
            return "Passwords do not match"
        #hash password
        hash_password = generate_password_hash(pwd)

        res=con.cursor()
        sql='insert into login (username,password) values(?,?)'
        value=(uid,hash_password)
        try:
            res.execute(sql,value)
            con.commit()

            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return str(e)
    return render_template('register.html')

#logout page     
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

if(__name__)=="__main__":
    app.secret_key="Ajith@9751"
    app.run(debug=True,port=8000)