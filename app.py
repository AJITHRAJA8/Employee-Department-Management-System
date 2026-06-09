from flask import Flask,render_template,url_for,request,redirect
import mysql.connector

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
    return render_template("home.html", datas=result)

#Update EMployee Tabel
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        name=request.form['name']
        dept_id=request.form['dept_id']
        print(request.form)
        salary=request.form['salary']
        city=request.form['city']
        res=con.cursor(dictionary=True)
        sql='update employee set name=%s,salary=%s,city=%s,dept_id=%s where id=%s'
        value=(name,salary,city,dept_id,id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    return render_template('update.html')

if(__name__)=="__main__":
    app.run(debug=True,port=8000)