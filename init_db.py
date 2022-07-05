import psycopg2


###
 # Executado uma vez apenas e usado para criar a database
 # que usaremos no projeto.
###


conn = psycopg2.connect(database='postgres',
                        user='***',
                        password='***',
                        host='localhost',
                        port='5432')
conn.autocommit = True

cursor = conn.cursor()

sql = '''CREATE DATABASE pokemon;'''

cursor.execute('''CREATE DATABASE pokemon;''')

print('Ok!!')

conn.close()