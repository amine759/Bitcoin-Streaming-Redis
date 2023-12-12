import asyncio
import json
from utils import *

r, channel = redis_connect()


async def subscribe_to_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        # Process received message
        if message["type"] == "message":
            message_data = message["data"].decode("utf-8")
            enqueue(message_data)
            # data_from_queue = get_data_from_queue()


def enqueue(data):
    r.rpush("queue", json.dumps(data))
    print("data pushed in queue: ", data)


if __name__ == "__main__":
    asyncio.run(subscribe_to_channel(channel))
