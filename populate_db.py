import psycopg2

###
 # Com a database criada, vamos criar uma tabela
 # e copiar o nosso .csv para ela.
###


try:
    conn = psycopg2.connect(database='pokemon',
                            user='***',
                            password='***',
                            host='localhost',
                            port='5432')
    
    cursor = conn.cursor()
except:
    raise Exception('A conexão deu ruim!!')


try:
    cursor.execute('''DROP TABLE IF EXISTS pokemon;

                    CREATE TABLE pokemon (
                        Id INTEGER NOT NULL PRIMARY KEY,
                        Name VARCHAR(20) NOT NULL,
                        HP INTEGER NOT NULL,
                        Att INTEGER NOT NULL,
                        Def INTEGER NOT NULL,
                        SpAtt INTEGER NOT NULL,
                        SpDef INTEGER NOT NULL,
                        Spd INTEGER NOT NULL,
                        Type1 VARCHAR(10) NOT NULL,
                        Type2 VARCHAR(10),
                        Height FLOAT NOT NULL,
                        Weight FLOAT NOT NULL,
                        Ability1 VARCHAR(20) NOT NULL,
                        Ability2 VARCHAR(20),
                        HiddenAbility VARCHAR(20),
                        Legendary VARCHAR(10) NOT NULL
                        );'''
    )

    print('Tabela criada!!')

    with open('pokemon.csv', 'r') as f:
        cursor.copy_expert("COPY pokemon FROM stdin WITH CSV HEADER DELIMITER AS ','", f)

    print('CSV importado!!')

    conn.commit()
    conn.close()
    cursor.close()

except:
    conn.close()
    cursor.close()
    raise Exception('Houve um erro na importação do .csv!')