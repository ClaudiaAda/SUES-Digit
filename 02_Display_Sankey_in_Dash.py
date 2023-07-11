from dash import Dash, dcc, html, Input, Output
import json, urllib, requests, pprint
import pandas as pd
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.H2('Sankey Diagram'),

        html.Label('Västra Götalands Iän'),
        dcc.Dropdown(['Skara kommun','Lidköping kommun'], 'Skara kommun'),


        dcc.Graph(id="graph"),
        html.P("Ratio"),
        dcc.Slider(id='Scenario 1', min=0, max=1, 
                value=0, step=0.05)
    ], style={'padding': 10, 'flex': 1}),

    html.Div(children=[
        html.Label('Year'),
        dcc.Dropdown(['2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033','2034'],'2023')
    ], style={'padding': 10, 'flex': 1})
    ])

@app.callback(
   Output("graph", "figure"), 
    Input("Scenario 1", "value"))

def display_sankey(value):

    # LOAD PERMANENT DICTIONARY in info_data
    # (There are 3 types of data: 
    # - Normal: Its name appears in the visualisation and has connections with other labels.
    # - Link: Its name does not appear in the visualisation, its value is used for the connection of other labels.
    # - Output: Its name appears, but its value is not used in the Diagram, as it is the final target.)
    url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/All_labels_Claudia.json'
    response_all_labels = urllib.request.urlopen(url_all_labels)
    info_data = json.loads(response_all_labels.read())

    # LOAD SCENARIO DATA 
    url_scen_file = "https://raw.githubusercontent.com/ClaudiaAda/Scenario_Files/main/vensim_data_Scen1_Skara_ver4%20(3).csv"
    scen_file = pd.read_csv(url_scen_file)
    scen_labels = (scen_file.head(0)) #Save the first row - labels' names

    # Declaration of scenario dictionary - data used for the Sankey Diagram
    scen_data = {"node": { "label":[], "color":[]},         
                "link": { "source":[], "target":[], "value":[], "color":[]}
                }

    # Declaration of dictionary to asign a number to each energy variable, 
    # so later these names can be changed to numbers for Sankey Diagram
    positions = {}
    i = 0

    # Declaration of a list with the constant variables
    constant_variables = []

    # Declaration of input variables from the Web Page
    year = "0"
    slider = 2

    # Read all the energy types and: 
    # - If it appears with its own name safe as constant.
    # - If it can be displayed in the Diagram, (not a link) see 
    # if it is used in this scenario save it and assign a number.
    for label in list(info_data.keys()):

        if label in scen_labels:
            constant_variables.append(label)

        if info_data[label]["target"] != "link":
            # To know if it is used in the scenario, it look if its name or 
            # its first temporary variable appears in the first row
            if ("T0 " + label) or label in scen_labels:

                positions[label] = i
                # Save the name of the label and its color in the scenario dictionary
                scen_data["node"]["label"].append(label)
                scen_data["node"]["color"].append(info_data[label]["color"])
                i += 1

        

    # For the energy types used, let's declare their connections with the values
    for label in scen_data["node"]["label"]:

        # Only treat "normal" energy types, the ones with targets:connections.
        if info_data[label]["target"] != ("link" and "output"):
            # There can be more than one connection, so it is evaluated each one (0,a).
            for a in range(len(info_data[label]["target"])):
                
                # If the variable to connect and the variable that assigns 
                # the value to that connection also exists, it will be added 
                # their numbers to the dictionary for Sankey Diagram, and the color
                # (It is compared the name and the temporary name) 
                target_name = info_data[label]["target"][a]
                value_name = info_data[label]["value"][a]

                if ((("T0 " + target_name) or (target_name)) 
                    and (("T0 " + value_name) or (value_name))) in scen_labels:
                
                    target_position = positions[target_name]
                    scen_data["link"]["target"].append(target_position)
                    
                    if value_name in constant_variables:
                        find_value = (scen_file[value_name][(value*20)])
                    else:
                     find_value = (scen_file["T" + year + " " + value_name][(value*20)])

                    scen_data["link"]["value"].append(find_value)
                    scen_data["link"]["color"].append(info_data[value_name]["color"])

                    #Also, for each connection, it is added the number of the source    
                    scen_data["link"]["source"].append(positions[label])
        

    # Code to display the Sankey Diagram, it fils the inputs with 
    # the scenario dictionary : scen_data
    fig = go.Figure(data=[go.Sankey(
        # Define nodes
        node = dict(
            pad = 30,
            thickness = 15,
            line = dict(color = "black", width = 0.01),
            label =  scen_data["node"]['label'],
            color =  scen_data["node"]['color']
        ),
        # Add links
        link = dict(
            arrowlen = 30,
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