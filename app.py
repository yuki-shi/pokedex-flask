from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)

#---
@app.route('/', methods=['GET', 'POST'])
def index():

    connection = sqlite3.connect('database.db')
    df = pd.read_sql_query("""
        SELECT * FROM pokemon""", con=connection)
    connection.commit()
    connection.close()

    df = df.head(30)

    fig = go.Figure(data=[go.Table(
                            header=dict(values=list(df.columns),
                                        fill_color='olive',
                                        align='left'),
                            cells=dict(values=df.transpose(),
                                       align='left'))
                    ])


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)


#---
if __name__ == '__main__':
    app.run(debug=True)