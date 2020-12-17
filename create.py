import sqlite3

conn = sqlite3.connect('face.db')
print ("Opened database successfully");

conn.execute('''CREATE TABLE TEACHERS_ATTENDANCE
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         NAME           TEXT    NOT NULL,
         DATE_PRESENT   TEXT,
         SESSION	TEXT);''')
print ("Table created successfully");

conn.close()