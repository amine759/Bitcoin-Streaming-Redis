import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import json
import redis
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieving environment variables
redis_host = os.environ.get("redis_host")
channel = os.environ.get("channel")
redis_port = os.environ.get("redis_port")

# Redis connection setup
r = redis.StrictRedis(host=redis_host, port=redis_port)


# Function to handle subscription to the Redis channel
async def subscribe_to_channel():
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        # Process received message
        if message["type"] == "message":
            message_data = message["data"].decode("utf-8")
            process_queue(message_data)


def process_queue(data):
    r.rpush("queue", json.dumps(data))


# Function to retrieve data from the Redis queue
def get_data_from_queue():
    data = []
    while True:
        item = r.lpop("queue")  # Retrieve and remove left-most element from the queue
        if item:
            data.append(json.loads(item.decode("utf-8")))
        else:
            break
    return data


# Initialize Dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div(
    [
        html.H1("Bitcoin data from Redis Queue", style={"textAlign": "center"}),
        dcc.Graph(id="bitcoin-price-graph"),
        dcc.Graph(id="trades-count-graph"),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
    ]
)


# Callback to update graphs with data from the queue
@app.callback(
    Output("bitcoin-price-graph", "figure"),
    Output("trades-count-graph", "figure"),
    Input("interval-component", "n_intervals"),
)
def update_graph_live(n_intervals):
    data_from_queue = get_data_from_queue()
    if data_from_queue:
        event_times = []
        n_trades = []
        close_prices = []

        for item in data_from_queue:
            close_prices.append(item["close_price"])
            n_trades.append(item["n_trades"])
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
                go.Bar(x=event_times, y=n_trades, name="Number of Trades per second")
            ],
            "layout": go.Layout(
                title="Number of Trades per second",
                xaxis=dict(title="Event Time"),
                yaxis=dict(title="Number of Trades per second"),
            ),
        }

        return close_prices_fig, trades_count_fig
    else:
        return {}, {}


# Asynchronous function to start the Redis channel subscription
async def start_subscription():
    asyncio.create_task(subscribe_to_channel())


if __name__ == "__main__":
    # Start the subscription asynchronously
    asyncio.run(start_subscription())

    # Run the Dash app
    app.run_server(debug=True)
