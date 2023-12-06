import os
import websockets
import json
import redis
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

redis_host = os.environ.get("redis_host")
channel1 = os.environ.get("channel_stream1")
channel2 = os.environ.get("channel_stream2")
redis_port = os.environ.get("redis_port")

stream1 = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"  # streaming in 1s mode -> metrics : n trades per seconds, Event time
stream2 = "wss://stream.binance.com:9443/ws/btcusdt@trade"  # streaming in trade mode -> metrics : btc price , event time
"""
Data stored in time series in redis --> then connected to grafana
"""

r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


def unix_to_time(time):
    seconds = time / 1000
    normal_time = datetime.utcfromtimestamp(seconds).strftime("%Y-%m-%dT%H:%M:%S")
    return normal_time


async def publish_to_redis(stream, channel):
    async with websockets.connect(stream) as ws:
            while True:
                msg = await ws.recv()
                # Assuming the received message is JSON
                data = json.loads(msg)
                event_time = unix_to_time(data.get("E"))  # Event timestamp

                # Example data points to store in Redis
                if channel == channel1:
                    n_trades = data.get("k").get("n")  # Number of transactions
                    data = json.dumps({"event_time": event_time,"n_trades": n_trades})
                    r.set(channel2,data)
                    print("published : ",data)

                elif channel == channel2:
                    btc_price = data.get("p")  # Bitcoin price
                    data = json.dumps({"event_time": event_time,"bitcoin_price": btc_price})
                    r.set(channel2,data)
                    print("published : ",data)

async def main():
    # Run coroutines to publish to Redis channels
    await asyncio.gather(
        publish_to_redis(stream1, channel1), publish_to_redis(stream2, channel2)
    )


if __name__ == "__main__":
    asyncio.run(main())

