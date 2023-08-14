import plotly.graph_objects as go
import pandas as pd


def build_sankey(scen_data,actual_unit):
    # Code to display the Sankey Diagram, it fils the inputs with 
    # the scenario dictionary : scen_data
    fig = go.Figure(data=[go.Sankey(
        arrangement = 'freeform',
        valuesuffix = " "+ actual_unit,
        valueformat = ".2f",
        # Define nodes
        node = dict(
            thickness = 15,
            line = dict(color = "black", width = 0.01),
            label =  scen_data["node"]['label'],
            color =  scen_data["node"]['color'],
            x = scen_data["node"]["x"],
            y = scen_data["node"]["y"],
            pad = 30,
            customdata= scen_data["node"]["percentage"],
            hovertemplate='<b>%{label}</b><br>'+'%{value} <br>'+'%{customdata}'+'<extra></extra>'
        ),
        # Add links
        link = dict(
            arrowlen = 30,
            source =  scen_data["link"]['source'],
            target =  scen_data["link"]['target'],
            color =  scen_data["link"]['color'],
            value = scen_data["link"]['value'],
        )
    )])
 
    fig.update_layout(
        #width = 500, #These 2 parameters determine the size of the graphic
        height = 800,
    )

    fig.update_traces(
        hoverlabel_namelength = -1
    )

    #print(scen_data["node"]['label'])
    #print(scen_data["node"]['color'])
    #print(scen_data["node"]["percentage"])
    #print(scen_data)
    #print(scen_data)
    #print(scen_data)

    return fig
