import os
import websockets
import json
import redis
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

redis_host = os.environ.get("redis_host")
channel = os.environ.get("channel")
redis_port = os.environ.get("redis_port")

stream = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"  # streaming in 1s mode -> metrics : n trades per seconds, Event time, btc close price


r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


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
                data = json.dumps({"event_time": event_time,"n_trades": n_trades,'close_price': close_price})
                r.publish(channel,data)
                print("published : ",data)

if __name__ == "__main__":
    asyncio.run(publish_to_redis(stream, channel))