import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};Server=localhost\SQLEXPRESS;Database=ai_class;UID=meorung;PWD=mr12345;Trusted_Connection=True;')
cursor = cnxn.cursor()


# select every row of the raw_class_data table
cursor.execute("SELECT * FROM raw_class_data")
rows = cursor.fetchall()

# print(rows[0])
for row in rows:
    # count number of previous class based on semester
    # fall semester
    if row[3].strip() == 'FA':
        cursor.execute("EXEC ai_class.dbo.GetClassBeforeFall @studentId=?, @year=?;", row[1].strip(), row[2].strip())
        result = cursor.fetchall()
    
    # spring semester
    if row[3].strip() == 'SP':
        cursor.execute("EXEC ai_class.dbo.GetClassBeforeSpring @studentId=?, @year=?;", row[1].strip(), row[2].strip())
        result = cursor.fetchall()

    # summer semester
    if row[3].strip() == 'SU':
        cursor.execute("EXEC ai_class.dbo.GetClassBeforeSummer @studentId=?, @year=?;", row[1].strip(), row[2].strip())
        result = cursor.fetchall()

    # Jan semester
    if row[3].strip() == 'JA':
        cursor.execute("EXEC ai_class.dbo.GetClassBeforeJan @studentId=?, @year=?;", row[1].strip(), row[2].strip())
        result = cursor.fetchall()

    # while True:
    #     pass
    # add result to the class_data table
    cursor.execute("INSERT INTO class_data (id, studentId, year, semester, class, previous_class) VALUES (?, ?, ?, ?, ?, ?)", row[0], row[1], row[2], row[3], row[4], result[0][0])
    cursor.commit()
