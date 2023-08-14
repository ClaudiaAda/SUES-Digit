import json, urllib, requests
import pandas as pd
import numpy as np
from functools import reduce

def build_scen_data(scen_file, year, scenario,value_slider,value_slider2,v_s3,v_s31,v_s4,v_s41,v_s5,v_s6, unit, kommun, peak_hour):
    
    # LOAD PERMANENT DICTIONARY in info_data
    # (There are 3 types of data: 
    # - Normal: Its name appears in the visualisation and has connections with other labels.
    # - Link: Its name does not appear in the visualisation, its value is used for the connection of other labels.
    # - Output: Its name appears, but its value is not used in the Diagram, as it is the final target.)
    with open("Latest Folder/D_All_Labels_Dictionary.json") as dictionary:
        info_data = json.load(dictionary)

    # LOAD CONSTANT ENERGIES information it is permanent for all scenarios
    constant_file = pd.read_csv("Latest Folder\Scenarios/vensim_data_Constants_" + kommun + "_ver.csv")

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
    scen_labels = scen_file.head(0) #Save the first row - labels' names
    columns_names=list(scen_labels)
    column1 = columns_names[1]
    # To select the correct number the values of the table are rounded up
    scen_file[column1] = pd.Series([round(val,2) for val in scen_file[column1]])
    num_simulation = [0]
    
    if(scenario=="All"): # LE HARAN FALTA MODIFICACIONES
        print("Finishing programming")
        column2=columns_names[2]
        #scen_file[column2] = pd.Series([round(val,2) for val in scen_file[column2]])
        column3=columns_names[3]
        column31=columns_names[4]
        column4=columns_names[5]
        column41=columns_names[6]
        column5=columns_names[7]
        column6=columns_names[8]

        # np.where function finds the row where the slider value is.
        cond1 = np.where(scen_file[column1] == value_slider)
        cond2 = np.where(scen_file[column2] == value_slider2)
        cond3 = np.where(scen_file[column3] == v_s3)
        cond31 = np.where(scen_file[column31] == v_s31)
        cond4 = np.where(scen_file[column4] == v_s4)
        cond41 = np.where(scen_file[column41] == v_s41)
        cond5 = np.where(scen_file[column5] == v_s5)
        cond6 = np.where(scen_file[column6] == v_s6)

        # the object obtained is an array, this lines are used so the data can be used later
        cond1 = cond1[0].tolist()
        cond2 = cond2[0].tolist()
        cond3 = cond3[0].tolist()
        cond31 = cond31[0].tolist()
        cond4 = cond4[0].tolist()
        cond41 = cond41[0].tolist()
        cond5 = cond5[0].tolist()
        cond6 = cond6[0].tolist()
        num_simulation = list(set(cond1) & set(cond2) & set(cond3) & set(cond31) & set(cond4) & set(cond41) & set(cond5) & set(cond6))

    elif(scenario=="3" or scenario=="4"):
        column2=columns_names[2]
        scen_file[column2] = pd.Series([round(val,2) for val in scen_file[column2]])

        cond1 = np.where(scen_file[column1] == value_slider)
        cond2 = np.where(scen_file[column2] == value_slider2) 

        cond1 = cond1[0].tolist()
        cond2 = cond2[0].tolist()
        num_simulation = list(set(cond1) & set(cond2))
                                    
    else:
        num_sim = np.where(scen_file[column1] == value_slider)
        num_simulation = num_sim[0].tolist()

    print(num_simulation)
    # The sum of production and usage energies 
    s_e_production = scen_file["T" + year + " sum energy production"][num_simulation[0]]
    s_e_usage = scen_file["T" + year + " sum energy usage"][num_simulation[0]]


    # 1 LOOP: NODES -> Read all the energies stored in the dictionary and
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
                if ("T0 " + label) in scen_labels:
                        node_value = (scen_file["T" + str(year) + " " + label][num_simulation[0]])
                elif label in constant_variables:
                        node_value = (constant_file[label][0])

                # If the value is 0, it will not be stored to display it in the sankey 
                if node_value != 0:
                    # The energy name is stored as it is going to be displayed and 
                    # a number is associated with it (Sankey's diagram works with vectors of numbers)
                    if node_value > 0:
                        node_positions[label] = i
                        # label2 saves the same as label, with the exception of the negativa value
                        label2 = label

                    elif node_value < 0: # Special case that sometimes happens with "electic energy import"
                        node_positions["electric energy export"] = i     
                        node_value = -node_value
                        label2 = "electric energy export"
                        
                    # Save the name of the label, it looks if it has a "translation"
                    # (It displays a different name than the one used in vensim)
                    if "translation" in info_data[label2]:
                        scen_data["node"]["label"].append(info_data[label2]["translation"])
                    else: 
                        scen_data["node"]["label"].append(label2)
                    #Save the color to show
                    scen_data["node"]["color"].append(info_data[label2]["color"])
                    # i is actualised with the number of the next energy
                    i += 1

                    # Calculate percentages:
                    # - percentage_value is used to define the y-position of the energies in the Sankey
                    # - percentage_name is used to show the value of the percentage of the 
                    # energy regarding the sum of energy in the Sankey
                    # Input nodes
                    if info_data[label2]["column"] == 1:
                        percentage_value = node_value/s_e_production
                        percentage_name = str(round(percentage_value,2)*100) + "%"

                    # Intermediate nodes (they do not display percentage)
                    elif info_data[label2]["column"] == 2:
                        percentage_value = node_value/s_e_production
                        percentage_name = ""

                    # Outputs nodes
                    elif info_data[label2]["column"] == 3:
                        percentage_value = node_value/s_e_usage
                        percentage_name = str(round(percentage_value,2)*100) + "%"

                    scen_data["node"]["percentage"].append(percentage_name)

                    # ASSIGN X-Y POSITIONS 
                    # Assign position in x-axis to nodes, x-position is defined
                    # in the dictionary for some special energies. If they do not 
                    # have it defined it is assigned a predefined value
                    if "x" in info_data[label2]:
                        scen_data["node"]["x"].append(info_data[label2]["x"])

                    elif info_data[label2]["column"] == 1:
                        scen_data["node"]["x"].append(0.001)

                    elif info_data[label2]["column"] == 2:
                        scen_data["node"]["x"].append(0.5)

                    elif info_data[label2]["column"] == 3:
                        scen_data["node"]["x"].append(1)
            
                    # Assign position in y-axis to nodes 
                    # The possition is actualised taking in to account the half of the width of the energy
                    # because the possition assigned to the center of the label
                    # Extra code is because when the values are too low sankey make the lines overlap, it is the
                    # fastest solution, do not found the error
                    if "y" in info_data[label2]:
                        scen_data["node"]["y"].append(info_data[label2]["y"])
                        
                    elif info_data[label2]["column"] == 1: # Add to this condition the columns that have very low value 
                        if percentage_value > 0.05:
                            y[info_data[label2]["column"]] += percentage_value/2
                            scen_data["node"]["y"].append(y[info_data[label2]["column"]])
                            # The other half of the width is added for the next energy label
                            y[info_data[label2]["column"]] += (percentage_value/2 - 0.01)

                        else: 
                            y[info_data[label2]["column"]] += 0.015
                            scen_data["node"]["y"].append(y[info_data[label2]["column"]])
                            y[info_data[label2]["column"]] += percentage_value/2 + 0.015

                    else: # If above condition is used for everything it looks bad 
                        y[info_data[label2]["column"]] = y[info_data[label2]["column"]] + percentage_value/2
                        scen_data["node"]["y"].append(y[info_data[label2]["column"]])
                        y[info_data[label2]["column"]] = y[info_data[label2]["column"]] + percentage_value/2
            

    # 2 LOOP: LINKS -> For the energy types used, it declare their connections with their values
    for label in node_positions:

        # Only treat "normal" energy types, the ones with targets(connections).
        if info_data[label]["target"] != ("link" and "output"):
            # There can be more than one connection, so it is evaluated each one (0,a).
            for a in range(len(info_data[label]["target"])):
                # If the variable to connect and the variable that assigns 
                # the value to that connection also exists, it will be added 
                # their numbers to the dictionary for Sankey Diagram, and the color
                target_name = info_data[label]["target"][a]
                value_name = info_data[label]["value"][a]

                # This line checks if the target exists in the simulation
                if target_name in node_positions.keys():
                    
                    target_position = node_positions[target_name]
                    scen_data["link"]["target"].append(target_position)

                    if ("T0 " + value_name) in scen_labels:
                        find_value = abs(scen_file["T" + str(year) + " " + value_name][num_simulation[0]])
                    
                    elif value_name in constant_variables:
                        find_value = constant_file[value_name][0]

                    # Modify value according to unit and if peak hour is chosen
                    # Comprobar una vez tengamos los archivos excel del peak hour
                    """if peak_hour == ['on']:
                        find_value = find_value*3/8760
                        #print("Peak hour")"""

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


    # Comprobar una vez tengamos los archivos excel del peak hour
    """if peak_hour == ['on']:
        s_e_production = s_e_production*3/8760
        s_e_usage = s_e_usage*3/8760
        #print("Peak hour")"""
    
    # Modify values of sum of energies 
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

    print(scen_data)

    return (scen_data, s_e_production, s_e_usage)
