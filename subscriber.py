import os
import asyncio
import redis
from dotenv import load_dotenv

load_dotenv()
# Retrieving environment variables
redis_host = os.environ.get("redis_host")
channel = os.environ.get("channel")
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


if __name__ == "__main__":
    asyncio.run(subscribe_to_channel(channel))