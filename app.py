from flask import Flask, render_template, request
import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from pg_auth import pg_auth
import re

app = Flask(__name__)

#---------

@app.route('/')
def index():

    conn = pg_auth()
    cursor = conn.cursor()

    cursor.execute("""SELECT DISTINCT type1 FROM pokemon;""")
    columns = cursor.fetchall()
    cursor.execute("""SELECT DISTINCT type2 FROM pokemon;""")
    columns.extend(cursor.fetchall())

    columns = set(columns) # remover duplicados

    types = [re.sub(r"[,()']", '', str(x)) for x in columns]
    types.remove('None')
    types.sort()

    return render_template('index.html', types=types)


@app.route('/callback')
def callback():
    return get_graph(request.args.get('data'))



#---------
def get_graph(type='grass'):

    conn = pg_auth()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM pokemon
         WHERE type1 = '{type}'
         OR type2 = '{type}'; """)

    columns = [x[0] for x in cursor.description]     
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=columns)

    conn.close()
    cursor.close

    fig = go.Figure(data=[go.Table(
                            header=dict(values=list(df.columns),
                                        fill_color='olive',
                                        align='left'),
                            cells=dict(values=df.transpose(),
                                    align='left'))
                    ])
    fig.update_layout(width=980, height=1900)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

#------------
if __name__ == '__main__':
    app.run(debug=True)