# Import packages
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("https://raw.githubusercontent.com/yvesdeum/neues-repo/main/gapminderDataFiveYear.csv")
pibpa = pd.read_csv("https://raw.githubusercontent.com/yvesdeum/neues-repo/main/pibpa.csv")


columns = pd.to_numeric(pibpa.columns, errors='coerce')
columns = columns.dropna()
columns = [int(x) for x in columns]

app = Dash(__name__)

markdown_text = '''
>
>Sur cette Realisé  par *[Yves Deumeni Wandji] (mailto:y.deumeni@outlook.de) * Vous avez 2 graphiques:
>
* Le premier réprésente la population et l'espérence de vie du pays que vous avez sélectioné dans un même graphique. Les Données vont Malheureusement seulement de 1950 à 2010 pour ce graphique.
* Le Deuximeme Graphique affiche l'évolution du PIB par habitant du ou des pays sélectionnés. Les Données ici vont de 1990 à 2023. Vous pouvez choisir la plage d'année qui vous intéresse ici.
>
*__NB__:* Après un zoom sur un graphique, il peut être utile d'utiliser le boutton __*Home*__ (emoji maison) en haut à droite du graphe pour réinitialiser les axes.



'''
app.layout= html.Div([
    html.H1(children='Population, Esperence de Vie et Pib Par habitant', style=dict(textAlign = 'center')),
    
    dcc.Markdown(children= markdown_text),
    html.H3(children='Graphique 1'),
    html.Div(children = "Please, select a country ", style= dict(margin = '10px')),
    html.Div([
        dcc.Dropdown(
        id = 'country',
        options=[{'label': x, 'value': x} for x in df['country'].dropna().unique().tolist()],
        value= 'Cameroon'
    ),
    ], style={'width': '38%'}),
    
    dcc.Graph(id='graph'),
    html.H3(children='Graphique 2'),
    html.Div([
        dcc.Markdown(children="Veuillez choisir un ou plusieurs pays"),
        dcc.Dropdown(
        id = 'multi_country',
        options=[{'label': x, 'value': x} for x in pibpa['Country Name'].dropna().unique().tolist()],
        #value= 'Algeria',
        multi=True
    ),], style={'width': '38%','display': 'inline-block','padding': 10}),
    html.Div([
        dcc.Markdown(children="Veuillez choisir l'année minimale"),
        dcc.Dropdown(
        id = 'min-year',
        options=[{'label': x, 'value': x} for x in columns],
        value = min(columns),
        multi=False
    ),], style={'width': '15%','display': 'inline-block','padding': 10}),
    html.Div([
        dcc.Markdown(children="Veuillez choisir l'année maximale"),
        dcc.Dropdown(
        id = 'max-year',
        options=[{'label': x, 'value': x} for x in columns],
        value = max(columns),
        multi=False
    ),], style={'width': '15%','display': 'inline-block','padding': 10}),
    
    html.Div([
        dcc.Graph(id='fig_compare'),
    ], style={
        'height': '80vh'
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
        name = 'Esperence de vie'
    )]

    layout = go.Layout(
        title= f'Population et esperence de vie du {country}',
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
            title = 'Esperence de vie'
        )
    )

    fig = go.Figure(
        data= data, 
        layout = layout
    )
    return fig

@app.callback(
    Output('fig_compare', 'figure'),
    [Input('multi_country', 'value'),
     Input('min-year', 'value'),
     Input('max-year', 'value')]
)

def compare(countries,min_y, max_y):
    if not countries:
        return go.Figure()
    data =[]
    for country in countries:
        df_temp = pibpa[pibpa['Country Name']== country]
        df_temp = df_temp.iloc[0,4:]
        df_temp = df_temp.loc[str(min_y):str(max_y)]
        y = pd.to_numeric(df_temp)
        y = y.tolist()
        trace = go.Scatter(
            x= df_temp.index.tolist(),
            y = y,
            name= country,
            mode='markers+lines'
        )
        data.append(trace)
    layout = go.Layout(
        title='PIB par habitant',
        title_x = 0.5,
        xaxis=dict(
            title='Années',
        ),
        yaxis=dict(
            title = 'PIB par habitant',
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