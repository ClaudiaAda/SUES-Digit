from dash import Dash, dcc, html, Input, Output, callback, div
import plotly.graph_objects as go







# Datos para el gráfico
etiquetas = ['A', 'B', 'C', 'D', 'E']
valores = [10, 23, 7, 15, 12]

# Crear la figura y el gráfico de barras
fig = go.Figure(data=[go.Bar(x=etiquetas, y=valores)])
# Mostrar la figura
fig.update_layout()


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
                            children = "Choose a scenario:"
                        ),
                        dcc.Dropdown(
                            id = "scenario_slider",
                            className = "dropdown",
                            options = [
                                {'label' : 'Scenario 1', 'value' : 1 },
                                {'label' : 'Scenario 2', 'value' : 2 },
                                {'label' : 'Scenario 3', 'value' : 3 },
                                {'label' : 'Scenario 4', 'value' : 4 }
                            ],
                            clearable=False,
                            value=1
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
@callback(
    Output("sankey", "figure"),
    Input("scenario_slider", "value")
)

def update_sankey(value):
    num = value
    print(num)
    if num == 2 :
        # Datos para el gráfico
        etiquetas = ['A', 'B', 'C', 'D', 'E']
        valores = [20, 33, 17, 25, 32]

        # Crear la figura y el gráfico de barras
        fig = go.Figure(data=[go.Bar(x=etiquetas, y=valores)])

        # Mostrar la figura
        fig.update_layout()

    return fig, f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)







