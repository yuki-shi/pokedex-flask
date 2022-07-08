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

    return render_template('index.html', types=types, graphJSON=get_graph())


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

    #---

    df_filter = df.loc[(df['type1'] == f'{type}') | (df['type2'] == f'{type}'), :]

    df_bar = df_filter
    df_bar.loc[df_bar['type2'].isnull(), 'type2'] = df_bar['type1']
    df_bar = df_bar.groupby(['type1', 'type2']).nunique()['id'].reset_index()
    df_bar.loc[df_bar['type1'] == df_bar['type2'], 'type-agg'] = df_bar['type1']
    df_bar.loc[df_bar['type1'] != df_bar['type2'], 'type-agg'] = df_bar[['type1', 'type2']].transpose().agg(' + '.join)
    df_bar.sort_values('id', ascending=False, inplace=True)

    df_cat = df_filter.select_dtypes(exclude='object')
    df_cat = df_cat.drop('id', axis=1)
    df_stats = df_cat[['hp', 'att', 'def', 'spatt', 'spdef', 'spd']]
    df_stats.rename(columns={'hp':'HP', 'att':'Atk', 'def':'Defense', 
                            'spatt':'Sp.Attck', 'spdef':'Sp.Def', 'spd':'Speed'}, inplace=True)

    df_table = df[['name', 'type1', 'type2','hp', 'att', 'def', 'spatt', 'spdef', 'spd']]

    #---

    fig_bar = go.Figure(data=[go.Bar(x=df_bar['type-agg'],
                                 y=df_bar['id'])])

    fig_box = go.Figure()
    for column in df_stats.columns:
        fig_box.add_trace(go.Box(y=df_stats[column], name=column))

    fig_table = go.Figure(data=[go.Table(
                            header=dict(values=list(df_table.columns),
                                        fill_color='rgba(53, 170, 114, 0.95)',
                                        align='left'),
                            cells=dict(values=df_table.transpose(),
                                    align='left'))
                    ])

    fig_bar.update_layout(width=680, height=550)
    fig_box.update_layout(width=690, height=550)
    fig_table.update_layout(width=890)

    fig_bar.update_traces(marker_color='rgba(53, 170, 114, 0.95)')

    data = [fig_bar, fig_box, fig_table]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

#------------
if __name__ == '__main__':
    app.run(debug=True)


