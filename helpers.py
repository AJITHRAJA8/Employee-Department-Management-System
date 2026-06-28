from database import con

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

# Helper function for insert notication
# Helper function for insert notification
def add_notification(message):

    res = con.cursor()
    sql = """
    INSERT INTO notifications(message)
    VALUES (?)
    """
    value = (message,)
    res.execute(sql, value)
    con.commit()
