from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash
import json, urllib, requests
import plotly.graph_objects as go
import time
import dash_bootstrap_components as dbc

from data_processing_new import build_scen_data
from sankey_diagram_new import build_sankey



app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.title = "SUES-DIGIT Project"


app.layout = html.Div(
    id="app-container",
    style={ #'background-image': 'url(assets/background.jpg)',
            #'background-size': '100%',
            'weight': '100vw',
            'height': '100vh',
            },
    children=[
        dbc.Row(
            children=[
                dbc.Row(
                    id = "header_area",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H1(
                                            id = "header_title",
                                            children = "SUES-DIGIT"
                                        ),   
                                    ], 
                                    xs=8, sm=8, md=10, lg=10, xl=10, xxl=10
                                ),
                                dbc.Col(
                                    [
                                        html.Img(src="/assets/logoSuis.jpg",height=30),
                                        html.Img(src="/assets/logotyp.jpg",height=30),
                                    ], 
                                    xs=4, sm=4, md=2, lg=2, xl=2, xxl=2
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P(
                                            id = "header-description",
                                            children = "Distribution of energy",
                                        )
                                    ], 
                                    width=12,
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    id = "all_settings_area",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            id = "kommun_column",
                                            children = [
                                                html.Label('Västra Götalands Iän'),
                                                dcc.Dropdown(
                                                    id = "kommun_menu",
                                                    optionHeight = 25,
                                                    maxHeight = 1000,
                                                    options = [ 
                                                        {
                                                            "label" : html.Span(['Skaraborg'], style = {'font-size': 25}),
                                                            "value" : "Skaraborg",
                                                            "disabled" : True 
                                                        } ,
                                                        {
                                                            "label" : html.Span(['Skara kommun'], style = {'padding-left': 40, 'font-size': 20 }),
                                                            "value" : "Skara kommun"
                                                        } ,
                                                        {
                                                            "label" : html.Span(['Skara syd'], style = {'padding-left': 80}),
                                                            "value" : "Skara syd",
                                                            "disabled" : True 

                                                        } ,
                                                        {
                                                            "label" : html.Span(['Skara väst'], style = {'padding-left': 80}),
                                                            "value" : "Skara väst",
                                                            "disabled" : True 
                                                        } ,
                                                        {
                                                            "label" : html.Span(['Lidköping kommun'], style = {'padding-left': 40,'font-size': 20 }),
                                                            "value" : "Lidköping kommun"
                                                        }
                                                    ],
                                                    placeholder = "Select a place...",
                                                )
                                            ]  
                                        )                                         
                                    ], 
                                    xs=6, sm=6, md=6, lg=6, xl=6, xxl=6
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            id = "year_column",
                                            children = [
                                                html.Label("Year:"),
                                                dcc.Dropdown(
                                                    id = "years",
                                                    optionHeight = 20,
                                                    maxHeight = 500,
                                                    options = [
                                                        {'label' : '2023', 'value' : '0' },
                                                        {'label' : '2024', 'value' : '1' },
                                                        {'label' : '2025', 'value' : '2' },
                                                        {'label' : '2026', 'value' : '3' },
                                                        {'label' : '2027', 'value' : '4' },
                                                        {'label' : '2028', 'value' : '5' },
                                                        {'label' : '2029', 'value' : '6' },
                                                        {'label' : '2030', 'value' : '7' },
                                                        {'label' : '2031', 'value' : '8' },
                                                        {'label' : '2032', 'value' : '9' },
                                                        {'label' : '2033', 'value' : '10' }
                                                    ],
                                                    placeholder = "Select a year...",
                                                ),
                                            ]
                                        )
                                    ], 
                                    xs=3, sm=3, md=3, lg=3, xl=3, xxl=3
                                ),
                                dbc.Col(
                                    [
                                        html.Label(""),
                                        html.Div(
                                            id = "peak",
                                            children = [
                                                dcc.Checklist(
                                                    id = "peak_hour",
                                                    options=[
                                                        {
                                                            "label": [
                                                                html.Img(src="/assets/imagen.jpg",height=30),
                                                                html.Span("Peak hour")
                                                            ],
                                                            'value': "on",
                                                        }
                                                    ]
                                                )
                                            ]
                                        )
                                    ], 
                                    xs=3, sm=3, md=3, lg=3, xl=3, xxl=3
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            id = "scenario_menu_column",
                                            children = [
                                                html.Label("Choose a scenario:"),
                                                dcc.Dropdown(
                                                    id = "scenario_menu",
                                                    options = [
                                                        {'label' : 'Scenario 1 - Ratio of EVs', 'value' : "1" },
                                                        {'label' : 'Scenario 2 - New industry establishment NIE', 'value' : "2" },
                                                        {'label' : 'Scenario 3 - New Houses - Ratio New houses DHP user', 'value' : "3" },
                                                        {'label' : 'Scenario 4 - Users apartment buildings - Goal ratio DHP users small houses', 'value' : "4" },
                                                        {'label' : 'Scenario 5 - Number large solar panel projects', 'value' : "5" },
                                                        {'label' : 'Scenario 6 - Number large wind mill projects', 'value' : "6" },
                                                        {'label' : 'Scenario All', 'value' : "7" }
                                                    ],
                                                    placeholder = "Select a scenario..."
                                                )
                                            ]
                                        )
                                    ], 
                                    xs=9, sm=9, md=9, lg=9, xl=9, xxl=9
                                ),
                                dbc.Col(
                                    [
                                        html.Label(""),
                                        html.Div(
                                            id = "units_menu",
                                            children = [
                                                dcc.Dropdown(
                                                    id = "unit",
                                                    options = [
                                                        {'label' : 'Kwh', 'value' : 'kilo' },
                                                        {'label' : 'Mwh', 'value' : 'mega' },
                                                        {'label' : 'Gwh', 'value' : 'giga' }
                                                    ],
                                                    value='giga'
                                                )
                                            ]
                                        )
                                    ], 
                                    xs=3, sm=3, md=3, lg=3, xl=3, xxl=3
                                ),
                            ]
                        ),
                        dbc.Row(
                            [                                
                                dbc.Col(
                                    [                                        
                                        dcc.Markdown(
                                            id="slider_scale",
                                            children ="Select a value:",
                                            style = {"textAlign" : "left"}
                                        ),
                                        html.Div(
                                            id = "invisible_slider",
                                            style = {'display' : 'none'},
                                            children = [
                                                dcc.Markdown(
                                                    id="slider_scale2a",
                                                    children ="New houses", 
                                                    style = {"textAlign" : "left",'display' : 'none'}   
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            id = "invisible_slider2",
                                            style = {'display' : 'none'},
                                            children = [
                                                dcc.Markdown(
                                                    children ="New houses", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="3",
                                                    min=100,
                                                    max=300,
                                                    step=100,
                                                    value=[None,None],
                                                ),                                                        
                                                dcc.Markdown(
                                                    children ="Ratio new houses DHP user", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="31",
                                                    min=0.5,
                                                    max=1,
                                                    step=0.25,
                                                    value=[None,None],
                                                ),
                                                dcc.Markdown(
                                                    children ="Goal ratio DHP users small houses", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="4",
                                                    min=0.5,
                                                    max=1,
                                                    step=0.25,
                                                    value=[None,None],
                                                ),
                                                dcc.Markdown(
                                                    children ="Goal ratio DHP users apartment buildings", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="41",
                                                    min=0.96,
                                                    max=1,
                                                    step=0.04,
                                                    value=[None,None],
                                                ),                                                            
                                                dcc.Markdown(
                                                    children ="Number large solar panel projects", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="5",
                                                    min=6,
                                                    max=12,
                                                    step=3,
                                                    value=[None,None],
                                                ),
                                                dcc.Markdown(
                                                    children ="Number large wind mill projects", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.RangeSlider(
                                                    id="6",
                                                    min=0,
                                                    max=2,
                                                    step=1,
                                                    value=[None,None],
                                                ),
                                            ]
                                        )                                    
                                    ], 
                                    xs=3, sm=3, md=3, lg=3, xl=3, xxl=3
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            id = "scenario_slider_column",
                                            children = [
                                                html.Div(
                                                    children = [                                                            
                                                        dcc.RangeSlider(
                                                            id="slider",
                                                            min=0,
                                                            max=1,
                                                            step=0.05,
                                                            value=[None,None],
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    id = "invisible_slider3",
                                                    style = {'display' : 'none'},
                                                    children = [                                                        
                                                        dcc.RangeSlider(
                                                            min=0,
                                                            max=1,
                                                            step=0.25,
                                                            value=[None,None],
                                                            id="slider2",
                                                        ),
                                                    ]
                                                ),    
                                                html.Div(
                                                    id = "invisible_slider4",
                                                    style = {'display' : 'none'},
                                                    children = [
                                                        
                                                        dcc.RangeSlider(
                                                            id="3",
                                                            min=100,
                                                            max=300,
                                                            step=100,
                                                            value=[None,None],
                                                        ), 
                                                        dcc.RangeSlider(
                                                            id="31",
                                                            min=0.5,
                                                            max=1,
                                                            step=0.25,
                                                            value=[None,None],
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="4",
                                                            min=0.5,
                                                            max=1,
                                                            step=0.25,
                                                            value=[None,None],                                                    
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="41",
                                                            min=0.96,
                                                            max=1,
                                                            step=0.04,
                                                            value=[None,None],
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="5",
                                                            min=6,
                                                            max=12,
                                                            step=3,
                                                            value=[None,None],
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="6",
                                                            min=0,
                                                            max=2,
                                                            step=1,
                                                            value=[None,None],
                                                        ),
                                                    ]
                                                )                                                
                                            ]
                                        ),
                                    ], 
                                    xs=7, sm=7, md=7, lg=7, xl=7, xxl=7
                                ),
                            ]
                        ),
                    ]   
                ), 
            ]
        ),
        html.Hr(),
        dbc.Row(
            id = "graph_area",
            children=[ 
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(                     
                                    children = [
                                        html.P(id="text_sum_energy_production", children="Sum Energy Production"),
                                        html.P(id="sum_energy_production")
                                    ]
                                ),
                            ], 
                            xs=6, sm=6, md=6, lg=6, xl=6, xxl=6
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    children=[
                                        html.P(id="text_sum_energy_usage", children="Sum Energy Usage "),
                                        html.P(id="sum_energy_usage")
                                    ]
                                ),
                                html.Data(
                                    id= "actual_unit",
                                    style = {'display':'none'}
                                ),
                            ], 
                            xs=6, sm=6, md=6, lg=6, xl=6, xxl=6
                        ),
                    ], 
                ),                        
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                #valor tabla    
                            ], 
                            xs=2, sm=2, md=2, lg=2, xl=2, xxl=2
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    id="graph-container", 
                                    style = {'display' : 'none'},
                                    children = [ 
                                    dcc.Graph(
                                        id = "graph",
                                        )
                                    ]
                                ),
                            ], 
                            xs=8, sm=8, md=8, lg=8, xl=8, xxl=8
                        ),
                        dbc.Col(
                            [
                                #valor tabla    
                            ], 
                            xs=2, sm=2, md=2, lg=2, xl=2, xxl=2
                        ),
                    ], 
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                #valor tabla   
                            ], 
                            xs=2, sm=2, md=2, lg=2, xl=2, xxl=2
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    id="graph-container2", 
                                    style = {'display' : 'none'},
                                    children = [ 
                                    dcc.Graph(
                                        id = "graph2",
                                        )
                                    ]
                                )       
                            ], 
                            xs=8, sm=8, md=8, lg=8, xl=8, xxl=8
                        ),
                        dbc.Col(
                            [
                                #valor tabla   
                            ], 
                            xs=2, sm=2, md=2, lg=2, xl=2, xxl=2
                        ),
                    ], 
                ),
            ]
        ),    
    ]
)
        


if __name__ == "__main__":
    app.run(debug=True)