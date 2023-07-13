from dash import Dash, dcc, html, Input, Output, State, callback


app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
                id = "scenario_menu",
                 options = [
                    {'label' : 'Scenario 1', 'value' : 1 },
                    {'label' : 'Scenario 2', 'value' : 2 },
                    {'label' : 'Scenario 3', 'value' : 3 },
                    {'label' : 'Scenario 3.1', 'value' : 31 },
                    {'label' : 'Scenario 4', 'value' : 4 },
                    {'label' : 'Scenario 4.1', 'value' : 41 },
                    {'label' : 'Scenario 5', 'value' : 5 },
                    {'label' : 'Scenario 6', 'value' : 6 }
                ],
                placeholder='Please select...'
                ),
    dcc.Slider(
                min=0.5,
                max=1,
                step=0.25,
                value=None,
                #marks={k: '{}'.format(k) for k in range(0,21)},
                #tooltip={"placement" : "bottom", "always_visible" : True},
                id="slider",
                #vertical=True
                ),
    html.Div(
        id="text",
        #html.Label(slider_scale)
    )
])

@app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "step"),
    #Output("text", "slider_scale"),
    #Output("slider", "marks"),
    Input("scenario_menu", "value"),
    State("slider", "min"),
    State("slider", "max"),
    State("slider", "step"),
    #State("slider", "marks")
    )

def update_output(value, min, max, step):
    if value == 1:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step)   #{k: '{}'.format(k) for k in range(min,max+1)}
    if value == 2:  
        min=0
        max=2
        step=1
        return (min, max, step)   
    if value == 3:  
        min=100
        max=300
        step=100
        return (min, max, step)
    if value == 31:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step)
    if value == 4:  
        min=0.5
        max=1
        step=0.25
        return (min, max, step)
    if value == 41:  
        min=0.96
        max=1
        step=0.04
        return (min, max, step)
    if value == 5:  
        min=6
        max=12
        step=3
        return (min, max, step)
    if value == 6:  
        min=0
        max=2
        step=1
        return (min, max, step)

"""def slider_scale(value):
    if value == 1 or value==31 or value==4 or value==41:
        return  '%'
    else:    
        return 'units'
"""

if __name__ == '__main__':
    app.run(debug=True)