import plotly.graph_objects as go
import pandas as pd

def build_sankey(scen_data):
    # Code to display the Sankey Diagram, it fils the inputs with 
    # the scenario dictionary : scen_data
    fig = go.Figure(data=[go.Sankey(
        arrangement = 'snap',
        # Define nodes
        node = dict(
            pad = 30,
            thickness = 15,
            line = dict(color = "black", width = 0.01),
            label =  scen_data["node"]['label'],
            color =  scen_data["node"]['color'],
            #x = scen_data["node"]["x"],
            #y = scen_data["node"]["y"],
        ),
        # Add links
        link = dict(
            arrowlen = 30,
            source =  scen_data["link"]['source'],
            target =  scen_data["link"]['target'],
            color =  scen_data["link"]['color'],
            value = scen_data["link"]['value'],
    ))])
 
    fig.update_layout(
        #width = 1700, #These 2 parameters determine the size of the graphic
        height = 800,
    )

    return fig


    # Assign position in y-axis to nodes
    """for label in list(positions.keys()):
        y_position = positions[label] * scen_data["link"]["value"][i]
        scen_data["node"]["y"].append(y_position)"""