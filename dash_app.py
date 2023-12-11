import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Simulated data for demonstration purposes
np.random.seed(0)
time_series = pd.date_range('2023-12-11', periods=100, freq='S')
bitcoin_prices = np.random.randint(35000, 45000, size=100)
n_trades = np.random.randint(5, 20, size=100)

# Initialize Dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.H1("Bitcoin data from redis Queue",style={'textAlign': 'center'}),
    dcc.Graph(id='bitcoin-price-graph', figure={
        'data': [
            go.Scatter(
                x=time_series,
                y=bitcoin_prices,
                mode='lines',
                name='Bitcoin close Price variation per second'
            )
        ],
        'layout': go.Layout(
            title='Bitcoin close Prices per second',
            xaxis=dict(title='event Time'),
            yaxis=dict(title='Price')
        )
    }),
    dcc.Graph(id='trades-count-graph', figure={
        'data': [
            go.Bar(
                x=time_series,
                y=n_trades,
                name='Number of Trades per second'
            )
        ],
        'layout': go.Layout(
            title='Number of Trades',
            xaxis=dict(title='event Time'),
            yaxis=dict(title='Number of Trades per second')
        )
    }),
])

if __name__ == '__main__':
    app.run_server(debug=True)
