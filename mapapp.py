import json
import pandas as pd
import plotly.express as px  # (version 4.7.0 or^)
from dash import Dash, dcc, html, Input, Output  # (version 2.0.0 or^)

app = Dash(__name__)

df = pd.read_csv('totalsdata_2016-2020.csv')
with open('usgeomap.json') as file:
    mapdata = json.load(file)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("SSBG Data Dashboard", style={'text-align': 'center'}),

    dcc.RadioItems(id='slct_year',
                   options=[
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                     value=2020,
                     inline=True),

    dcc.Dropdown(id="slct_servicecategory",
                 options=[
                     {"label": "All Services", "value": 32},
                     {"label": "Adoption Services", "value": 1},
                     {"label": "Case Management", "value": 2},
                     {"label": "Congregate Meals", "value": 3},
                     {"label": "Counseling Services", "value": 4},
                     {"label": "Day Care - Adults", "value": 5},
                     {"label": "Day Care - Children", "value": 6},
                     {"label": "Education and Training Services", "value": 7},
                     {"label": "Employment Services", "value": 8},
                     {"label": "Family Planning Services", "value": 9},
                     {"label": "Foster Care Services - Adults", "value": 10},
                     {"label": "Foster Care Services - Children", "value": 11},
                     {"label": "Health-Related Services", "value": 12},
                     {"label": "Home-Based Services", "value": 13},
                     {"label": "Home-Delivered Meals", "value": 14},
                     {"label": "Housing Services", "value": 15},
                     {"label": "Independent/Transitional Living Services", "value": 16},
                     {"label": "Information and Referral", "value": 17},
                     {"label": "Legal Services", "value": 18},
                     {"label": "Pregnancy and Parenting", "value": 19},
                     {"label": "Prevention and Intervention", "value": 20},
                     {"label": "Protective Services - Adults", "value": 21},
                     {"label": "Protective Services - Children", "value": 22},
                     {"label": "Recreation Services", "value": 23},
                     {"label": "Residential Treatment", "value": 24},
                     {"label": "Special Services - Disabled", "value": 25},
                     {"label": "Special Services - Youth at Risk", "value": 26},
                     {"label": "Substance Abuse Services", "value": 27},
                     {"label": "Transportation", "value": 28},
                     {"label": "Other Services", "value": 29}],
                 multi=False,
                 value=32,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='SSBG_map', figure={})

])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='SSBG_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_servicecategory', component_property='value')
    ]   
)
def update_graph(year_selected, service_selected):
    container = ""

    dff = df.copy()
    dff = dff[dff["Year"] == year_selected]
    dff = dff[dff["Line Num"] == service_selected]

    # Plotly Express
    fig = px.choropleth(
        dff,
        locations='id',
        color='Total SSBG Expenditures',
        geojson=mapdata,
        title='Total SSBG Expenditures by State',
        scope='usa',
        hover_data=['State Name','Total SSBG Expenditures'],
        color_continuous_scale=px.colors.sequential.Purp,
        template='plotly_dark',
        animation_frame='Year'
    )

    return container, fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
