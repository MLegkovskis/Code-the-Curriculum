import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from fractions import Fraction
from utils.math_helpers import get_gcd


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Input(id='p4-whole1', type='number', placeholder='Whole', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p4-num1', type='number', placeholder='Num', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p4-den1', type='number', placeholder='Den', style={'width': '30%', 'display': 'inline-block'})
        ], md=5),
        dbc.Col(html.Div("÷", id='p4-operator', className="text-center h4"), width=2),
        dbc.Col([
            dbc.Input(id='p4-whole2', type='number', placeholder='Whole', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p4-num2', type='number', placeholder='Num', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p4-den2', type='number', placeholder='Den', style={'width': '30%', 'display': 'inline-block'})
        ], md=5)
    ], align="center", justify="center", className="mb-4"),
    dbc.Row(dbc.Col(dbc.Button("Calculate Division", id="p4-calculate-button", color="primary"), className="text-center mb-4")),
    dbc.Row([
        dbc.Col(html.Div(id='p4-division-steps', className='lead'), width=12)
    ]),
    dcc.Store(id='p4-division-store')
])


def parse_fraction_input(whole, num, den):
    if whole is None:
        whole = 0
    if num is None or den is None or den == 0:
        return None
    return Fraction(whole * den + num, den)


@callback(
    Output('p4-division-steps', 'children'),
    Output('p4-division-store', 'data'),
    Input('p4-calculate-button', 'n_clicks'),
    State('p4-whole1', 'value'), State('p4-num1', 'value'), State('p4-den1', 'value'),
    State('p4-whole2', 'value'), State('p4-num2', 'value'), State('p4-den2', 'value'),
    prevent_initial_call=True
)
def perform_division(n_clicks, w1, n1, d1, w2, n2, d2):
    f1 = parse_fraction_input(w1, n1, d1)
    f2 = parse_fraction_input(w2, n2, d2)
    if f1 is None or f2 is None:
        return "Invalid input.", dash.no_update
    steps = []
    steps.append(dcc.Markdown(fr"Start with: $ {f1} \div {f2} $"))
    inverted = Fraction(f2.denominator, f2.numerator)
    steps.append(dcc.Markdown(fr"Invert second fraction: $ {f1} \times {inverted} $"))
    result = f1 * inverted
    steps.append(dcc.Markdown(f"Result: $ {result.numerator}/{result.denominator} $"))
    store_data = {'steps': [c.to_plotly_json() for c in steps], 'current_step': 0}
    return steps, store_data
