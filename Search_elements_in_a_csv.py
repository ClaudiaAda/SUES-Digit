import json, urllib, requests
import pandas as pd

labels = {}
i = 0

# LOAD ALL LABELS
url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/Pruebas/main/All_labels.json'
response_all_labels = urllib.request.urlopen(url_all_labels)
all_labels = json.loads(response_all_labels.read())

# LOAD SCENARIO DATA
scen_data = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/Pruebas/main/vensim_data_Scen1_Skara_ver4.csv")
variables = list(scen_data.head(0))
#variables_ejemplo = variables[0:100]
#print(variables_ejemplo)

for label in all_labels:
    for column in variables:
        if "T0 " + label == column:
            labels[label] = i
            i += 1
            break

print(labels)

