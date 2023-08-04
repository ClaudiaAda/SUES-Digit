import json, urllib, requests
import pandas as pd
import numpy as np

def build_scen_data(scen_file, year, scenario,value_slider,value_slider2, peak_hour, unit, kommun):
    
    # LOAD PERMANENT DICTIONARY in info_data
    # (There are 3 types of data: 
    # - Normal: Its name appears in the visualisation and has connections with other labels.
    # - Link: Its name does not appear in the visualisation, its value is used for the connection of other labels.
    # - Output: Its name appears, but its value is not used in the Diagram, as it is the final target.)
    url_all_labels = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/All_labels_Claudia10.json'
    response_all_labels = urllib.request.urlopen(url_all_labels)
    info_data = json.loads(response_all_labels.read())


    # LOAD CONSTANT ENERGIES information it is permanent for all scenarios
    if kommun == "Skara kommun":
        constant_file = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/Scenario_Files/main/vensim_data_Constants_Skara_ver1_good.csv")

    elif kommun == "Lidköping kommun":
        constant_file = pd.read_csv("https://raw.githubusercontent.com/ClaudiaAda/Scenario_Files/main/vensim_data_Constants_Lidk%C3%B6ping_ver1_good.csv")

    # Declaration of a list with the constant variables
    constant_variables = list(constant_file.head(0))


    # Declaration of scenario dictionary - data used for the Sankey Diagram
    scen_data = {"node": { "label":[], "color":[], "x": [], "y": [], "percentage": []},         
                "link": { "source":[], "target":[], "value":[], "color":[]},
                }
    

    # Declaration of dictionary to asign a number to each energy variable, 
    # so later these names can be changed to numbers for Sankey Diagram
    node_positions = {}
    i = 0 # Total number of nodes
    # List used to save the y-position of the variables in their columns
    y = [0,0.01,0.01,0.01] 


    # Obtain the number simulation depending on the scenario and sliders' values to take the correct variables' values.
    scen_labels = (scen_file.head(0)) #Save the first row - labels' names
    columns_names=list(scen_labels)
    column1 = columns_names[1]
    # To select the correct number the values of the table are rounded up
    scen_file[column1] = pd.Series([round(val,2) for val in scen_file[column1]])
    
    if(scenario==7):
        print("It is not programmed")

    elif(scenario==3 or scenario==4):
        column2=scen_labels[2]
        scen_file[column2] = pd.Series([round(val,2) for val in scen_file[column2]])

        # np.where function finds the row where the slider value is.
        cond1 = np.where(scen_file[column1] == value_slider)
        cond2 = np.where(scen_file[column2] == value_slider2) 
        # the object obtained is an array, this lines are used so the data can be used later
        cond1 = cond1[0].tolist()
        cond2 = cond2[0].tolist()
        num_simulation = list(set(cond1).intersection(cond2))
                                    
    else:
        num_sim = np.where(scen_file[column1] == value_slider)
        num_simulation = num_sim[0].tolist()


    # The sum of production and usage energies 
    s_e_production = scen_file["T" + year + " sum energy production"][num_simulation[0]]
    s_e_usage = scen_file["T" + year + " sum energy usage"][num_simulation[0]]


    # 1 LOOP : NODES -> Read all the energies stored in the dictionary and
    # if it can be displayed in the Diagram, (not a link) see if it
    # is used in this scenario (it is found in the excel file and has a value)
    # is saved along with some information.
    for label in list(info_data.keys()):

        if info_data[label]["target"] != "link":
            # To know if it is used in the simulation, it looks if its
            # name appears in the constants' excel file or its first
            # temporary variable appears in the first row of the variables' excel file
            if (("T0 " + label) in scen_labels) or label in constant_variables:
                
                # The value of the node is stored, this value is needed in later processes
                if label in constant_variables:
                        node_value = (constant_file[label][0])
                elif ("T0 " + label) in scen_labels:
                        node_value = (scen_file["T" + str(year) + " " + label][num_simulation[0]])

                # If the value is 0, it will not be stored to display it in the sankey 
                if node_value != 0:
                    # The energy name is stored as it is going to be displayed and 
                    # a number is associated with it (Sankey's diagram works with vectors of numbers)
                    node_positions[label] = i
                    # Save the name of the label and its color in the scenario dictionary
                    scen_data["node"]["label"].append(label)
                    scen_data["node"]["color"].append(info_data[label]["color"])
                    # i is actualised with the number of the next energy
                    i += 1
                    
                    # Calculate percentages:
                    # - percentage_value is used to define the y-position of the energies in the Sankey
                    # - percentage_name is used to show the value of the percentage of the 
                    # energy regarding the sum of energy in the Sankey
                    # Input nodes
                    if info_data[label]["column"] == 1:
                        percentage_value = round(node_value/s_e_production,2)
                        percentage_name = str(percentage_value*100) + "%"

                    # Intermediate nodes (they do not display percentage)
                    elif info_data[label]["column"] == 2:
                        percentage_value = round(node_value/s_e_production,2)
                        percentage_name = ""

                    # Outputs nodes
                    elif info_data[label]["column"] == 3:
                        percentage_value = round(node_value/s_e_usage,2)
                        percentage_name = str(percentage_value*100) + "%"

                    scen_data["node"]["percentage"].append(percentage_name)

                    # Assign position in x-axis to nodes, x-position is defined
                    # in the dictionary for some special energies. If they do not 
                    # have it defined it is assigned a predefined value
                    if "x" in info_data[label]:
                        scen_data["node"]["x"].append(info_data[label]["x"])

                    elif info_data[label]["column"] == 1:
                        scen_data["node"]["x"].append(0.001)

                    elif info_data[label]["column"] == 2:
                        scen_data["node"]["x"].append(0.5)

                    elif info_data[label]["column"] == 3:
                        scen_data["node"]["x"].append(1)
            
                    # Assign position in y-axis to nodes 
                    # The possition is actualised taking in to account the half of the width of the energy
                    # because the possition assigned to the center of the label
                    y[info_data[label]["column"]] += percentage_value/2

                    scen_data["node"]["y"].append(y[info_data[label]["column"]])
                    # The other half of the width is added for the next energy label
                    y[info_data[label]["column"]] += percentage_value/2


    # For the energy types used, let's declare their connections with the values
    for label in scen_data["node"]["label"]:

        #print(label)

        # Only treat "normal" energy types, the ones with targets: connections.
        if info_data[label]["target"] != ("link" and "output"):
            #print("")
            #print ("Soy variable")
            #print(label)
            # There can be more than one connection, so it is evaluated each one (0,a).
            for a in range(len(info_data[label]["target"])):
                
                # If the variable to connect and the variable that assigns 
                # the value to that connection also exists, it will be added 
                # their numbers to the dictionary for Sankey Diagram, and the color
                # (It is compared the name and the temporary name) 
                target_name = info_data[label]["target"][a]
                value_name = info_data[label]["value"][a]
                #print("")
                #print("La union es:")
                #print(target_name)
                #print(value_name)

                if ((("T0 " + target_name) in scen_labels) or (target_name in constant_variables)):

                    if target_name in node_positions.keys():
                
                        target_position = node_positions[target_name]
                        scen_data["link"]["target"].append(target_position)
                        
                        if value_name in constant_variables:
                            #print("SOY CONSTANTE!!!")
                            find_value = (constant_file[value_name][0])

                        elif ("T0 " + value_name) in scen_labels:
                            find_value = (scen_file["T" + str(year) + " " + value_name][num_simulation[0]])

                        #print("HE ENTRADO y valgo:")
                        #print(find_value)
                        
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

                        #print(info_data[value_name])

                        scen_data["link"]["value"].append(find_value)
                        scen_data["link"]["color"].append(info_data[value_name]["color"])

                        #Also, for each connection, it is added the number of the source    
                        scen_data["link"]["source"].append(node_positions[label])

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

    print("INFORMACION EJES X E Y")
    print(node_positions)
    print(scen_data["node"]["x"])
    print(scen_data["node"]["y"])
    
 
        
    return (scen_data, s_e_production, s_e_usage)
