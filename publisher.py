import os
import websockets
import json
import redis
import asyncio
from datetime import datetime

redis_host = os.environ.get("redis_host")
channel1 = os.environ.get("channel_stream1")
channel2 = os.environ.get("channel_stream2")
redis_port = os.environ.get("redis_port")

stream1 = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"  # streaming in 1s mode -> metrics : n trades per seconds, Event time
stream2 = "wss://stream.binance.com:9443/ws/btcusdt@trade"  # streaming in trade mode -> metrics : btc price , event time

"""
Data stored in time series in redis --> then connected to grafana
"""

# r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


def unix_to_time(time):
    seconds = time / 1000
    normal_time = datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%dT%H:%M:%S')
    return normal_time


async def publish_channel1(stream):
    # Process received WebSocket messages here

    """Process and store data in Redis time series
    Example: Storing data in Redis with a timestamp as key"""
    async with websockets.connect(stream) as ws:
        # Stay alive forever, listening to incoming msgs
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            event_time = unix_to_time(data.get("E"))  # E: Event timestamp
            n_trades = data.get("k").get("n")  # E: number of transactions
            # r.set(event_time, n_trades)
            # r.set(event_time, btc_price)  # Store the message using the timestamp as key in Redis
            print(event_time, n_trades)


async def publish_channel2(stream):
    async with websockets.connect(stream) as ws:
        # Stay alive forever, listening to incoming msgs
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            event_time = unix_to_time(data.get("E"))  # E: Event timestamp
            # r.set(event_time, n_trades)
            btc_price = data.get("p")  # p: bitcoin price in the timestamp
            # r.set(event_time, btc_price)  # Store the message using the timestamp as key in Redis
            print(event_time, btc_price)


async def main():
    await asyncio.gather(publish_channel1(stream1), publish_channel2(stream2))


if __name__ == "__main__":
    asyncio.run(main())
