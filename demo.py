
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

def