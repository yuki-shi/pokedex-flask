import sqlite3

#---
#crio uma conexão com a database desejada
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#--- 
cursor.execute("""
CREATE TABLE contact_details
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    surname TEXT,
    address TEXT
)

""")


#---
connection.commit()
connection.close()