
'''
import pyodbc

try:
    con = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=AJITH-RAJA\\SQLEXPRESS;"
        "DATABASE=Python_DB;"
        "UID=AJITHRAJA;"
        "PWD=@Ajith@9751;"
        "TrustServerCertificate=yes;"
    )

    print("Connected Successfully")

except Exception as e:
    print(e)
'''

import pyodbc

try:
    con=pyodbc.connect(
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

def fetch_all_dict(cursor):
    columns = [column[0] for column in cursor.discription]
    rows = cursor.fetchall()
    return [dict(zip(columns,row))for row in rows]

def fetch_one_dict(cursor):
    columns = [column[0] for column in cursor.discription]
    row = cursor.fetchone()

    if row is None:
        return None
    return dict(zip(columns,row))