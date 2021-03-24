from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="attendance"
    )

mycursor = mydb.cursor()
query = "CREATE TABLE IF NOT EXISTS Students (RFID TEXT,Students TEXT, Time DATETIME);"
mycursor.execute(query)
    
bottom = (
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111,
    0b11111,
    0b11111
    )

lcd.create_char(0, bottom)

top = (
    	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b00000,
	0b00000,
	0b00000,
	0b00000
        )

lcd.create_char(1, top)

left = (
    	0b11100,
	0b11100,
	0b11100,
	0b11100,
	0b11100,
	0b11100,
	0b11100,
	0b11100
        )
lcd.create_char(2, left)

right = (
        0b00111,
	0b00111,
	0b00111,
	0b00111,
	0b00111,
	0b00111,
	0b00111,
	0b00111
        )

lcd.create_char(3, right)

top_left = (
    	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b11100,
	0b11100,
	0b11100,
	0b11100
        )

lcd.create_char(4, top_left)

top_right = (
    	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b00111,
	0b00111,
	0b00111,
	0b00111
        )

lcd.create_char(5, top_right)

bottom_left = (
	0b11100,
	0b11100,
	0b11100,
	0b11100,
	0b11111,
	0b11111,
	0b11111,
	0b11111
        )

lcd.create_char(6, bottom_left)

bottom_right = (
	0b00111,
	0b00111,
	0b00111,
	0b00111,
	0b11111,
	0b11111,
	0b11111,
	0b11111
        )

lcd.create_char(7, bottom_right)

while True:
    long = False
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string('Please Scan Your\n\rCard')
    lcd.cursor_pos = (0,0)

    id, text = reader.read()
    print(id)
    print(text)
    lcd.clear()

    lcd.write_string('\4\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\5')
    lcd.cursor_pos = (1,0)
    lcd.write_string('\2')
    lcd.cursor_pos = (2,0)
    lcd.write_string('\2')
    lcd.cursor_pos = (1,19)
    lcd.write_string('\3')
    lcd.cursor_pos = (2,19)
    lcd.write_string('\3')
    lcd.cursor_pos = (3,0)
    lcd.write_string('\6\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\7')
    lcd.cursor_pos = (1,6)
    lcd.write_string('Welcome:')

    sad = 0
    text = text.strip()
    length = len(text)
    print(length)
    space = 0
    if length == 0 or length == 1:
        space = 10
    elif length == 2 or length == 3:
        space = 9
    elif length == 4 or length == 5:
        space = 8
    elif length == 6 or length == 7:
        space = 7
    elif length == 8 or length == 9:
        space = 6
    elif length == 10 or length == 11:
        space = 5
    elif length == 12 or length == 13:
        space = 4
    elif length == 14 or length == 15:
        space = 3
    elif length == 16 or length == 17:
        space = 2
    else:
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string('Name Too Long ERROR')
        long = True
        time.sleep(5)
    
    if long == False:
        lcd.cursor_pos = (2,space)
        lcd.write_string(text)

        sql = "INSERT INTO Students (RFID, Students, Time) VALUES (%s, %s, NOW())"
        val = (id, text)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "name inserted.")
        print("")
        query = "SELECT RFID, Students, DATE_FORMAT(Time, '%Y-%m-%d %T') FROM Students ORDER BY Time DESC LIMIT 5"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        
        for row in myresult:
            print(row)
        time.sleep(5)








