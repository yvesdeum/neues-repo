# Import packages
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import numpy as np
import pandas as pd
from pandasgui import show
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo
import plotly.figure_factory as ff
from plotly import tools
from plotly import subplots

df = pd.read_csv("https://raw.githubusercontent.com/yvesdeum/neues-repo/main/gapminderDataFiveYear.csv")

app = Dash(__name__)

app.layout= html.Div([
    html.H1(children='Dynamic Graphic', style=dict(textAlign = 'center')),
    html.Div(children = "Please, select a country ", style= dict(margin = '10px')),
    dcc.Dropdown(
        id = 'country',
        options=[x for x in df['country'].unique().tolist()],
        value= 'Cameroon'
    ),
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id = 'multi_country',
        options=[x for x in df['country'].unique().tolist()],
        #value= 'Algeria',
        multi=True
    ),
    html.Div([
        dcc.Graph(id='fig_compare'),
    ], style={
        'height': '100vh'
    })
    
])

@app.callback(
    Output('graph', 'figure'),
    [Input('country', 'value')]
)

def update_graph(country):
    df2 = df[df['country']== country]

    data = [go.Scatter(
        x = df2['year'],
        y= df2['gdpPercap'],
        mode = 'markers+lines',
        name = 'GDP (PIB) per person ',
        yaxis= 'y2'
    ),
    go.Scatter(
        x = df2['year'],
        y = df2['lifeExp'],
        mode='markers+lines',
        name = ' Life Experience'
    )]

    layout = go.Layout(
        title= f'Population and Life Experience of {country}',
        title_x = 0.5,
        xaxis= dict(
            title = 'year',
        ),
        yaxis2=dict(
            title='Population',

            overlaying='y',  # Superpose l'axe y2 sur y
            side='right'     # Place l'axe y2 à droite
        ),
        yaxis= dict(
            title = 'Life Experience'
        )
    )

    fig = go.Figure(
        data= data, 
        layout = layout
    )
    return fig

@app.callback(
    Output('fig_compare', 'figure'),
    [Input('multi_country', 'value')]
)

def compare(countries):
    if not countries:
        return go.Figure()
    data =[]
    for country in countries:
        df_temp = df[df['country']== country]
        trace = go.Scatter(
            x = df_temp['year'],
            y = df_temp['gdpPercap'],
            name= country,
            mode='markers+lines'
        )
        data.append(trace)
    layout = go.Layout(
        title='GDP (PIB) per person',
        title_x = 0.5,
        xaxis=dict(
            title='year',
        ),
        yaxis=dict(
            title = 'GAP per person',
        )
    )
    fig_compare = go.Figure(
        data = data, 
        layout = layout
    )

    return fig_compare

# Run the app
if __name__ == '__main__':
    app.run(debug=True)