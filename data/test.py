import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};Server=localhost\SQLEXPRESS;Database=ai_class;UID=meorung;PWD=mr12345;Trusted_Connection=True;')

cursor = cnxn.cursor()