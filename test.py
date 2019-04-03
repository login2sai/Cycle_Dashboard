import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from app import indicator

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('Batch_Status.csv')
df_abend = pd.read_csv('Abend_Details.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app_list = [{'label': '--By Application--', 'value': '--By Application--'}]
for app_option in df['Application'].unique():
    app_list.append({'label': app_option, 'value': app_option})

region_list = [{'label': '--By Region--', 'value': '--By Region--'}]
for region_option in df['Region'].unique():
    region_list.append({'label': region_option, 'value': region_option})


app.layout = html.Div([
                html.Div([
                    html.Span("Batch Monitoring Dashboard", className='app-title'),
                    html.Div(
                        html.Img(src='assets/logo.jpg', height="100%"),
                        style={"float": "right", "height": "100%"}
                    )
                ],
                    className="row header",
                    # style={"marginBottom": "5"}
                ),
                html.Div([
                    html.Div(
                        dcc.Dropdown(id='application_drop',
                                     options=app_list,
                                     value='--By Application--',
                                     clearable=False),
                        className="two columns",

                    ),
                    html.Div(
                        dcc.Dropdown(id='region_drop',
                                     options=region_list,
                                     value='--By Region--',
                                     clearable=False),
                        className="two columns",

                    ),
                    html.Div(
                        dcc.Dropdown(id='date_drop',
                                     options=[{'label': '--By Day--', 'value': 'day'},
                                              {'label': '--By Week--', 'value': 'week'},
                                              {'label': '--By Month--', 'value': 'month'}
                                              ],
                                     value='day',
                                     clearable=False),
                        className="two columns"
                    )
                ],
                    className="row",
                    style={"margin": "1% 3%"},
                ),
                html.Div([
                   indicator("Active Cycles Running", "3"),
                   indicator("Cycles Completed", "4"),
                   indicator("Open Abends", "11"),
                ],
                    className="row",
                    style={"margin": "1% 3%"},
                ),


                html.Div([
                    html.Div([
                        html.P("Batch Completion Status"),
                        dcc.Graph(id='graph_status',
                                  config=dict(displayModeBar=False),
                                  style={"height": "89%", "width": "98%"},

                                  )
                    ],
                        className="six columns chart_div",
                    ),
                    html.Div([
                        html.P("Abend Root Cause"),
                        dcc.Graph(id='abend_reasons',
                                  config=dict(displayModeBar=False),
                                  style={"height": "89%", "width": "98%"},
                                  )
                    ],
                        className="six columns chart_div",
                    )
                ],
                    className="row",
                    style={"margin": "1% 3%"},

                ),

                html.Div([
                    html.Div([
                        html.P("Abend Distribution Across Applications"),
                        dcc.Graph(id='abend_dist',
                                  config=dict(displayModeBar=False),
                                  style={"height": "87%", "width": "98%"},
                                  )
                    ],
                        className="six columns chart_div",
                    ),
                    html.Div([
                        html.P("Cycle Completion Trend"),
                        dcc.Graph(id='cycle_trend',
                                  config=dict(displayModeBar=False),
                                  style={"height": "87%", "width": "98%"},
                                  )
                    ],
                        className="six columns chart_div",
                    ),
                    ],
                    className="row",
                    style={"margin": "1% 3%"},
                )
            ],
            )


@app.callback(Output('graph_status', 'figure'),
              [Input('application_drop', 'value'),
               Input('region_drop', 'value')])
def update_status(application, region):

    percent_complete = int(df['Completion'].mean())

    # DATA ONLY FOR THE SELECTED APPLICATION FROM THE DROP-DOWN
    if "--" not in str(application):
        app_filtered_df = df[df['Application'] == application]
        percent_complete = int(app_filtered_df['Completion'].mean())

    # DATA ONLY FOR THE SELECTED REGION FROM THE DROP-DOWN
    if "--" not in str(region):
        region_filtered_df = app_filtered_df[app_filtered_df['Region'] == region]
        percent_complete = int(region_filtered_df['Completion'].mean())

    pie_colors = ['#2BB655', '#9EA0A1']

    fig = {
        "data": [
            {
                "values": [percent_complete, (100-percent_complete)],
                "name": "Batch Status",
                "hoverinfo": "label+percent+name",
                "hole": .6,
                "marker": {'colors': pie_colors},
                "type": "pie",
                "textinfo": "none",
                "opacity": .7
            }],
        "layout": {
            "legend": {
                "orientation": "h"
            },
            "margin": {
                "l": 15,
                "r": 10,
                "t": 0,
                "b": 65
            },
            "autosize": False,

            # "title": "Batch Completion Status",
            "titlefont": {
                "size": 13
            },

            "showlegend": False,
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": str(percent_complete)+'%',
                },
            ]
        }
    }

    return fig


@app.callback(Output('abend_reasons', 'figure'),
              [Input('application_drop', 'value'),
               Input('region_drop', 'value')])
def update_abend_reason(region, application):

    fig = {
        "data": [
            {
                "labels": ["Data Exceptions", "Environmental", "Third-party", "Code", "Other"],
                "values": [20, 30, 10, 25, 15],
                "name": "Batch Status",
                "hoverinfo": "label+percent+name",
                "type": "pie",
                "opacity": .7
            }],

        "layout": {
            "legend": {
                "orientation": "h"
            },
            "margin": {
                "l": 15,
                "r": 10,
                "t": 0,
                "b": 65
            },
        }
    }

    return fig


@app.callback(Output('abend_dist', 'figure'),
              [Input('application_drop', 'value'),
               Input('region_drop', 'value')])
def update_abend_dist(region, application):



    trace0 = go.Bar(x=df_abend['Application'], y=df_abend['INT1'],
                    name='INT1', marker={'color': '#FFC300'}, textposition='auto')

    trace1 = go.Bar(x=df_abend['Application'], y=df_abend['INT2'],
                    name='INT2', marker={'color': '#2E86C1'}, textposition='auto')

    trace2 = go.Bar(x=df_abend['Application'], y=df_abend['SYSTEST'],
                    name='SYSTEST', marker={'color': '#CD7F32'}, textposition='auto')

    data = [trace0, trace1, trace2]

    #layout = dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="v"))
    layout = go.Layout(margin=dict(l=40, r=25, b=40, t=0, pad=4))

    # to have bar stack chart
    # layout = go.Layout(title='Medals',barmode='stack')
    fig = go.Figure(data, layout)

    return fig

@app.callback(Output('cycle_trend', 'figure'),
              [Input('application_drop', 'value'),
               Input('region_drop', 'value')])
def update_abend_dist(region, application):
    y_values_1 = [8, 9, 14, 11, 8, 10, 13, 14, 11, 18]
    x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    y_values_2 = [5, 6, 8, 12, 6, 8, 6, 11, 12, 13]
    x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    y_values_3 = [6, 7, 12, 14, 12, 11, 9, 12, 10, 11]
    x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    y_values_4 = [7, 10, 11, 10, 9, 11, 12, 10, 9, 14]
    x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # regular scatter plot

    trace1 = go.Scatter(x=x_values, y=y_values_1, mode='lines+markers', name='Smartapp')
    trace2 = go.Scatter(x=x_values, y=y_values_2, mode='lines+markers', name='MRPS')
    trace3 = go.Scatter(x=x_values, y=y_values_3, mode='lines+markers', name='AH')
    trace4 = go.Scatter(x=x_values, y=y_values_4, mode='lines+markers', name='WMA')

    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)

    return fig

if __name__ == '__main__':
    app.run_server()

