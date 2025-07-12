import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from fractions import Fraction
from utils.math_helpers import get_lcm

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Input(id='p6-w1', type='number', placeholder='Whole', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p6-n1', type='number', placeholder='Num', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p6-d1', type='number', placeholder='Den', style={'width': '30%', 'display': 'inline-block'})
        ], md=5),
        dbc.Col(
            dcc.RadioItems(id='p6-operator', options=['+', '-'], value='-', inline=True, className="mt-4 pt-2"),
            md=2, className="text-center"),
        dbc.Col([
            dbc.Input(id='p6-w2', type='number', placeholder='Whole', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p6-n2', type='number', placeholder='Num', style={'width': '30%', 'display': 'inline-block'}),
            dbc.Input(id='p6-d2', type='number', placeholder='Den', style={'width': '30%', 'display': 'inline-block'})
        ], md=5)
    ], className="mb-4"),
    dbc.Row(dbc.Col(dbc.Button("Calculate", id="p6-calculate-button", color="primary"), className="text-center mb-4")),
    dbc.Row(dbc.Col(id='p6-calculation-steps', style={'minHeight': '200px'}))
])


def parse_mixed_input(w, n, d):
    w = w or 0
    if n is None or d is None or d == 0:
        return None
    return Fraction(w * d + n, d)


@callback(
    Output('p6-calculation-steps', 'children'),
    Input('p6-calculate-button', 'n_clicks'),
    State('p6-w1', 'value'), State('p6-n1', 'value'), State('p6-d1', 'value'),
    State('p6-operator', 'value'),
    State('p6-w2', 'value'), State('p6-n2', 'value'), State('p6-d2', 'value'),
    prevent_initial_call=True
)
def perform_add_subtract(n_clicks, w1, n1, d1, op, w2, n2, d2):
    f1 = parse_mixed_input(w1, n1, d1)
    f2 = parse_mixed_input(w2, n2, d2)
    if f1 is None or f2 is None:
        return "Invalid input."
    steps = []
    steps.append(html.H5("Step 1: Convert to Improper Fractions"))
    steps.append(dcc.Markdown(f"First number: $ {w1 or ''} \\frac{{{n1}}}{{{d1}}} = \\frac{{{f1.numerator}}}{{{f1.denominator}}} $"))
    steps.append(dcc.Markdown(f"Second number: $ {w2 or ''} \\frac{{{n2}}}{{{d2}}} = \\frac{{{f2.numerator}}}{{{f2.denominator}}} $"))
    steps.append(html.Hr())
    steps.append(html.H5("Step 2: Find Common Denominator"))
    lcm = get_lcm(f1.denominator, f2.denominator)
    steps.append(dcc.Markdown(f"LCM of {f1.denominator} and {f2.denominator} is **{lcm}**."))
    m1 = lcm // f1.denominator
    m2 = lcm // f2.denominator
    new_f1_num = f1.numerator * m1
    new_f2_num = f2.numerator * m2
    steps.append(dcc.Markdown(f"$ \\frac{{{f1.numerator}}}{{{f1.denominator}}} = \\frac{{{new_f1_num}}}{{{lcm}}} $ and $ \\frac{{{f2.numerator}}}{{{f2.denominator}}} = \\frac{{{new_f2_num}}}{{{lcm}}} $"))
    steps.append(html.Hr())
    steps.append(html.H5("Step 3: Perform Calculation"))
    if op == '+':
        result_num = new_f1_num + new_f2_num
        steps.append(dcc.Markdown(f"$ \\frac{{{new_f1_num}}}{{{lcm}}} + \\frac{{{new_f2_num}}}{{{lcm}}} = \\frac{{{result_num}}}{{{lcm}}} $"))
    else:
        result_num = new_f1_num - new_f2_num
        steps.append(dcc.Markdown(f"$ \\frac{{{new_f1_num}}}{{{lcm}}} - \\frac{{{new_f2_num}}}{{{lcm}}} = \\frac{{{result_num}}}{{{lcm}}} $"))
    final_fraction = Fraction(result_num, lcm)
    steps.append(html.Hr())
    steps.append(html.H5(f"Final Answer: $ {final_fraction.numerator}/{final_fraction.denominator} $", className="text-success"))
    return steps
