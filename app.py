from flask import Flask,render_template,url_for,request,redirect
import mysql.connector
from mysql.connector import IntegrityError

#Getting File Name
app=Flask(__name__)

#mysql connection
con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Ajith@9751",
    database="mangement"
)
if con.is_connected:
    print("Connected Successfully")
else:
    print("Connection Fail")

#Dashboard
@app.route('/')
def home():
    res=con.cursor(dictionary=True)
    sql="select employee.id,name,dept_name,salary,city from employee inner join department on employee.id=department.dept_id"
    res.execute(sql)
    result=res.fetchall()

    #employee count
    res=con.cursor(dictionary=True)
    sql='select count(*) as total_employee from employee'
    res.execute(sql)
    employee_count = res.fetchone()


    #department count
    res=con.cursor(dictionary=True)
    sql='select count(*) as total_department from department'
    res.execute(sql)
    department_count=res.fetchone()

    #Avg Salary of Employee
    res=con.cursor(dictionary=True)
    sql='select round(avg(salary),2) as avg_count from employee'
    res.execute(sql)
    avg_salary=res.fetchone()

    return render_template("home.html", 
                           datas=result,
                           employee_count=employee_count,
                           department_count=department_count,
                           avg_salary=avg_salary)


#Update EMployee Tabel
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    res=con.cursor(dictionary=True)
    if request.method=='POST':
        name=request.form['name']
        salary=request.form['salary']
        city=request.form['city']
        dept_id=request.form['dept_id']

        sql='update employee set name=%s,salary=%s,city=%s,dept_id=%s where id=%s'
        value=(name,salary,city,dept_id,id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    # Employee Detials
    sql='select * from employee where id=%s'
    value=(id,)
    res.execute(sql,value)
    employee=res.fetchone()
    #All Departments
    res.execute('select * from department')
    departments=res.fetchall()
    return render_template(
            "update.html",
            employee=employee,
            departments=departments
        )

#search Employee
@app.route('/search',methods=['GET','POST'])
def search():
    search=request.form['search']
    res=con.cursor(dictionary=True)
    sql = (
        "SELECT employee.id, employee.name, department.dept_name, employee.salary, employee.city "
        "FROM employee "
        "INNER JOIN department "
        "ON employee.dept_id = department.dept_id "
        "WHERE employee.name LIKE %s"
    )
    value=('%' +search+ '%',)
    res.execute(sql,value)
    result=res.fetchall()   
    return render_template("home.html",datas=result)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=="POST":
        name=request.form['name']
        salary=request.form['salary']
        city=request.form['city']
        dept_id=request.form['dept_id']
        res=con.cursor(dictionary=True)
        sql='insert into employee (name,salary,city,dept_id)' \
            'values (%s,%s,%s,%s)'
        value=(name,salary,city,dept_id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    
    #Select Department
    res=con.cursor(dictionary=True)
    sql='select * from department'
    res.execute(sql)
    result=res.fetchall()
    return render_template('add.html',departments=result)

#Add Department
@app.route('/add_Department',methods=['GET','POST'])
def add_department():
    if request.method=='POST':
        dept_name=request.form['dept_name']
        res=con.cursor(dictionary=True)
        sql="insert into department (dept_name) values (%s)"
        value=(dept_name,)
        res.execute(sql,value)
        con.commit()
        return redirect (url_for('department'))
    return render_template('add_department.html')

#Delete Employee
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    res=con.cursor(dictionary=True)
    sql="delete from employee where id=%s"
    value=(id,)
    res.execute(sql,value)
    con.commit()
    return redirect(url_for('home'))

#Employees Page
@app.route('/employees')
def employees():
    res=con.cursor(dictionary=True)
    sql = sql = 'SELECT employee.id, employee.name, department.dept_name, employee.salary, employee.city ' \
      'FROM employee INNER JOIN department ' \
      'ON employee.dept_id = department.dept_id'
    res.execute(sql)
    result=res.fetchall()
    return render_template('employees.html',datas=result)

#department data
@app.route('/department')
def department():
    res=con.cursor(dictionary=True)
    sql='select * from department'
    res.execute(sql)
    result=res.fetchall()
    return render_template('department.html',datas=result)

#update Department
@app.route('/update_department/<int:id>',methods=['GET','POST'])
def update_department(id):
    if request.method=="POST":
        dept_name=request.form['dept_name']
        res=con.cursor(dictionary=True)
        sql='update department set dept_name=%s where dept_id=%s'
        value=(dept_name,id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('department'))
    
    res=con.cursor(dictionary=True)
    sql="select * from department where dept_id=%s"
    value=(id,)
    res.execute(sql,value)
    result=res.fetchone()
    return render_template('update_dept.html',data=result)

#delete Department
@app.route('/delete_dept/<int:id>',methods=['GET','POST'])
def delete_dept(id):
    try:
        res=con.cursor(dictionary=True)
        sql='delete from department where dept_id=%s'
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

if(__name__)=="__main__":
    app.run(debug=True,port=8000)