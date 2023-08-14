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
            'padding-left': 40 ,
            'padding-right' : 40,
            },
    children=[
        dbc.Row(
            id = "top_area",
            style={#'background-image': 'url(assets/1.jpg)',
                   'background-color' : 'rgba(0, 255, 255, 0.1)',
                   'background-size': '100%',
                   #'weight': '100vw',
                   #'height': '20vh',
                   },
            children=[
                dbc.Row(                    
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H1(
                                            id = "header_title",
                                            children = "SUES-DIGIT",
                                            style = {"textAlign" : "center", "font-weight": "bold" },
                                        ),   
                                    ], 
                                    xs=7, sm=7, md=7, lg=7, xl=7, xxl=7
                                ),
                                dbc.Col(
                                    id="logos",
                                    children=[
                                        html.Img(src="/assets/logoSuis.png",height=70),
                                        html.Img(src="/assets/logoSkaraborgs.png",height=70),
                                        html.Img(src="/assets/logoUni.png",height=70),
                                        
                                    ], 
                                    xs=4, sm=4, md=4, lg=4, xl=4, xxl=4
                                ),
                                dbc.Col(                                    
                                    [
                                        html.Div(
                                            id = "language",
                                            style={"width": "60%", },
                                            children = [                                                
                                                dcc.Dropdown(
                                                    optionHeight = 20,   
                                                    maxHeight = 500,                                                                                                     
                                                    options = [
                                                        {'label' : 'EN', 'value' : 'EN' },
                                                        {'label' : 'Sv', 'value' : 'Sv' },                                                          
                                                    ],
                                                    value = "EN",
                                                ),
                                            ]
                                        )
                                    ], 
                                    xs=1, sm=1, md=1, lg=1, xl=1, xxl=1
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
                                            style = {"font-weight": "bold" },
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
                                                html.Label('Västra Götalands Iän',style = {"font-weight": "bold" }),
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
                                                html.Label("Year:",style = {"font-weight": "bold" },),
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
                                        html.Div(
                                            id = "peak",
                                            children = [
                                                dcc.Checklist(
                                                    id = "peak_hour",
                                                    style = {"font-weight": "bold" },
                                                    options=[
                                                        {'label': 'Peak hour:', 'value': 'on'},
                                                    ],
                                                                                                                                                             
                                                ),                                                
                                                html.Div(
                                                id = "wintersummer",
                                                style = {'display' : 'none'},
                                                children = [
                                                    dcc.RadioItems([                                                    
                                                            {
                                                                "label":
                                                                    [
                                                                        html.Img(src="/assets/winter.png",height=30),
                                                                        html.Span(" Winter"),
                                                                    ],
                                                                "value": "Winter",
                                                            },
                                                            {
                                                                "label":
                                                                    [
                                                                        html.Img(src="/assets/Sun.png",height=30),
                                                                        html.Span(" Summer"),
                                                                    ], 
                                                                "value": "Summer",
                                                            },
                                                            
                                                        ], 
                                                        inline=True, 
                                                        labelStyle={ "align-items": "center"},
                                                    ),
                                                ],
                                                ),
                                            ], 
                                        )
                                    ], xs=3, sm=3, md=3, lg=3, xl=3, xxl=3
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
                                                html.Label("Choose a scenario:",style = {"font-weight": "bold" },),
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
                                        html.Label("Select a value:",style = {"font-weight": "bold" },),
                                        dcc.Markdown(
                                            id="slider_scale",
                                            children ="",
                                            style = {"textAlign" : "left"}
                                        ),
                                        html.Div(
                                            id = "invisible_slider_scale",
                                            style = {'display' : 'none'},
                                            children = [
                                                dcc.Markdown(
                                                    id="slider_scale2",
                                                    children ="New houses", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            id = "invisible_slider2_scale",
                                            style = {'display' : 'none'},
                                            children = [
                                                dcc.Markdown(
                                                    children ="New houses", 
                                                    style = {"textAlign" : "left"}   
                                                ),                                                   
                                                dcc.Markdown(
                                                    children ="Ratio new houses DHP user", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.Markdown(
                                                    children ="Goal ratio DHP users small houses", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.Markdown(
                                                    children ="Goal ratio DHP users apartment buildings", 
                                                    style = {"textAlign" : "left"}   
                                                ),                                                       
                                                dcc.Markdown(
                                                    children ="Number large solar panel projects", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.Markdown(
                                                    children ="Number large wind mill projects", 
                                                    style = {"textAlign" : "left"}   
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
                                                    id = "invisible_slider_values",
                                                    style = {'display' : 'none'},
                                                    children = [                                                        
                                                        dcc.RangeSlider(
                                                            id="slider2",
                                                            min=0,
                                                            max=1,
                                                            step=0.25,
                                                            value=[None,None],
                                                            
                                                        ),
                                                    ]
                                                ),    
                                                html.Div(
                                                    id = "invisible_slider2_values",
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
                                html.Div(
                                    id= "actual_unit",
                                    style = {'display':'none'},
                                    children =["Gw"],
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
                            xs=1, sm=1, md=1, lg=1, xl=1, xxl=1
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
                            xs=10, sm=10, md=10, lg=10, xl=10, xxl=10
                        ),
                        dbc.Col(
                            [
                                #valor tabla    
                            ], 
                            xs=1, sm=1, md=1, lg=1, xl=1, xxl=1
                        ),
                    ], 
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(                     
                                    children = [
                                        html.P(id="text_sum_energy_production2", children="Sum Energy Production "),
                                        html.P(id="sum_energy_production2")
                                    ]
                                ),
                            ], 
                            xs=6, sm=6, md=6, lg=6, xl=6, xxl=6
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    children=[
                                        html.P(id="text_sum_energy_usage2", children="Sum Energy Usage "),
                                        html.P(id="sum_energy_usage2")
                                    ]
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

# Assign properties to the sliders

@app.callback(
    
    Output("slider_scale", "children"),
    Output("invisible_slider_scale", "style"), 
    Output("slider_scale2", "children"),
    Output("invisible_slider2_scale", "style"),
    Output("invisible_slider_values", "style"), 
    Output("invisible_slider2_values", "style"),
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "step"),
    Output("slider2", "min"),
    Output("slider2", "max"),
    Output("slider2", "step"), 

    Output("slider", "value"),
    Output("slider2", "value"),
    Output("3", "value"),
    Output("31", "value"),
    Output("4", "value"),
    Output("41", "value"),
    Output("5", "value"),
    Output("6", "value"),

    Input("scenario_menu", "value"),

    State("slider", "min"),
    State("slider", "max"),
    State("slider", "step"),
    State("slider2", "min"),
    State("slider2", "max"),
    State("slider2", "step"),
    State("slider", "value"),
    State("slider2", "value"),
    State("3", "value"),
    State("31", "value"),
    State("4", "value"),
    State("41", "value"),
    State("5", "value"),
    State("6", "value"),

    )

def update_output(value,min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6):
    if value == "1": 
        style = style_slider = {'display':'none'}
        style2 = style_slider2 = {'display':'none'} 
        min=0
        max=1
        step=0.05
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        
        return (f"Ratio of EVs", style, f"", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6) 
    if value == "2": 
        style = style_slider = {'display':'none'}
        style2 = style_slider2 = {'display':'none'}
        min=0
        max=3
        step=1
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        
        return (f"New industry establishment NIE", style, f"", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6)   
    if value == "3":  
        style = style_slider ={'display':'block'}
        style2 = style_slider2 = {'display':'none'}
        min=0
        max=300
        step=25
        min2=0
        max2=1
        step2=0.25
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        
        return (f"New houses", style, f"Ratio new houses DHP user", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6)
    if value == "4":  
        style = style_slider ={'display':'block'}
        style2 = style_slider2 ={'display':'none'}
        min=0.2
        max=1
        step=0.1
        min2=0.96
        max2=1
        step2=0.01
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
       
        return (f"Goal ratio DHP users small houses", style, f"Goal ratio DHP users apartment buildings", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6)
    if value == "5":  
        style = style_slider ={'display':'none'}
        style2 = style_slider2 ={'display':'none'}
        min=0
        max=12
        step=1
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]

        return (f"Number large solar panel projects", style, f"", style2, style_slider, style_slider2, min, max, step, min2, max2, step2,val, val2, val3, val31, val4, val41, val5, val6)
    if value == "6":  
        style = style_slider ={'display':'none'}
        style2 = style_slider2 = {'display':'none'}
        min=0
        max=2
        step=1
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        
        return (f"Number large wind mill projects", style, f"", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6)
    if value == "7":  
        style = style_slider ={'display':'block'}
        style2 = style_slider2 = {'display':'block'}
        min=0.5
        max=1
        step=0.25  
        min2=0
        max2=2
        step2=1
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        
        return (f"Ratio of EVs", style, f"New industry establishment NIE", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6 )


@app.callback(
    Output("unit", "options"),
    Output("wintersummer", "style"),
    Input("peak_hour", "value")
)

def unit_menu(value):
    
    if value == ['on']:
        options = [
            {'label' : 'Kw', 'value' : 'kilo' },
            {'label' : 'Mw', 'value' : 'mega' },
            {'label' : 'Gw', 'value' : 'giga' }
        ]
        style = {'display':'block'}

        return options, style
    else: 
        options = [
            {'label' : 'Kwh', 'value' : 'kilo' },
            {'label' : 'Mwh', 'value' : 'mega' },
            {'label' : 'Gwh', 'value' : 'giga' }
        ]
        style = {'display':'none'}

        return options, style
    

@app.callback(
    Output("text_sum_energy_production", "children"),
    Output("text_sum_energy_usage", "children"),
    Output("actual_unit", "children"),
    Input("peak_hour", "value"),
    Input("unit", "value")
)

def update_sum_unit(check_item, units):
    if check_item == ['on']: 
        if units == 'kilo':
            return f"Sum Energy Production (KW):", f"Sum Energy Usage (KW):", f"KW"
        if units == 'mega':
            return f"Sum Energy Production (MW):", f"Sum Energy Usage (MW):", f"MW"
        if units == 'giga':
            return f"Sum Energy Production (GW):", f"Sum Energy Usage (GW):", f"GW"
    else: 
        if units == 'kilo':
            return  f"Sum Energy Production (KWh):", f"Sum Energy Usage (KWh):", f"KWh"
        if units == 'mega':
            return  f"Sum Energy Production (MWh):", f"Sum Energy Usage (MWh):", f"MWh"
        if units == 'giga':
            return  f"Sum Energy Production (GWh):", f"Sum Energy Usage (GWh):", f"GWh"
        

# SELECT THE URL OF EACH SCENARIO CASE
url_scenarios_cases = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/Scenarios_cases3.json' 
response_scenario_cases = urllib.request.urlopen(url_scenarios_cases)
info_scenarios_cases = json.loads(response_scenario_cases.read())

s_e_production2 = 0
s_e_usage2 = 0

@app.callback(
    Output("graph", "figure"),
    Output("graph2", "figure"),
    Output("sum_energy_production", "children"),
    Output("sum_energy_usage", "children"),
    Output("graph-container", 'style'),
    Output("graph-container2", 'style'),
    Input("kommun_menu", "value"),
    Input("scenario_menu", "value"),
    Input("years", "value"),
    Input("slider","value"),
    Input("slider2","value"),
    Input("peak_hour", "value"),
    Input("unit", "value"),
    Input("actual_unit", "children"),
)

def display_sankey(kommun,scenario,years,value_slider,value_slider2, peak_hour, unit, actual_unit):

    if (kommun is None) or (scenario is None) or (years is None) or (value_slider is None):
        raise PreventUpdate
        return
    
    else:
        print("")
        print("")
        print("")
        print("NEW SIMULATION")
        print("")
        print("")
        print("")

        print(kommun)
        print(scenario)
        print(years)
        print(value_slider[0])
        print(value_slider[1])
        print(value_slider2)
        print(value_slider2)
        print(peak_hour)
        print(unit)
        print(actual_unit)
        #print(info_scenarios_cases[kommun][scenario])

        # Save the correct excel file
        scen_file = pd.read_csv(info_scenarios_cases[kommun][scenario])
    
        # Create a dictionary with the information selected 
        (scen_data, s_e_production, s_e_usage) = build_scen_data(scen_file, years, scenario,value_slider[0],value_slider2, peak_hour, unit, kommun)
        (scen_data2, s_e_production2, s_e_usage2) = build_scen_data(scen_file, years, scenario,value_slider[1],value_slider2, peak_hour, unit, kommun)

        # Display a sankey diagram with the information
        fig = build_sankey(scen_data, actual_unit)
        fig.update_layout()

        fig2 = build_sankey(scen_data2, actual_unit)
        fig2.update_layout()

        return fig, fig2, s_e_production, s_e_usage, {'display':'block'}, {'display':'block'}
    





if __name__ == "__main__":
    app.run(debug=True)