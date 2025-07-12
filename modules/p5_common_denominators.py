import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from fractions import Fraction
from utils.math_helpers import get_lcm_for_list


layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Input(id='p5-fraction-input', placeholder='a/b, c/d, ...', style={'width': '100%'}), width=12)
    ], className="mb-3"),
    dbc.Row(dbc.Col(dbc.Button("Order Fractions", id="p5-order-button", color="primary"), className="text-center mb-4")),
    dbc.Row([
        dbc.Col(id='p5-ordering-steps', md=6),
        dbc.Col(dcc.Graph(id='p5-comparison-barchart'), md=6)
    ])
])


@callback(
    Output('p5-ordering-steps', 'children'),
    Output('p5-comparison-barchart', 'figure'),
    Input('p5-order-button', 'n_clicks'),
    State('p5-fraction-input', 'value'),
    prevent_initial_call=True
)
def order_fractions(n_clicks, input_str):
    if not input_str:
        return "Please enter fractions.", px.bar()
    try:
        fractions_str = [f.strip() for f in input_str.split(',')]
        fractions = [Fraction(f) for f in fractions_str]
    except (ValueError, ZeroDivisionError):
        return html.Div("Invalid input. Please use the format 'a/b, c/d,...'", className="text-danger"), px.bar()

    denominators = [f.denominator for f in fractions]
    lcm = get_lcm_for_list(denominators)
    steps = []
    steps.append(dcc.Markdown(f"The denominators are {', '.join(map(str, denominators))}. LCM is **{lcm}**."))
    steps.append(html.Hr())
    converted = []
    for f in fractions:
        mult = lcm // f.denominator
        new_num = f.numerator * mult
        converted.append({'original': f, 'converted_num': new_num, 'lcm': lcm})
        steps.append(dcc.Markdown(f"$ \\frac{{{f.numerator}}}{{{f.denominator}}} = \\frac{{{new_num}}}{{{lcm}}} $"))
    converted.sort(key=lambda x: x['converted_num'])
    steps.append(html.Hr())
    final_order = ", ".join([f"$\\frac{{{c['original'].numerator}}}{{{c['original'].denominator}}}$" for c in converted])
    steps.append(dcc.Markdown(f"Ordered fractions: {final_order}"))

    df_chart = pd.DataFrame(converted)
    df_chart['original_str'] = df_chart['original'].apply(lambda f: f"{f.numerator}/{f.denominator}")
    fig = px.bar(df_chart, x='original_str', y='converted_num', text='converted_num',
                 labels={'original_str': 'Original Fraction', 'converted_num': f'Equivalent Numerator (out of {lcm})'},
                 title=f"Fractions Compared with Common Denominator ({lcm})")
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis={'categoryorder': 'total ascending'})

    return steps, fig
