from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import json, urllib, requests
import plotly.graph_objects as go
import time

from data_processing_new import build_scen_data
from sankey_diagram_new import build_sankey

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
                                        {'label' : 'Scenario 3 - New Houses - Ratio New houses DHP user', 'value' : "3" },
                                        {'label' : 'Scenario 4 - Users apartment buildings - Goal ratio DHP users small houses', 'value' : "4" },
                                        {'label' : 'Scenario 5 - Number large solar panel projects', 'value' : "5" },
                                        {'label' : 'Scenario 6 - Number large wind mill projects', 'value' : "6" },
                                        {'label' : 'Scenario All', 'value' : "7" }
                                    ],
                                    placeholder = "Select a scenario..."
                                )
                            ]
                        ),
                        html.Div(
                            id = "scenario_slider_column",
                            children = [
                                html.Div(
                                    children = [
                                        dcc.Markdown(
                                            id="slider_scale",
                                            children ="Select a value:",
                                            style = {"textAlign" : "left"}
                                        ),
                                        dcc.RangeSlider(
                                            id="slider",
                                            min=0,
                                            max=1,
                                            step=0.05,
                                            value=[None,None],
                                        ),
                                        dcc.Markdown(
                                            id="slider_scale1",
                                            children ="",
                                            style = {"textAlign" : "right"}
                                        )
                                    ]
                                ),
                                html.Div(
                                    id = "invisible_slider",
                                    style = {'display' : 'none'},
                                    children = [
                                        dcc.Markdown(
                                            id="slider_scale2a",
                                            children ="New houses", 
                                            style = {"textAlign" : "left"}   
                                        ),
                                        dcc.RangeSlider(
                                            min=0,
                                            max=1,
                                            step=0.25,
                                            value=[None,None],
                                            id="slider2",
                                        ),
                                        dcc.Markdown(
                                            id="slider_scale2",
                                            children ="", 
                                            style = {"textAlign" : "right"}   
                                        )
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
                                            children ="units",
                                            style = {"textAlign" : "right"}
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
                                            children ="%",
                                            style = {"textAlign" : "right"}
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
                                            children ="%",
                                            style = {"textAlign" : "right"}
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
                                            children ="%",
                                            style = {"textAlign" : "right"}
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
                                            children ="units",
                                            style = {"textAlign" : "right"}
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
                                        dcc.Markdown(
                                            children ="units",
                                            style = {"textAlign" : "right"}
                                        ),
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
                            id= "actual_unit",
                            style = {'display':'none'}
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id="graph-container", 
            style = {'display' : 'none'},
            children = [ 
            dcc.Graph(
                id = "graph",
                figure=  {
                    'layout' : {
                        'plot_bgcolor' :'blue', #hay que meterlo en el update todo el layout tb
                        'paper_bgcolor' : 'red',
                        'font' : {
                            'color' : 'black'
                        },
                        'title' : 'holi', 
                    },
                },
                )
            ]
        ),
        html.Div(
            id="graph-container2", 
            style = {'display' : 'none'},
            children = [ 
            dcc.Graph(
                id = "graph2",
                figure=  {
                    'layout' : {
                        'plot_bgcolor' :'blue', #hay que meterlo en el update todo el layout tb
                        'paper_bgcolor' : 'red',
                        'font' : {
                            'color' : 'black'
                        },
                        'title' : 'holi', 
                    },
                },
                )
            ]
        )       
    ],
)

# Assign properties to the sliders

@app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "step"),
    Output("slider_scale1", "children"),
    Output("invisible_slider", "style"),
    Output("slider2", "min"),
    Output("slider2", "max"),
    Output("slider2", "step"),        
    Output("slider_scale2", "children"),
    Output("slider", "value"),
    Output("slider2", "value"),
    Output("slider_scale", "children"),
    Output("invisible_slider2", "style"),
    Output("slider_scale2a", "children"),
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
    State("invisible_slider", "style"),
    State("slider2", "min"),
    State("slider2", "max"),
    State("slider2", "step"),
    State("slider", "value"),
    State("slider2", "value"),
    State("invisible_slider2", "style"),
    State("3", "value"),
    State("31", "value"),
    State("4", "value"),
    State("41", "value"),
    State("5", "value"),
    State("6", "value"),

    )

def update_output(value, min, max, step, style, min2, max2, step2, val, val2, style2, val3, val31, val4, val41, val5, val6):
    if value == "1":  
        min=0
        max=1
        step=0.05
        style = {'display':'none'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"%",style, min2, max2, step2, f" ",val, val2, f"Ratio of EVs", style2, f"", val3, val31, val4, val41, val5, val6) 
    if value == "2": 
        min=0
        max=3
        step=1
        style = {'display':'none'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"units",style, min2, max2, step2, f" ", val, val2, f"New industry establishment NIE", style2, f"", val3, val31, val4, val41, val5, val6)   
    if value == "3":  
        min=0
        max=300
        step=25
        min2=0
        max2=1
        step2=0.25
        style={'display':'block'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"units",style, min2, max2, step2, f"%", val, val2, f"New houses", style2, f"Ratio new houses DHP user", val3, val31, val4, val41, val5, val6)
    if value == "4":  
        min=0.2
        max=1
        step=0.1
        min2=0.96
        max2=1
        step2=0.01
        style={'display':'block'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"%",style, min2, max2, step2, f"%", val, val2, f"Goal ratio DHP users small houses", style2, f"Goal ratio DHP users apartment buildings", val3, val31, val4, val41, val5, val6)
    if value == "5":  
        min=0
        max=12
        step=1
        style = {'display':'none'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"units",style, min2, max2, step2, f" ", val, val2, f"Number large solar panel projects", style2, f"", val3, val31, val4, val41, val5, val6 )
    if value == "6":  
        min=0
        max=2
        step=1
        style = {'display':'none'}
        style2 = {'display':'none'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"units",style, min2, max2, step2, f" ", val, val2, f"Number large wind mill projects", style2, f"", val3, val31, val4, val41, val5, val6)
    if value == "7":  
        min=0.5
        max=1
        step=0.25  
        min2=0
        max2=2
        step2=1
        style={'display':'block'}
        style2 = {'display':'block'}
        val = val2 = val3 = val31 = val4 = val41 = val5 = val6 = [None,None]
        return (min, max, step, f"%",style, min2, max2, step2, f"units", val, val2, f"Ratio of EVs", style2, f"New industry establishment NIE", val3, val31, val4, val41, val5, val6)
    
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
    Output('graph-container', 'style'),
    Output('graph-container2', 'style'),
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
        print("NEW SIMULATION AAAAAAAAAAAAAAAAAAAAAAAAAAA")
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
    
app.run_server(debug=True)

