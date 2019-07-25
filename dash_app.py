# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cleaned_df = pd.read_pickle('/Volumes/SeagateBlue/ds/scratch_ds/week-05/lending.pkl')
feature_names = ['Total Received Principal', 'Last Payment Amount',
    'Monthly Payment', 'Recovered Amount After Charged Off', 'Funded Amount']
features_list = ['total_rec_prncp', 'last_pymnt_amnt',
    'installment', 'recoveries', 'funded_amnt']
cleaned_df[cleaned_df['fully_paid']==1]['recoveries'] = cleaned_df[cleaned_df['fully_paid']==1]['recoveries'] + 1
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Charged Off or Fully Paid',
        style={'width': '50%', 'margin':'auto'}
    ),

    html.Div(children='''
        View the distributions of each feature
        for the Charged Off or Fully Paid class.
        ''',
        style={'width': '50%', 'margin':'auto'}
    ),

    html.Div(
        [dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': feature_names[i],
                'value': value}
            for i, value in enumerate(features_list)],
            value='int_rate'
            )
        ],
        style={'width': '50%',
               'margin': 'auto'}
    ),

    dcc.Graph(
        id='density-plot'
    )
])

@app.callback(
dash.dependencies.Output('density-plot', 'figure'),
[dash.dependencies.Input('my-dropdown', 'value')]
)
def update_distplot(value):
    hist_data = [cleaned_df[cleaned_df['fully_paid']==1][value],
                 cleaned_df[cleaned_df['fully_paid']==0][value]
                 ]
    group_labels = ['Paid Off', 'Charged Off']
    colors = ['#333F44', '#37AA9C']

    return ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

if __name__ == '__main__':
    app.run_server(debug=True)
