from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import json, urllib, requests
import plotly.graph_objects as go
import time
import dash_bootstrap_components as dbc

from B_data_processing import build_scen_data
from C_sankey_diagram import build_sankey


app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.title = "SUES-DIGIT Project"

# + All the code inside app.layout defines the objects that are shown in the web page

# -> + html.Div is the general object, in this project we use it to define different areas,
#       it has a lot of attributes to define it, some of the attributes explained are common to all objects:
#       - id (optional): gives a name to the specific object, it is neccesary if we want to use their values
#       because we have to call it (callback).
#       - children: objects inside this area.
#       - style: used to define sizes, alignments, colors,...
# -> html.H1 displays the text in children, H1 is the biggest size there is also H2..H5
# -> html.P displays a paragraph 
# -> html.Label('text') a fast way to display text
# -> + dcc.Dropdown displays a dropdown where you can choose between the options and it will 
#       give a value (callback). There are different ways to define "options". "placeholder"
#       is the message that appears before select any option.
# -> dcc.Checklist the square box to select
# -> dcc.Markdown text that can change the text (callback)
# -> + dcc.Slider or dcc.RangeSlider sliders that gives 1 or 2 values:
#       - min: minimun value
#       - max: maximun value
#       - step
#       - value: initial value, for Slider 1 value, for RangeSlider a list with 2 values [a,b]
# -> + dcc.Graph object to display a graph it is only necessary the "id" to do the callback
#       and send the graphic done later. If it is wanted to not show anything before chosing 
#       variable values it has to be inside a html.Div with: style = {'display' : 'none'}


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
                                        html.Img(src="/assets/logoSuis.png",height=70, style={'margin' : '10px' }),
                                        html.Img(src="/assets/logoSkaraborgs.png",height=70, style={'margin' : '10px' }),
                                        html.Img(src="/assets/logoUni.png",height=70, style={'margin' : '10px' }),
                                        
                                    ], 
                                    xs=4, sm=4, md=4, lg=4, xl=4, xxl=4
                                ),
                                dbc.Col(                                    
                                    [
                                        html.Div(
                                            id = "language",
                                            style={"width": "100%", },
                                            children = [                                                
                                                dcc.Dropdown(
                                                    optionHeight = 20,   
                                                    maxHeight = 500,                                                                                                     
                                                    options = [    
                                                        {
                                                            "label": html.Span(
                                                                [
                                                                    html.Img(src="/assets/english.png", height=20),
                                                                    html.Span("EN"),
                                                                ], style={'align-items': 'center', 'justify-content': 'center'}
                                                            ),
                                                            "value": "EN",
                                                        },  
                                                        {
                                                            "label": html.Span(
                                                                [
                                                                    html.Img(src="/assets/sweden.png", height=20),
                                                                    html.Span("SV"),
                                                                ], style={'align-items': 'center', 'justify-content': 'center'}
                                                            ),
                                                            "value": "SV",
                                                        },                                                      
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
                                                            "value" : "Skara"
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
                                                            "value" : "Lidköping"
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
                                                        {'label': 'Peak hour:', 'value': "PeakHourW"},
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
                                                        {'label' : 'Scenario All', 'value' : "All" }
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
                                                        {'label' : 'kWh', 'value' : 'kilo' },
                                                        {'label' : 'MWh', 'value' : 'mega' },
                                                        {'label' : 'GWh', 'value' : 'giga' }
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
                                                    children ="Goal ratio DHP users apartment buildings", 
                                                    style = {"textAlign" : "left"}   
                                                ),
                                                dcc.Markdown(
                                                    children ="Goal ratio DHP users small houses", 
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
                                                            min=0.96,
                                                            max=1,
                                                            step=0.04,
                                                            value=[None,None],                                                   
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="41",
                                                            min=0.75,
                                                            max=1,
                                                            step=0.25,
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
            style = {'display':'none'},
            children=[ 
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(         
                                    style = {"textAlign" : "center"},            
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
                                    style = {"textAlign" : "center"},
                                    children=[
                                        html.P(id="text_sum_energy_usage", children="Sum Energy Usage "),
                                        html.P(id="sum_energy_usage")
                                    ]
                                ),
                                html.Div(
                                    id= "actual_unit",
                                    style = {'display':'none'},
                                    children =["GW"],
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
                                    style = {"textAlign" : "center"},                    
                                    children = [
                                        html.P(id="text_sum_energy_production2", children="Sum Energy Production 2"),
                                        html.P(id="sum_energy_production2")
                                    ]
                                ),
                            ], 
                            xs=6, sm=6, md=6, lg=6, xl=6, xxl=6
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    style = {"textAlign" : "center"},
                                    children=[
                                        html.P(id="text_sum_energy_usage2", children="Sum Energy Usage 2"),
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
        min=0.96
        max=1
        step=0.01
        min2=0.2
        max2=1
        step2=0.1
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
       
        return (f"Goal ratio DHP users apartment buildings", style, f"Goal ratio DHP users small houses", style2, style_slider, style_slider2, min, max, step, min2, max2, step2, val, val2, val3, val31, val4, val41, val5, val6)
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
    if value == "All":  
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
    
    if value == ['PeakHourW']:
        options = [
            {'label' : 'kW', 'value' : 'kilo' },
            {'label' : 'MW', 'value' : 'mega' },
            {'label' : 'GW', 'value' : 'giga' }
        ]
        style = {'display':'block'}

        return options, style
    else: 
        options = [
            {'label' : 'kWh', 'value' : 'kilo' },
            {'label' : 'MWh', 'value' : 'mega' },
            {'label' : 'GWh', 'value' : 'giga' }
        ]
        style = {'display':'none'}

        return options, style
    

@app.callback(
    Output("text_sum_energy_production", "children"),
    Output("text_sum_energy_usage", "children"),
    Output("text_sum_energy_production2", "children"),
    Output("text_sum_energy_usage2", "children"),
    Output("actual_unit", "children"),
    Input("peak_hour", "value"),
    Input("unit", "value")
)

def update_sum_unit(check_item, units):
    if check_item == ['PeakHourW']: 
        if units == 'kilo':
            return f"Sum Energy Production (kW):", f"Sum Energy Usage (kW):", f"Sum Energy Production 2 (kW):", f"Sum Energy Usage 2 (kW):", f"kW"
        if units == 'mega':
            return f"Sum Energy Production (MW):", f"Sum Energy Usage (MW):", f"Sum Energy Production 2 (MW):", f"Sum Energy Usage 2 (MW):", f"MW"
        if units == 'giga':
            return f"Sum Energy Production (GW):", f"Sum Energy Usage (GW):", f"Sum Energy Production 2 (GW):", f"Sum Energy Usage 2 (GW):", f"GW"
    else: 
        if units == 'kilo':
            return  f"Sum Energy Production (kWh):", f"Sum Energy Usage (kWh):", f"Sum Energy Production 2 (kWh):", f"Sum Energy Usage 2 (kWh):", f"kWh"
        if units == 'mega':
            return  f"Sum Energy Production (MWh):", f"Sum Energy Usage (MWh):", f"Sum Energy Production 2 (MWh):", f"Sum Energy Usage 2 (MWh):", f"MWh"
        if units == 'giga':
            return  f"Sum Energy Production (GWh):", f"Sum Energy Usage (GWh):", f"Sum Energy Production 2 (GWh):", f"Sum Energy Usage 2 (GWh):", f"GWh"
        

@app.callback(
    Output("graph", "figure"),
    Output("graph2", "figure"),
    Output("sum_energy_production", "children"),
    Output("sum_energy_usage", "children"),
    Output("sum_energy_production2", "children"),
    Output("sum_energy_usage2", "children"),
    Output("graph_area", "style"),

    Input("kommun_menu", "value"),
    Input("scenario_menu", "value"),
    Input("years", "value"),
    Input("slider","value"),
    Input("slider2","value"),
    Input("3", "value"),
    Input("31", "value"),
    Input("4", "value"),
    Input("41", "value"),
    Input("5", "value"),
    Input("6", "value"),
    Input("peak_hour", "value"),
    Input("unit", "value"),
    Input("actual_unit", "children"),
)

def display_sankey(kommun,scenario,years,value_slider,value_slider2,v_s3,v_s31,v_s4,v_s41,v_s5,v_s6, peak_hour, unit, actual_unit):

    if (kommun is None) or (scenario is None) or (years is None) or (value_slider is None):
        raise PreventUpdate
        return
    
    else:
        print("")
        print("")
        print("")
        print("NEW SIMULATION AAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print("")
        print("")
        print("")

        print(kommun)
        print(scenario)
        print(years)
        print(value_slider)
        print(value_slider2)
        print(v_s3)
        print(v_s31)
        print(v_s4)
        print(v_s41)
        print(v_s5)
        print(v_s6)
        print(peak_hour)
        #print(type(peak_hour))
        print(unit)
        print(actual_unit)
        #print(info_scenarios_cases[kommun][scenario])

        # Save the correct excel file
        #scen_file = pd.read_csv("Latest Folder\Scenarios/vensim_data_Scen1_Skara_ver4.csv")

        #if peak_hour == ['PeakHourW'] or ['PeakHourS'] :
        if peak_hour == ['PeakHourW']:
            scen_file = pd.read_csv("Scenarios/vensim_data_Scen"+scenario+"_"+peak_hour[0]+"_"+kommun+"_ver.csv" )
        else:
            scen_file = pd.read_csv("Scenarios/vensim_data_Scen"+scenario+"_"+kommun+"_ver.csv" )


        # Create a dictionary with the information selected 
        (scen_data, s_e_production, s_e_usage) = build_scen_data(scen_file, years, scenario,value_slider[0],value_slider2[0],v_s3[0],v_s31[0],v_s4[0],v_s41[0],v_s5[0],v_s6[0],unit, kommun, peak_hour)
        (scen_data2, s_e_production2, s_e_usage2) = build_scen_data(scen_file, years, scenario,value_slider[1],value_slider2[1],v_s3[1],v_s31[1],v_s4[1],v_s41[1],v_s5[1],v_s6[1], unit, kommun, peak_hour)

        # Lines to compare values between 2 sankeys and highlight the differences making them more opaque
        for a in range(len(scen_data["link"]["value"])):
            if scen_data["link"]["value"][a] != scen_data2["link"]["value"][a]:
                scen_data2["link"]["color"][a] = scen_data2["link"]["color"][a].replace("0.4", "1")

        # Display a sankey diagram with the information
        fig = build_sankey(scen_data, actual_unit)
        fig.update_layout()

        fig2 = build_sankey(scen_data2, actual_unit)
        fig2.update_layout()

        return fig, fig2, s_e_production, s_e_usage, s_e_production2, s_e_usage2, {'display':'block'},
    
app.run(debug=True)

