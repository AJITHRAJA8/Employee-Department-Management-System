from flask import Flask,render_template,url_for
import mysql.connector

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


if(__name__)=="__main__":
    app.run(debug=True,port=8000)