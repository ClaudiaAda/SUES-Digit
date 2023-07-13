from dash import Dash, dcc, html, Input, Output
import pandas as pd
import json, urllib, requests

from data_processing import build_scen_data
from sankey_diagram import build_sankey

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
            id="menu-area",
            children = [
                html.Div(
                    children = [
                        html.Label("Choose a scenario:"),
                        dcc.Dropdown(
                            id = "scenario_menu",
                            options = [
                                {'label' : 'Scenario 1', 'value' : 1 },
                                {'label' : 'Scenario 2', 'value' : 2 },
                                {'label' : 'Scenario 3', 'value' : 3 },
                                {'label' : 'Scenario 4', 'value' : 4 },
                                {'label' : 'Scenario 5', 'value' : 5 },
                                {'label' : 'Scenario 6', 'value' : 6 },
                                {'label' : 'Scenario All', 'value' : 7 }
                            ],
                            clearable=False,
                            value=1
                        )
                    ]       
                ),
                html.Div(
                    children = [
                        html.Label('Västra Götalands Iän'),
                        dcc.Dropdown(
                            id = "kommun_menu",
                            options = [
                                {'label':'Skara kommun','value':"Skara kommun"},
                                {'label':'Lidköping kommun','value':"Lidköping kommun"}
                            ],
                            clearable = False,
                            value = "Skara kommun",
                        )
                    ]
                ),
                html.Div(
                    children = [
                        html.Label("Year:"),
                        dcc.Dropdown(
                            id = "year",
                            options = [
                                {'label' : '2023', 'value' : '0' },
                                {'label' : '2024', 'value' : 1 },
                                {'label' : '2025', 'value' : 2 },
                                {'label' : '2026', 'value' : 3 },
                                {'label' : '2027', 'value' : 4 },
                                {'label' : '2028', 'value' : 5 },
                                {'label' : '2029', 'value' : 6 },
                                {'label' : '2030', 'value' : 7 },
                                {'label' : '2031', 'value' : 8 },
                                {'label' : '2032', 'value' : 9 },
                                {'label' : '2033', 'value' : 10 }
                            ],
                            clearable=False,
                            value=0
                        )
                    ]       
                ),
            ]
        ),
                              
        dcc.Graph(id = "graph")
    ]
)

scen_value = 0.3


@app.callback(
    Output("graph", "figure"),
    Input("kommun_menu", "value"),
    Input("scenario_menu", "value"),
    Input("year", "value")
    
)

def display_sankey(kommun,scenario,year):

    # SELECT THE URL OF EACH SCENARIO CASE
    url_scenarios_cases = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/Scenarios_cases.json'
    response_scenario_cases = urllib.request.urlopen(url_scenarios_cases)
    info_scenarios_cases = json.loads(response_scenario_cases.read())

    scen_file = pd.read_csv(info_scenarios_cases[kommun][scenario])

    print(info_scenarios_cases[kommun][scenario])

    # Create a dictionary with the information selected 
    scen_data = build_scen_data(scen_file, year, scen_value)


    # Display a sankey diagram with the information
    fig = build_sankey(scen_data)
    fig.update_layout

    print(kommun)
    print(scenario)
    print(year)

    return fig

app.run_server(debug=True)

