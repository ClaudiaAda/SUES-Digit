from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import json, urllib, requests
import plotly.graph_objects as go
import time

from data_processing import build_scen_data
from sankey_diagram import build_sankey

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
                    style = { "padding-bottom" : 20, "maxHeight":5000},
                    children =[
                        html.Div(
                            id = "kommun_column",
                            #style = {"columnCount" : 1},
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
                                        {'label' : 'Scenario 1', 'value' : 1 },
                                        {'label' : 'Scenario 2', 'value' : 2 },
                                        {'label' : 'Scenario 3', 'value' : 3 },
                                        {'label' : 'Scenario 3.1', 'value' : 31 },
                                        {'label' : 'Scenario 4', 'value' : 4 },
                                        {'label' : 'Scenario 4.1', 'value' : 41 },
                                        {'label' : 'Scenario 5', 'value' : 5 },
                                        {'label' : 'Scenario 6', 'value' : 6 }
                                    ],
                                    placeholder = "Select a scenario..."
                                )
                            ]
                        ),
                        html.Div(
                            id = "scenario_slider_column",
                            children = [
                                html.Label("Place for the slider:"),
                                    dcc.Slider(
                                        min=0.5,
                                        max=1,
                                        step=0.25,
                                        value=None,
                                        #marks={k: '{}'.format(k) for k in range(0,21)},
                                        #tooltip={"placement" : "bottom", "always_visible" : True},
                                        id="slider",
                                        #vertical=True
                                    ),
                                    dcc.Markdown(
                                        id="slider_scale",
                                        children =""
                                    )
                            ]
                        )
                    ]
                )
            ],
        ),

        dcc.Graph(id = "graph", figure= fig)
    ],
)


@app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "step"),
    Output("slider_scale", "children"),
    #Output("slider", "marks"),
    Input("scenario_menu", "value"),
    State("slider", "min"),
    State("slider", "max"),
    State("slider", "step"),
    #State("slider", "marks")
    )

def update_output(value, min, max, step):
    if value == 1:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step, f"%")   #{k: '{}'.format(k) for k in range(min,max+1)}
    if value == 2:  
        min=0
        max=2
        step=1
        return (min, max, step, f"units")   
    if value == 3:  
        min=100
        max=300
        step=100
        return (min, max, step, f"units")
    if value == 31:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step, f"%")
    if value == 4:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step, f"%")
    if value == 41:  
        min=0.96
        max=1
        step=0.04
        return (min, max, step, f"%")
    if value == 5:  
        min=6
        max=12
        step=3
        return (min, max, step, f"units")
    if value == 6:  
        min=0
        max=2
        step=1
        return (min, max, step, f"units")


#VARIABLES NEEDED

scen_value = 0
año = '0'

# SELECT THE URL OF EACH SCENARIO CASE
url_scenarios_cases = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/Scenarios_cases3.json'
response_scenario_cases = urllib.request.urlopen(url_scenarios_cases)
info_scenarios_cases = json.loads(response_scenario_cases.read())


@app.callback(
    Output("graph", "figure"),
    Input("kommun_menu", "value"),
    Input("scenario_menu", "value"),
    Input("years", "value")
)

def display_sankey(kommun,scenario,years):

    print(kommun)
    print(scenario)
    print(years)

    #print(info_scenarios_cases[kommun][scenario])
    #Save the correct excel file
    scen_file = pd.read_csv(info_scenarios_cases[kommun][scenario])
 
    # Create a dictionary with the information selected 
    scen_data = build_scen_data(scen_file, years, scen_value)


    # Display a sankey diagram with the information
    fig = build_sankey(scen_data)
    fig.update_layout()
    
    return fig

app.run_server(debug=True)

