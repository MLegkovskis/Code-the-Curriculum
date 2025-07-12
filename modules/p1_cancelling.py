import random
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.math_helpers import get_simplification_steps


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Numerator"),
            dcc.Slider(id='p1-numerator-slider', min=1, max=20, step=1, value=8)
        ], md=6),
        dbc.Col([
            html.Label("Denominator"),
            dcc.Slider(id='p1-denominator-slider', min=1, max=20, step=1, value=12)
        ], md=6),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Button("Try Random Fraction", id='p1-random-button', color='secondary'), md=6),
        dbc.Col(dbc.Button("Simplify This Fraction", id='p1-simplify-button', color='primary'), md=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div(id='p1-simplification-output', className='lead'), md=6),
        dbc.Col(dcc.Graph(id='p1-fraction-pie-chart'), md=6)
    ]),
    dcc.Store(id='p1-simplification-store'),
    dcc.Interval(id='p1-interval-timer', interval=1500, n_intervals=0, disabled=True)
])


@callback(
    Output('p1-numerator-slider', 'value'),
    Output('p1-denominator-slider', 'value'),
    Input('p1-random-button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_random_fraction(n_clicks):
    base_num = random.randint(1, 5)
    base_den = random.randint(base_num + 1, 10)
    multiplier = random.randint(2, 6)
    return base_num * multiplier, base_den * multiplier


@callback(
    Output('p1-simplification-store', 'data'),
    Output('p1-fraction-pie-chart', 'figure'),
    Output('p1-interval-timer', 'disabled'),
    Output('p1-simplification-output', 'children'),
    Input('p1-simplify-button', 'n_clicks'),
    State('p1-numerator-slider', 'value'),
    State('p1-denominator-slider', 'value'),
    prevent_initial_call=True
)
def start_simplification(n_clicks, num, den):
    if den == 0:
        return dash.no_update, dash.no_update, True, "Denominator cannot be zero"

    steps = get_simplification_steps(num, den)
    store_data = {'steps': steps, 'current_step': 0}

    df = pd.DataFrame({'value': [num, den-num], 'category': ['Numerator', 'Denominator Part']})
    fig = px.pie(df, values='value', names='category',
                 title=f'Visualizing the Fraction: {num}/{den}',
                 color_discrete_map={'Numerator': '#1f77b4', 'Denominator Part': '#aec7e8'})
    fig.update_traces(textinfo='value')

    initial_text = html.Span(steps[0])
    return store_data, fig, False, initial_text


@callback(
    Output('p1-simplification-output', 'children', allow_duplicate=True),
    Output('p1-interval-timer', 'disabled', allow_duplicate=True),
    Input('p1-interval-timer', 'n_intervals'),
    State('p1-simplification-store', 'data'),
    prevent_initial_call=True
)
def update_step_by_step(n_intervals, store_data):
    if not store_data:
        return dash.no_update, True

    current_step_index = store_data.get('current_step', 0) + 1
    steps = store_data.get('steps', [])

    if current_step_index >= len(steps):
        return dash.no_update, True

    store_data['current_step'] = current_step_index
    displayed_text = "".join(steps[:current_step_index + 1])
    disable_timer = current_step_index == len(steps) - 1

    return html.Span(displayed_text), disable_timer
