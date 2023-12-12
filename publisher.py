import websockets
import json
import asyncio
from datetime import datetime
from utils import *

r, channel = redis_connect()

stream = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"  # streaming in 1s mode -> metrics : n trades per seconds, Event time, btc close price


def unix_to_time(time):
    seconds = time / 1000
    normal_time = datetime.utcfromtimestamp(seconds).strftime("%Y-%m-%dT%H:%M:%S")
    return normal_time


async def publish_to_redis(stream, channel):
    async with websockets.connect(stream) as ws:
        while True:
            msg = await ws.recv()

            data = json.loads(msg)
            event_time = unix_to_time(data.get("E"))

            n_trades = data.get("k").get("n")
            close_price = data.get("k").get("c")
            data = json.dumps(
                {
                    "event_time": event_time,
                    "n_trades": n_trades,
                    "close_price": close_price,
                }
            )
            r.publish(channel, data)
            print("published : ", data)


if __name__ == "__main__":
    asyncio.run(publish_to_redis(stream, channel))
