from datetime import datetime, timedelta
import redis
import os
from dotenv import load_dotenv


def redis_connect():
    load_dotenv()
    # Retrieving environment variables
    redis_host = os.environ.get("redis_host")
    channel = os.environ.get("channel")
    redis_port = os.environ.get("redis_port")

    # Redis connection setup
    return redis.StrictRedis(host=redis_host, port=redis_port), channel

def generate_default_graphs():
    # Generating default values
    now = datetime.now()
    two_seconds_ago = now - timedelta(seconds=2)

    default_event_times = [
        (two_seconds_ago + timedelta(milliseconds=i * 500)).isoformat()
        for i in range(10)
    ]

    default_n_trades_fig = {
        "data": [
            {
                "x": default_event_times,
                "y": list(),
                "type": "lines",
                "mode": "lines+markers",
                "name": "Number of Trades per second",
            }
        ],
        "layout": {
            "title": "Default Number of Trades per second",
            "xaxis": {"title": "Event Time"},
            "yaxis": {"title": "Number of Trades per second"},
            "width": 800,  # Specify the width
            "height": 500,  # Specify the height
        },
    }

    default_close_price_fig = {
        "data": [
            {
                "x": default_event_times,
                "y": list(),
                "type": "lines",
                "mode": "lines+markers",
                "name": "Bitcoin close Prices per second",
            }
        ],
        "layout": {
            "title": "Default Close Prices per second",
            "xaxis": {"title": "Event Time"},
            "yaxis": {"title": "Close Price"},
            "width": 800,  # Specify the width
            "height": 500,  # Specify the height
        },
    }

    return default_n_trades_fig, default_close_price_fig
