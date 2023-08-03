from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import json, urllib, requests
import plotly.graph_objects as go
import time

from data_processingtete import build_scen_data
from sankey_diagramtete import build_sankey

fig = go.Figure()

app = Dash(__name__)
app.title = "SUES-DIGIT Project"

app.layout = html.Div(
    id="app-container",
    children = [
        html.Div(
            id = "header_area",
            children = [
                html.H1(
                    id = "header_title",
                    children = "SUES-DIGIT"
                ),
                html.P(
                    id = "header-description",
                    children = "Distribution of energy"
                )
            ]
        ),
        html.Div(
            id = "all_settings_area",
            children = [
                html.Div(
                    id = "first_row",
                    #To put distance between elements: style = { "padding-bottom" : 20},
                    children =[
                        html.Div(
                            id = "kommun_column",
                            #style = {"columnCount" : 2},
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
                        ),
                        html.Div(
                            id = "year_column and peak hour",
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
                                dcc.Checklist(
                                    id = "peak_hour",
                                    options=[
                                    # {'label': 'Peak hour', 'value': 'on'},
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
                        ),
                    ],
                ),
                html.Div(
                    id = "scenario_area",
                    #style = {"columnCount":2},
                    children = [
                        html.Div(
                            id = "scenario_menu_column",
                            children = [
                                html.Label("Choose a scenario:"),
                                dcc.Dropdown(
                                    id = "scenario_menu",
                                    options = [
                                        {'label' : 'Scenario 1 - Ratio of EVs', 'value' : "1" },
                                        {'label' : 'Scenario 2 - New industry establishment NIE', 'value' : "2" },
                                        {'label' : 'Scenario 3 - New Houses - ratio New houses DHP user', 'value' : "3" },
                                        {'label' : 'Scenario 4 - users apartment buildings - Goal ratio DHP users small houses', 'value' : "4" },
                                        {'label' : 'Scenario 5 - no large solar panel projects', 'value' : "5" },
                                        {'label' : 'Scenario 6 - no large wind mill projects', 'value' : "6" },
                                        {'label' : 'Scenario All', 'value' : "7" }
                                    ],
                                    placeholder = "Select a scenario..."
                                )
                            ]
                        ),
                        html.Div(
                            id = "scenario_slider_column",
                            children = [
                                html.Label("Place for the slider"),
                                html.Div(
                                    children = [
                                        dcc.Slider(
                                            min=0,
                                            max=1,
                                            step=0.05,
                                            value=None,
                                            id="slider",
                                            #vertical=True   
                                        ),
                                        dcc.Markdown(
                                            id="slider_scale",
                                            children ="",
                                            style = {"textAlign" : "right"}
                                        )
                                    ]
                                ),
                                html.Div(
                                    id = "invisible_slider",
                                    style = {"visibility" : "hidden"},
                                    children = [
                                        dcc.Slider(
                                            min=0,
                                            max=1,
                                            step=0.25,
                                            value=None,
                                            id="slider2",
                                        ),
                                        dcc.Markdown(
                                            id="slider_scale2",
                                            children ="", 
                                            style = {"textAlign" : "right"}   
                                        )
                                    ]
                                )
                            ]
                        ),
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
                    ]
                )
            ],
        ),
        html.Div(
            id = "display_area",
            children = [
                html.Div(
                    id = "sum_energy",
                    style = {"columnCount":2},
                    children = [
                        html.Div(                     
                            children = [
                                html.P(id="text_sum_energy_production", children="Sum Energy Production"),
                                html.P(id="sum_energy_production")
                            ]
                        ),
                        html.Div(
                            children = [
                                html.P(id="text_sum_energy_usage", children="Sum Energy Usage "),
                                html.P(id="sum_energy_usage")
                            ]
                        ),
                        html.Data(
                            id= "actual_unit"
                        )
                    ]
                )
            ]
        ),
        dcc.Graph(
            id = "graph", 
            figure=  {
                'layout' : {
                    'plot_bgcolor' :'yellow', #hay que meterlo en el update todo el layout tb
                    'paper_bgcolor' : 'pink',
                    'font' : {
                        'color' : 'black'
                    },
                    'title' : 'holi'
                }
            }
        )
    ],
)

# Assign properties to the sliders

@app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "step"),
    Output("slider_scale", "children"),
    Output("invisible_slider", "style"),
    Output("slider2", "min"),
    Output("slider2", "max"),
    Output("slider2", "step"),        
    Output("slider_scale2", "children"),
    Output("slider", "value"),
    Output("slider2", "value"),

    Input("scenario_menu", "value"),
    State("slider", "min"),
    State("slider", "max"),
    State("slider", "step"),
    State("invisible_slider", "style"),
    State("slider2", "min"),
    State("slider2", "max"),
    State("slider2", "step"),
    State("slider", "value"),
    State("slider2", "value"),

    )

