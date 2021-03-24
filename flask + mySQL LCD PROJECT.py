import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="attendance"
    )

from flask import Flask
import random

app = Flask(__name__)


@app.route("/")
def home():
    myhtml = '''
<!DOCTYPE html>
<html>
<head>
<h1>Most Recent Student Entries</h1>
<table style="width:200" border = "2">
    <tr>
        <th>RFID</th>
        <th>Student Name</th>
        <th>Date & Time</th>
    </tr>
'''
    mycursor = mydb.cursor()
    query = "SELECT RFID, Students, DATE_FORMAT(Time, '%Y-%m-%d %T') FROM Students ORDER BY Time DESC LIMIT 5"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for row in myresult:
        print(row)
        myhtml = myhtml + '''
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
'''.format(row[0],row[1],row[2])
        print(row)
    
    myhtml = myhtml + '''
</head>
</html>
'''
    return myhtml

if __name__ == "__main__":
    app.run(host='0.0.0.0')

    
    
    
    