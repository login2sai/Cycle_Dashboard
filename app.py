import dash
import dash_core_components as dcc
import dash_html_components as html

# returns top indicator div
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def indicator(text, ind_value):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                ind_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
)