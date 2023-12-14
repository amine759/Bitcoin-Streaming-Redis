import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import json
from utils import *

r, _ = redis_connect()

# Initialize Dash app
app = dash.Dash(__name__)

# Call the function with the sample data
default_n_trades_fig, default_close_price_fig = generate_default_graphs()

event_times = []
n_trades = []
close_prices = []

# Dash layout
app.layout = html.Div(
    [
        html.H1(
            "Bitcoin data from Redis as message broker", style={"textAlign": "center"}
        ),
        html.Button("Start Stream", id="button"),
        html.Img(src="", alt=""),
        dcc.Graph(id="bitcoin-price-graph", figure=default_close_price_fig),
        dcc.Graph(id="trades-count-graph", figure=default_n_trades_fig),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
    ]
)


def dequeue():
    data = []
    while True:
        item = r.lpop("queue")  # Retrieve and remove left-most element from the queue
        if item:
            data.append(json.loads(json.loads(item.decode("utf-8"))))
        else:
            break
    return data


# Callback to update graphs with data from the queue
@app.callback(
    Output("bitcoin-price-graph", "figure"),
    Output("trades-count-graph", "figure"),
    Input("interval-component", "n_intervals"),
    Input("button", "n_clicks"),
)
def update_graph_live(n_intervals, n_clicks):
    global default_close_price_fig, default_n_trades_fig
    
    if n_clicks is not None and n_clicks > 0:
        data_from_queue = dequeue()
        if data_from_queue:
            print(data_from_queue)

            for data in data_from_queue:
                close_prices.append(data["close_price"])
                n_trades.append(data["n_trades"])
                event_times.append(data["event_time"])

            close_prices_fig = {
                "data": [
                    go.Line(
                        x=event_times,
                        y=close_prices,
                        name="Bitcoin Prices",
                    )
                ],
                "layout": go.Layout(
                    title="Bitcoin close Prices per second",
                    xaxis=dict(title="Event Time"),
                    yaxis=dict(title="Price"),
                    width=800,  # Specify the width
                    height=500,
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
                    width=800,  # Specify the width
                    height=500,  # Specify the height
                ),
            }
            default_close_price_fig = close_prices_fig
            default_n_trades_fig = trades_count_fig

            return close_prices_fig, trades_count_fig
    return default_close_price_fig, default_n_trades_fig


if __name__ == "__main__":
    # Run the Dash app
    app.run_server(debug=True)
