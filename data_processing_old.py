import json, urllib, requests
import pandas as pd
import numpy as np

def build_scen_data(scen_file, year, scenario,value_slider,value_slider2, peak_hour, unit):
    
    # LOAD PERMANENT DICTIONARY in info_data
    # (There are 3 types of data: 
    # - Normal: Its name appears in the visualisation and has connections with other labels.
    # - Link: Its name does not appear in the visualisation, its value is used for the connection of other labels.
    # - Output: Its name appears, but its value is not used in the Diagram, as it is the final target.)
    url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/All_labels_Claudia.json'
    response_all_labels = urllib.request.urlopen(url_all_labels)
    info_data = json.loads(response_all_labels.read())

    scen_labels = (scen_file.head(0)) #Save the first row - labels' names

    # Declaration of scenario dictionary - data used for the Sankey Diagram
    scen_data = {"node": { "label":[], "color":[], "x": [], "y": []},         
                "link": { "source":[], "target":[], "value":[], "color":[]},
                }

    # Declaration of dictionary to asign a number to each energy variable, 
    # so later these names can be changed to numbers for Sankey Diagram
    node_positions = {}
    node_value = {}
    i = [0,0,0,0] # List with number of nodes in total and in each column
    y = [0,0,0,0] # Position of the variable in the column

    # Declaration of a list with the constant variables
    constant_variables = []

    # Obtain the number simulation depending on the sliders' values to select the correct variables' values.
    # To select the correct number the values of the table are rounded up
    columns_names=list(scen_labels)
    column1 = columns_names[1]
    scen_file[column1] = pd.Series([round(val,2) for val in scen_file[column1]])

    if(scenario==7):
        print("It is not programmed")

    elif(scenario==3 or scenario==4):
        column2=scen_labels[2]
        scen_file[column2] = pd.Series([round(val,2) for val in scen_file[column2]])

        cond1 = np.where(scen_file[column1] == value_slider)
        cond2 = np.where(scen_file[column2] == value_slider2) 
        cond1 = cond1[0].tolist()
        cond2 = cond2[0].tolist()
        num_simulation = list(set(cond1).intersection(cond2))
                                    
    else:
        num_sim = np.where(scen_file[column1] == value_slider)
        num_simulation = num_sim[0].tolist()


    # Read all the energy types and: 
    # - If it appears with its own name safe as constant.
    # - If it can be displayed in the Diagram, (not a link) see 
    # if it is used in this scenario save it and assign a number.
    
    print(info_data.keys())
    for label in list(info_data.keys()):

        if label in scen_labels:
            constant_variables.append(label)

        if info_data[label]["target"] != "link":
            # To know if it is used in the scenario, it look if its name or 
            # its first temporary variable appears in the first row
            if ("T0 " + label) or label in scen_labels:

                node_positions[label] = i[0]
                # Save the name of the label and its color in the scenario dictionary
                scen_data["node"]["label"].append(label)
                scen_data["node"]["color"].append(info_data[label]["color"])
                i[0] += 1
                i[info_data[label]["column"]]+=1  

            # Assign position in x-axis to nodes 
            if "x" in info_data[label]:
                scen_data["node"]["x"].append(info_data[label]["x"])

            elif info_data[label]["target"] == "output":
                scen_data["node"]["x"].append(1)

            else:
                scen_data["node"]["x"].append(0)

    print("VARIABLES CONSTANTES")
    print(constant_variables)
     # Assign position in y-axis to nodes 
    for label in node_positions.keys():

        # Normalized position order
        y_position = y[info_data[label]["column"]]/i[info_data[label]["column"]]

        # Adapted position to variables' values

        #variable_value = scen

        scen_data["node"]["y"].append(y_position)
        y[info_data[label]["column"]] += 1


    # Assign position in y-axis to nodes
    """for label in list(positions.keys()):
        y_position = positions[label] * scen_data["link"]["value"][i]
        scen_data["node"]["y"].append(y_position)"""


    # For the energy types used, let's declare their connections with the values
    for label in scen_data["node"]["label"]:

        # Only treat "normal" energy types, the ones with targets: connections.
        if info_data[label]["target"] != ("link" and "output"):
            print("")
            print ("Soy variable")
            print(label)
            # There can be more than one connection, so it is evaluated each one (0,a).
            for a in range(len(info_data[label]["target"])):
                
                # If the variable to connect and the variable that assigns 
                # the value to that connection also exists, it will be added 
                # their numbers to the dictionary for Sankey Diagram, and the color
                # (It is compared the name and the temporary name) 
                print("")
                print("La union es:")
                target_name = info_data[label]["target"][a]
                print(target_name)
                value_name = info_data[label]["value"][a]
                print(value_name)

                if ((("T0 " + target_name) or (target_name)) 
                    and (("T0 " + value_name) or (value_name))) in scen_labels:
                
                
                    target_position = node_positions[target_name]
                    scen_data["link"]["target"].append(target_position)
                    
                    if value_name in constant_variables:
                        find_value = (scen_file[value_name][num_simulation[0]])
                        print("SOY CONSTANTE!!!")
                    else:
                        find_value = (scen_file["T" + str(year) + " " + value_name][num_simulation[0]])

                    print("HE ENTRADO y valgo:")
                    print(find_value)
                    
                    # Modify value according to unit and if peak hour is chosen
                    if peak_hour == ['on']:
                        find_value = find_value/8760
                        #print("Peak hour")

                    if unit == "mega":
                        find_value = find_value*1000
                        #print("Megawatts")

                    elif unit == "kilo":
                        find_value = find_value*1000000
                        #print("Kilowatts")

                    scen_data["link"]["value"].append(find_value)
                    scen_data["link"]["color"].append(info_data[value_name]["color"])

                    #Also, for each connection, it is added the number of the source    
                    scen_data["link"]["source"].append(node_positions[label])


    # It is also display the sum of energies        
    s_e_production = scen_file["T" + year + " sum energy production"][num_simulation[0]]
    s_e_usage = scen_file["T" + year + " sum energy usage"][num_simulation[0]]

    if peak_hour == ['on']:
        s_e_production = s_e_production/8760
        s_e_usage = s_e_usage/8760
        #print("Peak hour")

    if unit == "mega":
        s_e_production = s_e_production*1000
        s_e_usage = s_e_usage*1000
        #print("Megawatts")

    elif unit == "kilo":
        s_e_production = s_e_production*1000000
        s_e_usage = s_e_usage*1000000
        #print("Kilowatts")

    s_e_production = round(s_e_production, 2)
    s_e_usage = round(s_e_usage, 2)

    print(node_positions)
    print(scen_data["node"]["x"])
    print(scen_data["node"]["y"])
    print(scen_data)
        
    return (scen_data, s_e_production, s_e_usage)
