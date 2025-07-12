import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from fractions import Fraction
from utils.math_helpers import (
    get_add_subtract_steps,
    get_multiplication_steps,
    get_division_steps,
)

layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader("Question 1"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Span("(a) 3/10 \u00d7 13/8 ="), md=4),
                dbc.Col([
                    dbc.Input(id='q1a-num', type='number', placeholder='Num', style={'width': '40%', 'display': 'inline-block'}),
                    html.Span('/', style={'margin': '0 5px'}),
                    dbc.Input(id='q1a-den', type='number', placeholder='Den', style={'width': '40%', 'display': 'inline-block'})
                ], md=4),
                dbc.Col(html.Div(id='q1a-feedback-icon'), md=1),
                dbc.Col(html.Div(id='q1a-feedback-solution'), md=3)
            ], align="center", className="mb-3"),
            dbc.Row([
                dbc.Col(html.Span("(b) 7/12 \u00f7 19/8 ="), md=4),
                dbc.Col([
                    dbc.Input(id='q1b-num', type='number', placeholder='Num', style={'width': '40%', 'display': 'inline-block'}),
                    html.Span('/', style={'margin': '0 5px'}),
                    dbc.Input(id='q1b-den', type='number', placeholder='Den', style={'width': '40%', 'display': 'inline-block'})
                ], md=4),
                dbc.Col(html.Div(id='q1b-feedback-icon'), md=1),
                dbc.Col(html.Div(id='q1b-feedback-solution'), md=3)
            ], align="center", className="mb-3"),
            dbc.Row([
                dbc.Col(html.Span("(c) 3 5/12 + 2 9/24 ="), md=4),
                dbc.Col([
                    dbc.Input(id='q1c-w', type='number', placeholder='Whole', style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Input(id='q1c-n', type='number', placeholder='Num', style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Input(id='q1c-d', type='number', placeholder='Den', style={'width': '25%', 'display': 'inline-block'})
                ], md=4),
                dbc.Col(html.Div(id='q1c-feedback-icon'), md=1),
                dbc.Col(html.Div(id='q1c-feedback-solution'), md=3)
            ], align="center", className="mb-3"),
            dbc.Row([
                dbc.Col(html.Span("(d) 2 3/4 - 4 5/6 ="), md=4),
                dbc.Col([
                    dbc.Input(id='q1d-w', type='number', placeholder='Whole', style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Input(id='q1d-n', type='number', placeholder='Num', style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Input(id='q1d-d', type='number', placeholder='Den', style={'width': '25%', 'display': 'inline-block'})
                ], md=4),
                dbc.Col(html.Div(id='q1d-feedback-icon'), md=1),
                dbc.Col(html.Div(id='q1d-feedback-solution'), md=3)
            ], align="center", className="mb-3"),
        ])
    ], className="mb-4"),
    dbc.Card([
        dbc.CardHeader("Question 2"),
        dbc.CardBody([
            html.Div("A tank holds 200 litres. 3/4 of the water is used. How many litres remain?"),
            dbc.Input(id='q2-answer', type='number', placeholder='Answer'),
            html.Div(id='q2-feedback-icon'),
            html.Div(id='q2-feedback-solution')
        ])
    ], className="mb-4"),
    dbc.Row(dbc.Col(dbc.Button("Check My Answers", id="check-answers-button", color="success", size="lg"), className="text-center"))
])


@callback(
    Output('q1a-feedback-icon', 'children'), Output('q1a-feedback-solution', 'children'),
    Output('q1b-feedback-icon', 'children'), Output('q1b-feedback-solution', 'children'),
    Output('q1c-feedback-icon', 'children'), Output('q1c-feedback-solution', 'children'),
    Output('q1d-feedback-icon', 'children'), Output('q1d-feedback-solution', 'children'),
    Output('q2-feedback-icon', 'children'), Output('q2-feedback-solution', 'children'),
    Input('check-answers-button', 'n_clicks'),
    State('q1a-num', 'value'), State('q1a-den', 'value'),
    State('q1b-num', 'value'), State('q1b-den', 'value'),
    State('q1c-w', 'value'), State('q1c-n', 'value'), State('q1c-d', 'value'),
    State('q1d-w', 'value'), State('q1d-n', 'value'), State('q1d-d', 'value'),
    State('q2-answer', 'value'),
    prevent_initial_call=True
)
def check_all_answers(n_clicks, q1a_n, q1a_d, q1b_n, q1b_d, q1c_w, q1c_n, q1c_d, q1d_w, q1d_n, q1d_d, q2_ans):
    answers = {
        'q1a': Fraction(39, 80),
        'q1b': Fraction(14, 57),
        'q1c': Fraction(47, 8),
        'q1d': Fraction(-25, 12),
        'q2': 50
    }
    correct_icon = html.I(className="fas fa-check-circle text-success")
    wrong_icon = html.I(className="fas fa-times-circle text-danger")

    try:
        user_q1a = Fraction(q1a_n, q1a_d)
        icon_a = correct_icon if user_q1a == answers['q1a'] else wrong_icon
        sol_a = "" if user_q1a == answers['q1a'] else get_multiplication_steps(Fraction(3, 10), Fraction(13, 8))[0]
    except Exception:
        icon_a = wrong_icon
        sol_a = "Invalid input."

    try:
        user_q1b = Fraction(q1b_n, q1b_d)
        icon_b = correct_icon if user_q1b == answers['q1b'] else wrong_icon
        sol_b = "" if user_q1b == answers['q1b'] else get_division_steps(Fraction(7, 12), Fraction(19, 8))[0]
    except Exception:
        icon_b = wrong_icon
        sol_b = "Invalid input."

    try:
        user_q1c = Fraction((q1c_w or 0) * q1c_d + q1c_n, q1c_d)
        icon_c = correct_icon if user_q1c == answers['q1c'] else wrong_icon
        sol_c = "" if user_q1c == answers['q1c'] else get_add_subtract_steps(Fraction(41, 12), Fraction(57, 24), '+')[0]
    except Exception:
        icon_c = wrong_icon
        sol_c = "Invalid input."

    try:
        if q1d_w is not None and q1d_w < 0:
            user_q1d = Fraction(q1d_w * q1d_d - q1d_n, q1d_d)
        else:
            user_q1d = Fraction((q1d_w or 0) * q1d_d + q1d_n, q1d_d)
        icon_d = correct_icon if user_q1d == answers['q1d'] else wrong_icon
        sol_d = "" if user_q1d == answers['q1d'] else get_add_subtract_steps(Fraction(11, 4), Fraction(29, 6), '-')[0]
    except Exception:
        icon_d = wrong_icon
        sol_d = "Invalid input."

    icon_q2 = correct_icon if q2_ans == answers['q2'] else wrong_icon
    sol_q2 = "" if q2_ans == answers['q2'] else "Expected 50"

    return icon_a, sol_a, icon_b, sol_b, icon_c, sol_c, icon_d, sol_d, icon_q2, sol_q2
