import dash
from dash import dcc, html
import plotly.graph_objs as go
from subscriber import get_data_from_queue
from dash.dependencies import Input, Output, State

# Initialize Dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div(
    [
        html.H1("Bitcoin data from redis Queue", style={"textAlign": "center"}),
        html.Button("Start Streaming", id="start-stream-button", n_clicks=0),
        dcc.Graph(id="bitcoin-price-graph"),
        dcc.Graph(id="trades-count-graph"),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in update frequency milliseconds
            n_intervals=0
        )
    ]
)

@app.callback(
    [
        Output("bitcoin-price-graph", "figure"),
        Output("trades-count-graph", "figure"),
    ],
    [
        Input("start-stream-button", "n_clicks"),
        Input('interval-component', 'n_intervals')
    ],
    [
        State('bitcoin-price-graph', 'figure'),
        State('trades-count-graph', 'figure'),
    ]
)

def update_graph_live(n_clicks,n_intervals, bitcoin_fig, trades_fig):
    if n_clicks:
        # Reset lists for every click to avoid data accumulation
        event_times = []
        n_trades = []
        close_prices = []

        data_from_queue = get_data_from_queue()

        if data_from_queue:
            print(data_from_queue)
            for item in data_from_queue:
                close_prices.append(item["close_price"])
                n_trades.append(item["n_trad    es"])
                event_times.append(item["event_time"])

            close_prices_fig = {
                "data": [
                    go.Scatter(
                        x=event_times,
                        y=close_prices,
                        mode="lines",
                        name="Bitcoin Prices",
                    )
                ],
                "layout": go.Layout(
                    title="Bitcoin close Prices per second",
                    xaxis=dict(title="Event Time"),
                    yaxis=dict(title="Price"),
                ),
            }

            trades_count_fig = {
                "data": [
                    go.Bar(
                        x=event_times, y=n_trades, name="Number of Trades per second"
                    )
                ],
                "layout": go.Layout(
                    title="Number of Trades per second",
                    xaxis=dict(title="Event Time"),
                    yaxis=dict(title="Number of Trades per second"),
                ),
            }

            return close_prices_fig, trades_count_fig

    return bitcoin_fig, trades_fig

if __name__ == "__main__":
    app.run_server(debug=True)
