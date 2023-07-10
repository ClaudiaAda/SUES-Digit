import json, urllib, requests, pprint
import pandas as pd
import plotly.graph_objects as go

scen_data = {"label":[], "color":[], "source":[], "target":[]}
positions = {}
i = 0

values = [1,1,1,1,1,1,1,1,1,1,1]

# LOAD ALL LABELS
url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/All_labels.json'
response_all_labels = urllib.request.urlopen(url_all_labels)
info_data = json.loads(response_all_labels.read())

# LOAD SCENARIO DATA
scen_file = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/Pruebas/main/vensim_data_Scen1_Skara_ver4.csv")
scen_labels = (scen_file.head(0))
#variables_ejemplo = variables[0:100]
#print(variables_ejemplo)

for label in list(info_data.keys()):
    for column in scen_labels:
        if "T0 " + label == column:
            positions[label] = i
            scen_data["label"].append(label)
            scen_data["color"].append(info_data[label]["color"])
            i += 1
            break


for label in scen_data["label"]:
    targets_names = info_data[label]["target"]
    targets_values = list(map(positions.get, targets_names))
    scen_data["target"].extend(targets_values)

    for index in range(len(targets_names)):
        scen_data["source"].extend([positions[label]])

    

fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  scen_data['label'],
      color =  scen_data['color']
    ),
    # Add links
    link = dict(
      source =  scen_data['source'],
      target =  scen_data['target'],
      #color =  scen_data['color'],
      value = values
))])

fig.show()
