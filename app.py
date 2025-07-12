import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from modules import p1_cancelling, p2_mixed_numbers, p3_multiplying, p4_dividing
from modules import p5_common_denominators, p6_adding_subtracting, p7_finding_fraction_of, p8_quiz

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    html.H2("AQA Further Maths: Fractions Dashboard", className="my-4"),
    dbc.Tabs([
        dbc.Tab(p1_cancelling.layout, label="1. Cancelling Down"),
        dbc.Tab(p2_mixed_numbers.layout, label="2. Mixed Numbers"),
        dbc.Tab(p3_multiplying.layout, label="3. Multiplying"),
        dbc.Tab(p4_dividing.layout, label="4. Dividing"),
        dbc.Tab(p5_common_denominators.layout, label="5. Common Denominators"),
        dbc.Tab(p6_adding_subtracting.layout, label="6. Adding/Subtracting"),
        dbc.Tab(p7_finding_fraction_of.layout, label="7. Fraction of a Quantity"),
        dbc.Tab(p8_quiz.layout, label="8. Practice Quiz"),
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
