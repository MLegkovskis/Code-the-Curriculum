import re
import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Fraction"),
            dcc.Input(id='p7-fraction-input', type='text', value='2/9', style={'width': '100%'})
        ], md=4),
        dbc.Col([
            html.Label("Of Quantity"),
            dcc.Input(id='p7-quantity-input', type='text', value='£360', style={'width': '100%'})
        ], md=4)
    ], className="mb-4", justify="center"),
    dbc.Row([
        dbc.Col(dbc.Button("Divide First", id='p7-divide-first-btn', color='secondary'), width='auto'),
        dbc.Col(dbc.Button("Multiply First", id='p7-multiply-first-btn', color='primary'), width='auto')
    ], className="text-center mb-4"),
    dbc.Row([
        dbc.Col(id='p7-calculation-output', className="lead text-center", style={'minHeight': '100px'})
    ])
])


@callback(
    Output('p7-calculation-output', 'children'),
    Input('p7-divide-first-btn', 'n_clicks'),
    Input('p7-multiply-first-btn', 'n_clicks'),
    State('p7-fraction-input', 'value'),
    State('p7-quantity-input', 'value'),
    prevent_initial_call=True
)
def find_fraction_of(div_clicks, mul_clicks, frac_str, quant_str):
    if not frac_str or not quant_str:
        return "Please provide all inputs."
    button_id = ctx.triggered_id
    try:
        num, den = map(int, frac_str.split('/'))
        currency_symbol = re.match(r'[^0-9.]*', quant_str).group(0)
        quantity = float(re.sub(r'[^0-9.]', '', quant_str))
    except (ValueError, ZeroDivisionError):
        return html.Div("Invalid input. Use 'a/b' for fraction and a number for quantity.", className="text-danger")
    if button_id == 'p7-divide-first-btn':
        step1 = quantity / den
        result = step1 * num
        calc = fr"$ ( {currency_symbol}{quantity} \div {den} ) \times {num} = {currency_symbol}{step1:.2f} \times {num} = {currency_symbol}{result:.2f} $"
        return dcc.Markdown(calc)
    elif button_id == 'p7-multiply-first-btn':
        step1 = quantity * num
        result = step1 / den
        calc = fr"$ ( {currency_symbol}{quantity} \times {num} ) \div {den} = {currency_symbol}{step1:.2f} \div {den} = {currency_symbol}{result:.2f} $"
        return dcc.Markdown(calc)
    return dash.no_update
