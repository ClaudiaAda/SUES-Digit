from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json, urllib, requests, pprint






# Datos para el gráfico
etiquetas = ['A', 'B', 'C', 'D', 'E']
valores = [10, 23, 7, 15, 12]

# Crear la figura y el gráfico de barras
fig = go.Figure(data=[go.Bar(x=etiquetas, y=valores)])
# Mostrar la figura"""
figure = fig.update_layout()


app = Dash(__name__)
app.title = "Sankey Diagram"

app.layout = html.Div(
    id = "app_sankey",
    children = [
        html.Div(
            id = "Header_area",
            children = [
                html.H1(
                    id = "header_title",
                    children = "title", style={"textAlign" : "left"}
                ),
                html.P(
                    id = "header_description",
                    children = "que bonito que es nuestro sankey jefa",
                ),
            ],
        ),
        html.Div(
            id = "menu_area",
            children = [
                html.Div(
                    children = [
                        html.Div(
                            className = "menu_title",
                            id = "menu",
                            children = "Choose a scenario:"
                        ),
                        dcc.Dropdown(
                            id = "scenario_slider",
                            className = "dropdown",
                            options = [
                                {'label' : 'Scenario 1', 'value' : 1 },
                                {'label' : 'Scenario 2', 'value' : 2 },
                                {'label' : 'Scenario 3', 'value' : 3 },
                                {'label' : 'Scenario 4', 'value' : 4 },
                                {'label' : 'Scenario 5', 'value' : 5 },
                                {'label' : 'Scenario 6', 'value' : 6 },
                                {'label' : 'Scenario All', 'value' : 7 }
                            ],
                            clearable=False,
                            value=5
                        )

                    ]
                )
            ]
        ),
        html.Div(
            id = "graph_area",
            children = dcc.Graph(
                id = "sankey",
                figure = fig,
                config = {"displayModeBar":False}
            ),
        ),
    ]
)
            
            
#connecting the dropdown values 
@app.callback(
    Output("sankey", "figure"),
    Input("scenario_slider", "value")
)

def update_sankey(value):
    num = value
    print(num)

    # SELECT THE URL OF EACH SCENARIO CASE
    url_scenarios_cases = 'https://raw.githubusercontent.com/ClaudiaAda/SUES-Digit/main/Scenarios_cases.json'
    response_scenario_cases = urllib.request.urlopen(url_scenarios_cases)
    info_scenarios_cases = json.loads(response_scenario_cases.read())

    





    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
