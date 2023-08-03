import plotly.graph_objects as go
import pandas as pd


def build_sankey(scen_data,actual_unit):
    # Code to display the Sankey Diagram, it fils the inputs with 
    # the scenario dictionary : scen_data
    lista_unit=[]
    print("estoy dentro del sankey")
    print(actual_unit)
    for a in range(len(scen_data['node']['label'])):
        lista_unit.append(actual_unit)

    print(lista_unit)
    fig = go.Figure(data=[go.Sankey(
        arrangement = 'snap',
        # Define nodes
        node = dict(
            pad = 30,
            thickness = 15,
            line = dict(color = "black", width = 0.01),
            label =  scen_data["node"]['label'],
            color =  scen_data["node"]['color'],
            x = scen_data["node"]["x"],
            y = scen_data["node"]["y"],
            customdata= lista_unit,
            hovertemplate='<b>%{label}</b><br>'+'%{value}'+' '+ '%{customdata}<br>'+'%{percentage}%'+'<extra></extra>',
            
        ),
        # Add links
        link = dict(
            arrowlen = 30,
            source =  scen_data["link"]['source'],
            target =  scen_data["link"]['target'],
            color =  scen_data["link"]['color'],
            value = scen_data["link"]['value'],
            customdata= lista_unit,
            hovertemplate='<b>%{source}</b><br>'+'%{value}'+' '+ '%{customdata}<br>'+'<extra></extra>',
    ))])
 
    fig.update_layout(
        #width = 1700, #These 2 parameters determine the size of the graphic
        height = 800,
    )
    fig.add_trace(go.Scatter(
        customdata= scen_data["node"]["percentage"],
        hovertemplate= '%{customdata}',

    ))

    return fig


    # Assign position in y-axis to nodes
    """for label in list(positions.keys()):
        y_position = positions[label] * scen_data["link"]["value"][i]
        scen_data["node"]["y"].append(y_position)"""