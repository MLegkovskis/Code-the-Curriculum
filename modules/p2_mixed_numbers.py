import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Mixed Number to Improper Fraction"),
                dbc.CardBody([
                    dbc.InputGroup([
                        dbc.InputGroupText("Whole"),
                        dbc.Input(id='p2-whole-num', type='number', value=1)
                    ], className="mb-2"),
                    dbc.InputGroup([
                        dbc.InputGroupText("Numerator"),
                        dbc.Input(id='p2-numerator', type='number', value=1)
                    ], className="mb-2"),
                    dbc.InputGroup([
                        dbc.InputGroupText("Denominator"),
                        dbc.Input(id='p2-denominator', type='number', value=2)
                    ]),
                    dbc.Button("Convert", id="p2-convert-to-improper", className="mt-3"),
                    html.Div(id='p2-improper-output', className="mt-3", style={'minHeight': '100px'})
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Improper Fraction to Mixed Number"),
                dbc.CardBody([
                    dbc.InputGroup([
                        dbc.InputGroupText("Numerator"),
                        dbc.Input(id='p2-improper-num', type='number', value=3)
                    ], className="mb-2"),
                    dbc.InputGroup([
                        dbc.InputGroupText("Denominator"),
                        dbc.Input(id='p2-improper-den', type='number', value=2)
                    ]),
                    dbc.Button("Convert", id="p2-convert-to-mixed", className="mt-3"),
                    html.Div(id='p2-mixed-output', className="mt-3", style={'minHeight': '100px'})
                ])
            ])
        ], md=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='p2-visualization-graph'), width=12, className="mt-4")
    ])
])


@callback(
    Output('p2-improper-output', 'children'),
    Output('p2-visualization-graph', 'figure'),
    Input('p2-convert-to-improper', 'n_clicks'),
    State('p2-whole-num', 'value'),
    State('p2-numerator', 'value'),
    State('p2-denominator', 'value'),
    prevent_initial_call=True
)
def convert_to_improper(n_clicks, whole, num, den):
    if any(v is None for v in [whole, num, den]) or den == 0:
        return "Please enter valid numbers.", dash.no_update
    improper_num = whole * den + num
    explanation = dcc.Markdown(f"$ {whole} \\frac{{{num}}}{{{den}}} = \\frac{{{improper_num}}}{{{den}}} $")

    fig = px.bar(x=[f"Part {i+1}" for i in range(whole + 1)],
                 y=[den] * whole + [num],
                 labels={'x': 'Units', 'y': f'Segments (out of {den})'},
                 title=f"Visualizing {whole} {num}/{den}")
    fig.update_layout(yaxis_range=[0, den])
    fig.update_traces(marker_color='#17a2b8', texttemplate=[f'{den}/{den}'] * whole + [f'{num}/{den}'], textposition='inside')

    return explanation, fig


@callback(
    Output('p2-mixed-output', 'children'),
    Output('p2-visualization-graph', 'figure', allow_duplicate=True),
    Input('p2-convert-to-mixed', 'n_clicks'),
    State('p2-improper-num', 'value'),
    State('p2-improper-den', 'value'),
    prevent_initial_call=True
)
def convert_to_mixed(n_clicks, num, den):
    if any(v is None for v in [num, den]) or den == 0:
        return "Please enter valid numbers.", dash.no_update

    whole = num // den
    remainder = num % den
    explanation = dcc.Markdown(f"$ {num}/{den} = {whole} \\frac{{{remainder}}}{{{den}}} $")

    df = pd.DataFrame({'Part': ['whole', 'remainder'],
                       'Value': [whole * den, remainder],
                       'Label': [f'{whole} whole units', f'{remainder}/{den}']})
    fig = px.bar(df, x='Part', y='Value', color='Part', text='Label',
                 labels={'Value': f'Total Segments (unit size = {den})'},
                 title=f"Visualizing {num}/{den} as {whole} {remainder}/{den}")
    fig.update_traces(textposition='auto')
    return explanation, fig
