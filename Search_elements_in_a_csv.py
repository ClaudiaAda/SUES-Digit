import json, urllib, requests
import pandas as pd

scen_data = {"label":[], "color":[], "source":[], "target":[]}
positions = {}
i = 0

# LOAD ALL LABELS
url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/Claudia-Branch/All_labels.json'
response_all_labels = urllib.request.urlopen(url_all_labels)
info_data = json.loads(response_all_labels.read())

# LOAD SCENARIO DATA
scen_file = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/Pruebas/main/vensim_data_Scen1_Skara_ver4.csv")
scen_labels = list(scen_file.head(0))
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

    print(f"For {label} its target is {targets_names} that corresponds with {targets_values}")
    #scen_data["target"].append(list(map(positions.get, info_data[label]["target"])))

#print(scen_data["label"])
print(positions)
#print(info_data['electric energy import']["target"])"""

