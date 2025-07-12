import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from fractions import Fraction
from utils.math_helpers import get_gcd


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("First Fraction"),
            dbc.Input(id='p3-num1', type='number', placeholder='Numerator', value=1, style={'width': '45%', 'display': 'inline-block'}),
            html.Span('/', style={'margin': '0 5px'}),
            dbc.Input(id='p3-den1', type='number', placeholder='Denominator', value=2, style={'width': '45%', 'display': 'inline-block'})
        ], md=6),
        dbc.Col([
            html.Label("Second Fraction"),
            dbc.Input(id='p3-num2', type='number', placeholder='Numerator', value=1, style={'width': '45%', 'display': 'inline-block'}),
            html.Span('/', style={'margin': '0 5px'}),
            dbc.Input(id='p3-den2', type='number', placeholder='Denominator', value=2, style={'width': '45%', 'display': 'inline-block'})
        ], md=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Button("Calculate", id='p3-calculate-button', color='primary'), md=6),
        dbc.Col(dbc.Button("Next Step", id='p3-next-step-button', color='secondary', disabled=True), md=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div(id='p3-multiplication-steps', className='lead'), md=6),
        dbc.Col(dcc.Graph(id='p3-area-model-graph'), md=6)
    ]),
    dcc.Store(id='p3-multiplication-store')
])


def create_area_model(f1: Fraction, f2: Fraction):
    fig = go.Figure()
    for i in range(f1.denominator + 1):
        fig.add_shape(type="line", x0=i, y0=0, x1=i, y1=f2.denominator, line=dict(color="lightgrey"))
    for i in range(f2.denominator + 1):
        fig.add_shape(type="line", x0=0, y0=i, x1=f1.denominator, y1=i, line=dict(color="lightgrey"))
    fig.add_shape(type="rect", x0=0, y0=0, x1=f1.numerator, y1=f2.denominator,
                  fillcolor="rgba(255,0,0,0.3)", line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=f1.denominator, y1=f2.numerator,
                  fillcolor="rgba(0,0,255,0.3)", line_width=0)
    fig.update_layout(xaxis=dict(range=[0, f1.denominator], showgrid=False, showticklabels=False),
                      yaxis=dict(range=[0, f2.denominator], showgrid=False, showticklabels=False, scaleanchor="x", scaleratio=1),
                      title=f"Area Model: {f1} \u00D7 {f2}", plot_bgcolor='white')
    return fig


@callback(
    Output('p3-multiplication-store', 'data'),
    Output('p3-next-step-button', 'disabled'),
    Output('p3-multiplication-steps', 'children'),
    Output('p3-area-model-graph', 'figure'),
    Input('p3-calculate-button', 'n_clicks'),
    State('p3-num1', 'value'), State('p3-den1', 'value'),
    State('p3-num2', 'value'), State('p3-den2', 'value'),
    prevent_initial_call=True
)
def start_multiplication(n_clicks, n1, d1, n2, d2):
    if any(v is None for v in [n1, d1, n2, d2]) or d1 == 0 or d2 == 0:
        return dash.no_update, True, "Invalid input", go.Figure()

    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    steps = []
    current_n1, current_d1, current_n2, current_d2 = n1, d1, n2, d2
    steps.append(f"Initial: $ \\frac{{{n1}}}{{{d1}}} \times \\frac{{{n2}}}{{{d2}}} $")
    gcd1 = get_gcd(current_n1, current_d2)
    if gcd1 > 1:
        new_n1, new_d2 = current_n1 // gcd1, current_d2 // gcd1
        steps.append(f"Cancel {current_n1} and {current_d2} by {gcd1}: $ \\frac{{{new_n1}}}{{{current_d1}}} \times \\frac{{{current_n2}}}{{{new_d2}}} $")
        current_n1, current_d2 = new_n1, new_d2
    gcd2 = get_gcd(current_n2, current_d1)
    if gcd2 > 1:
        new_n2, new_d1 = current_n2 // gcd2, current_d1 // gcd2
        steps.append(f"Cancel {current_n2} and {current_d1} by {gcd2}: $ \\frac{{{current_n1}}}{{{new_d1}}} \times \\frac{{{new_n2}}}{{{current_d2}}} $")
        current_n2, current_d1 = new_n2, new_d1
    result_num = current_n1 * current_n2
    result_den = current_d1 * current_d2
    steps.append(f"Multiply: $ \\frac{{{result_num}}}{{{result_den}}} $")
    store_data = {'steps': steps, 'current_step': 0}
    fig = create_area_model(Fraction(current_n1, current_d1), Fraction(current_n2, current_d2))
    return store_data, False, dcc.Markdown(steps[0]), fig


@callback(
    Output('p3-multiplication-steps', 'children', allow_duplicate=True),
    Output('p3-next-step-button', 'disabled', allow_duplicate=True),
    Input('p3-next-step-button', 'n_clicks'),
    State('p3-multiplication-store', 'data'),
    prevent_initial_call=True
)
def advance_multiplication_step(n_clicks, store_data):
    if not store_data or n_clicks == 0:
        return dash.no_update, dash.no_update

    current_step = store_data.get('current_step', 0) + 1
    steps = store_data.get('steps', [])
    if current_step >= len(steps):
        return dash.no_update, True

    store_data['current_step'] = current_step
    disable_button = current_step == len(steps) - 1
    return dcc.Markdown(steps[current_step]), disable_button
