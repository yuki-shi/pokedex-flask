from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

app = Flask(__name__)

#---
@app.route('/', methods=['GET', 'POST'])
def index():

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    type = request.form.get('type')
    cursor.execute("""
        SELECT * FROM pokemon
         WHERE Type1 LIKE ?
         OR Type2 LIKE ?
        """, (type, type))
    pokemon = cursor.fetchall()

    return render_template('index.html', pokemon=pokemon)


#---
if __name__ == '__main__':
    app.run(debug=True)