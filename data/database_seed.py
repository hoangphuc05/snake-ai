import csv
import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};Server=localhost\SQLEXPRESS;Database=ai_class;UID=meorung;PWD=mr12345;Trusted_Connection=True;')
cursor = cnxn.cursor()

with open('cs2.csv', 'r', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        #id
        id = row[0] + row[5] + row[6] + row[7]
        print(id)
        studentID = row[0]
        student_class = row[5]
        year = row[6]
        semester = row[7]

        # connect to database
        cursor.execute("INSERT INTO raw_class_data (id, studentId, year, semester, class) VALUES (?, ?, ?, ?, ?)", id, studentID, year, semester, student_class)
        cursor.commit()

cnxn.close()