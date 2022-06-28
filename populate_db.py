import sqlite3

#---
#crio uma conexão com a database desejada
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#--- 
cursor.execute("""
INSERT INTO contact_details (firstname, surname, address)
    VALUES ('Yuki', 'Zinha', 'Casa 123 aaa'),
           ('Yuki', 'Kabuki', 'Lá longe 3009'),
           ('Yuki', 'Ukiy', 'Não é Brasília 11')
""")


#---
connection.commit()
connection.close()




### sqlite3 database.db