import sqlite3

#---
#crio uma conexão com a database desejada
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#--- 
cursor.execute("""
SELECT * FROM contact_details
""")

student_info = cursor.fetchall()
print(student_info)

#---
connection.commit()
connection.close()