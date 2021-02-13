import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Output, Input

from dash_app.recyclingdata import RecyclingData
from dash_app.recyclingchart import RecyclingChart, RecyclingBarChart

# Prepare the data
data = RecyclingData()
area = 'London'
data.process_data_for_area(area)

# Create the figures
rc = RecyclingChart(data)
fig1 = rc.create_chart(area)
rcb = RecyclingBarChart(data)
fig2 = rcb.create_chart('2018/19')


# Create a Dash app
def init_dashboard(flask_app):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=flask_app,
                         routes_pathname_prefix="/dash_app/",
                         external_stylesheets=[dbc.themes.LITERA],
                         )

    dash_app.layout = dbc.Container(fluid=True, children=[
        html.Br(),
        html.H1('Waste and recycling'),
        html.P('Turn London waste into an opportunity – by reducing waste, reusing and recycling more of it.',
               className='lead'),
        dbc.Row([
            dbc.Col(width=3, children=[
                dbc.FormGroup([
                    html.H4("Select Area"),
                    dcc.Dropdown(id="area_select", options=[{"label": x, "value": x} for x in data.area_list],
                                 value="London")
                ]),
                html.Br(),
                html.Div(id="output-panel")
            ]),
            dbc.Col(width=9, children=[
                dbc.Tabs(className="nav nav-pills", children=[
                    dbc.Tab(dcc.Graph(id="recycle-chart", figure=fig1), label="Recycling by area"),
                    dbc.Tab(dcc.Graph(id="recycle-year", figure=fig2), label="Recycling by year"),
                ])
            ]),
        ]),
    ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output("output-panel", "children"), [Input("area_select", "value")])
    def render_output_panel(area_select):
        data.process_data_for_area(area_select)
        panel = html.Div([
            html.H4(area_select, id="card_name"),
            dbc.Card(body=True, className="bg-dark text-light", children=[
                html.Br(),
                html.H6("Compared to England:", className="card-title"),
                html.H4("{:,.0f}%".format(data.compare_to_eng), className="card-text text-light"),
                html.Br(),
                html.H6("Compared to previous year:".format(area=area), className="card-title"),
                html.H4("{:,.0f}%".format(data.change_area), className="card-text text-light"),
                html.Br(),
                html.H6("Best period:", className="card-title"),
                html.H4(data.best_period, className="card-text text-light"),
                html.H6("with recycling rate {:,.0f}%".format(data.best_rate), className="card-title text-light"),
                html.Br()
            ])
        ])
        return panel

    @dash_app.callback(Output("recycle-chart", "figure"), [Input("area_select", "value")])
    def update_recycling_chart(area_select):
        fig = rc.create_chart(area_select)
        return fig
