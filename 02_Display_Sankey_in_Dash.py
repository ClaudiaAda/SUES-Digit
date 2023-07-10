from dash import Dash, dcc, html, Input, Output
import json, urllib, requests, pprint
import pandas as pd
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    html.H2('Sankey Diagram'),
    dcc.Graph(id="graph"),
    html.P("Ratio"),
    dcc.Slider(id='Scenario 1', min=0, max=1, 
               value=0, step=0.05)
])

@app.callback(
   Output("graph", "figure"), 
    Input("Scenario 1", "value"))

def display_sankey(slider):
    scen_data = {"node": {"label":[], "color":[]},         
                "link": {"source":[], "target":[], "value":[],"color":[]}
                }

    positions = {}
    i = 0

    year = "0"
    slider = 5

    # LOAD ALL LABELS
    url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/All_labels.json'
    response_all_labels = urllib.request.urlopen(url_all_labels)
    info_data = json.loads(response_all_labels.read())

    # LOAD SCENARIO DATA
    scen_file = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/vensim_data_Scen1_Skara_ver4.csv")
    scen_labels = (scen_file.head(0))
    #variables_ejemplo = variables[0:100]
    #print(variables_ejemplo)

    for label in list(info_data.keys()):
        
        if info_data[label]["target"] != "link":
            if "T0 " + label in scen_labels:
                positions[label] = i
                scen_data["node"]["label"].append(label)
                scen_data["node"]["color"].append(info_data[label]["color"])
                i += 1
            


    for label in scen_data["node"]["label"]:

        if info_data[label]["target"] != ("link" and "output"):
        #print(label)
        
            targets_names = info_data[label]["target"]
            targets_values = list(map(positions.get, targets_names))
            scen_data["link"]["target"].extend(targets_values)

            for index in range(len(targets_names)):
                scen_data["link"]["source"].extend([positions[label]])

            
            for target in info_data[label]["value"]:
                if "T0 " + target in scen_labels:
                    find_value = (scen_file["T0 " + target][slider])
                    scen_data["link"]["value"].append(find_value)
                    #print(find_value)

                    scen_data["link"]["color"].append(info_data[target]["color"])

                        #scen_data["link"]["color"].append(info_data[target]["color"])
            
    fig = go.Figure(data=[go.Sankey(
        # Define nodes
        node = dict(
        pad = 15,
        thickness = 15,
        line = dict(color = "black", width = 0.5),
        label =  scen_data["node"]['label'],
        color =  scen_data["node"]['color']
        ),
        # Add links
        link = dict(
        source =  scen_data["link"]['source'],
        target =  scen_data["link"]['target'],
        color =  scen_data["link"]['color'],
        value = scen_data["link"]['value']
    ))])

    return fig
app.run_server(debug=True)


"""print(scen_data["node"]['label'])
print(scen_data["node"]['color'])
print(scen_data["link"]['source'])
print(scen_data["link"]['target'])
print(scen_data["link"]['value'])
print(positions)"""