def update_output(value, min, max, step, style, min2, max2, step2, val, val2):
    if value == "1":  
        min=0
        max=1
        step=0.05
        style = {"visibility": "hidden"}
        val = None
        val2 = None
        return (min, max, step, f"%",style, min2, max2, step2, f" ",val, val2) #{k: '{}'.format(k) for k in range(min,max+1)}
    if value == "2":  
        min=0
        max=3
        step=1
        style = {"visibility": "hidden"}
        val = None
        val2 = None
        return (min, max, step, f"units",style, min2, max2, step2, f" ",val,val2)   
    if value == "3":  
        min=0
        max=300
        step=25
        min2=0
        max2=1
        step2=0.25
        style={"visibility": "visible"}
        val = None
        val2 = None
        return (min, max, step, f"units",style, min2, max2, step2, f"%",val,val2)
    if value == "4":  
        min=0.96
        max=1
        step=0.01
        min2=0.2
        max2=1
        step2=0.1
        style={"visibility": "visible"}
        val = None
        val2 = None
        return (min, max, step, f"%",style, min2, max2, step2, f"%",val,val2 )
    if value == "5":  
        min=0
        max=12
        step=1
        style = {"visibility": "hidden"}
        val = None
        val2 = None
        return (min, max, step, f"units",style, min2, max2, step2, f" ",val,val2)
    if value == "6":  
        min=0
        max=2
        step=1
        style = {"visibility": "hidden"}
        val = None
        val2 = None
        return (min, max, step, f"units",style, min2, max2, step2, f" ",val,val2)
    
@app.callback(
    Output("unit", "options"),
    Input("peak_hour", "value")
)

def unit_menu(value):
    
    if value == ['on']:
        #value = 'on' 
        options = [
            {'label' : 'Kw', 'value' : 'kilo' },
            {'label' : 'Mw', 'value' : 'mega' },
            {'label' : 'Gw', 'value' : 'giga' }
        ]
        return options
    else: 
        #value = 'off'
        options = [
            {'label' : 'Kwh', 'value' : 'kilo' },
            {'label' : 'Mwh', 'value' : 'mega' },
            {'label' : 'Gwh', 'value' : 'giga' }
        ]
        return options 
    

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
            return f"Sum Energy Production (Kw):", f"Sum Energy Usage (Kw):", f"Kw"
        if units == 'mega':
            return f"Sum Energy Production (Mw):", f"Sum Energy Usage (Mw):", f"Mw"
        if units == 'giga':
            return f"Sum Energy Production (Gw):", f"Sum Energy Usage (Gw):", f"Gw"
    else: 
        if units == 'kilo':
            return  f"Sum Energy Production (Kwh):", f"Sum Energy Usage (Kwh):", f"Kwh"
        if units == 'mega':
            return  f"Sum Energy Production (Mwh):", f"Sum Energy Usage (Mwh):", f"Mwh"
        if units == 'giga':
            return  f"Sum Energy Production (Gwh):", f"Sum Energy Usage (Gwh):", f"Gwh"

   
# VARIABLES NEEDED
año = '0'
value_condition = ""

# SELECT THE URL OF EACH SCENARIO CASE
url_scenarios_cases = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/Scenarios_cases3.json'
response_scenario_cases = urllib.request.urlopen(url_scenarios_cases)
info_scenarios_cases = json.loads(response_scenario_cases.read())

@app.callback(
    Output("graph", "figure"),
    Output("sum_energy_production", "children"),
    Output("sum_energy_usage", "children"),
    Input("kommun_menu", "value"),
    Input("scenario_menu", "value"),
    Input("years", "value"),
    Input("slider","value"),
    Input("slider2","value"),
    Input("peak_hour", "value"),
    Input("unit", "value"),
    Input("actual_unit", "children"),
    

)

def display_sankey(kommun,scenario,years,value_slider,value_slider2, peak_hour, unit,actual_unit):

    if (kommun is None) or (scenario is None) or (years is None) or (value_slider is None):
        raise PreventUpdate
    
    else:
        print(kommun)
        print(scenario)
        print(years)
        print(value_slider)
        print(value_slider2)
        print(peak_hour)
        print(unit)
        print(actual_unit)
        
        

        #print(info_scenarios_cases[kommun][scenario])
        # Save the correct excel file
        scen_file = pd.read_csv(info_scenarios_cases[kommun][scenario])
    
        # Create a dictionary with the information selected 
        (scen_data, s_e_production, s_e_usage) = build_scen_data(scen_file, years, scenario,value_slider,value_slider2, peak_hour, unit, kommun)
        #print("Data hecho")

        # Display a sankey diagram with the information
        fig = build_sankey(scen_data,actual_unit)
        fig.update_layout(
            title= 'holi2',
    
        )
        #print("Sankey hecho")

        return fig, s_e_production, s_e_usage
    
    

app.run_server(debug=True)

