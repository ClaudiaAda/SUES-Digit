import plotly.graph_objects as go
import pandas as pd

def build_sankey(scen_data):
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