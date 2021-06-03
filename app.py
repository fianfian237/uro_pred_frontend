import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np
import requests
from flask import Flask



server = Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div(
     children = [
        #Le titre et l'entête de la page
        html.Div(id='header', children=[

                html.H4('Vuroba: Renseignez ci-dessous votre analyse de la tumeur'),


            ], style={

                'width': '100%',

                'border': '1px solid #eee',

                'text-align': 'center',

                'padding': '30px 30px 30px',

                'box-shadow': ' 0 2px 2px #ccc',

                'display': 'inline-block0',

                'verticalAlign': 'top'

            }),

        #Le formulaire du modèle
        html.Div(id='formulaire', children=[
                html.Label('Structure'),
                dcc.Dropdown(
                    id='Structure_dropdown',
                    options=[
                        {'label': 'Exophytic', 'value': 'Exophytic'},
                        {'label': 'Micro-papillary', 'value': 'Micro-papillary'},
                        {'label': 'Flat', 'value': 'Flat'}
                    ],
                    value='Exophytic'
                ),

                html.Label('Size'),
                dcc.Dropdown(
                    id='Size_dropdown',
                    options=[
                        {'label': 'Medium size (1-3cm)', 'value': 'Medium size (1-3cm)'},
                        {'label': 'Small < 1cm', 'value': 'Small < 1cm'},
                        {'label': 'Large > 3cm', 'value': 'Large > 3cm'}
                    ],
                    value='Medium size (1-3cm)'
                ),

                html.Label('Number'),
                dcc.Dropdown(
                    id='Number_dropdown',
                    options=[
                        {'label': 'Single', 'value': 'Single'},
                        {'label': 'Multiple', 'value': 'Multiple'}
                    ],
                    value='Single'
                ),

                html.Label('Lesion margin'),
                dcc.Dropdown(
                    id='Lesion-margin_dropdown',
                    options=[
                        {'label': 'Ill defined', 'value': 'Ill defined'},
                        {'label': 'Well delineated / sharp limits', 'value': 'Well delineated / sharp limits'}
                    ],
                    value='Ill defined'
                ),

                html.Label('Lesion pedicle'),
                dcc.Dropdown(
                    id='Lesion-pedicle_dropdown',
                    options=[
                        {'label': 'Thin (<1/3 tumor diameter)', 'value': 'Thin (<1/3 tumor diameter)'},
                        {'label': 'Sessile', 'value': 'Sessile'},
                        {'label': 'Stout (>1/3 tumor diameter)', 'value': 'Stout (>1/3 tumor diameter)'}
                    ],
                    value='Sessile'
                ),

                html.Label('Lesion fronds'),
                dcc.Dropdown(
                    id='Lesion-fronds_dropdown',
                    options=[
                        {'label': 'Large/ coalescent', 'value': 'Large/ coalescent'},
                        {'label': 'solid tumor', 'value': 'solid tumor'},
                        {'label': 'Thin', 'value': 'Thin'}
                    ],
                    value='Large/ coalescent'
                ),

                html.Label('Vascular architecture of the bladder wall'),
                dcc.Dropdown(
                    id='Vascular-architure-wall_dropdown',
                    options=[
                        {'label': 'Normal, geometric pattern', 'value': 'Normal, geometric pattern'},
                        {'label': 'Tortuous and irregular', 'value': 'Tortuous and irregular'},
                        {'label': 'Increased density', 'value': 'Increased density'}
                    ],
                    value='Increased density'
                ),

                html.Label('Microvascular architecture of the tumor'),
                dcc.Dropdown(
                    id='Microvascular-architecture_dropdown',
                    options=[
                        {'label': 'Large, club-like or ill-defined', 'value': 'Large, club-like or ill-defined'},
                        {'label': 'Not Visible', 'value': 'Not Visible'},
                        {'label': 'Thin vascular fronds', 'value': 'Thin vascular fronds'}
                    ],
                    value='Large, club-like or ill-defined'
                ),

            ], style={'columnCount': 2}),


        #Envoyer la requête http et afficher la réponse
        html.Div(id='results', children=[
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='container-button-basic',
                     children='Submit your diagnostic to get the prediction')
        ])
    ]
)

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('Structure_dropdown', 'value'),
    Input('Size_dropdown', 'value'),
    Input('Number_dropdown', 'value'),
    Input('Lesion-margin_dropdown', 'value'),
    Input('Lesion-pedicle_dropdown', 'value'),
    Input('Lesion-fronds_dropdown', 'value'),
    Input('Vascular-architure-wall_dropdown', 'value'),
    Input('Microvascular-architecture_dropdown', 'value')
    )
def update_output(n_clicks, structure, size, number, lesion_margin,
                  lesion_pedicle, lesion_fronds, vascular_architecture,
                  microvascular_architecture):
    body = {
        'Structure': structure,
        'Size': size,
        'Number': number,
        'Lesion Margin': lesion_margin,
        'Lesion pedicle': lesion_pedicle,
        'Lesion fronds': lesion_fronds,
        'Vascular architecture of the bladder wall': vascular_architecture,
        'Microvascular architecture of the tumor': microvascular_architecture
    }

    url = os.getenv('preduro_backend_url')
    if url is None:
        url = "http://localhost:4000"

    test = None
    response = requests.get(
        url=url + '/predict_grade_n_stade',
        headers={'Content-Type': 'application/json'},
        params=body
    )
    app.logger.info(response.json())
    return 'The tumor you just gave a diagnostic for seems to be a {}_{} tumor'.format(
        response.json()["stade"], response.json()["grade"]
        )


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
