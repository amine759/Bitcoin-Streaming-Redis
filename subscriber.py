import os
import asyncio
import redis
from dotenv import load_dotenv

load_dotenv()
# Retrieving environment variables
redis_host = os.environ.get("redis_host")
channel1 = os.environ.get("channel_stream1")
channel2 = os.environ.get("channel_stream2")
redis_port = os.environ.get("redis_port")

# Redis connection setup
r = redis.StrictRedis(host=redis_host, port=redis_port)

async def subscribe_to_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    
    for message in pubsub.listen():
        # Process received message
        if message['type'] == 'message':
            print(f"Received message from {channel}: {message['data'].decode('utf-8')}")

async def main():
    # Run coroutines to subscribe to Redis channels
    await asyncio.gather(
        subscribe_to_channel(channel1),
        subscribe_to_channel(channel2)
    )

if __name__ == "__main__":
    asyncio.run(main())