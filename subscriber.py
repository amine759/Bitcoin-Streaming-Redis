import os
import asyncio
import redis
from dotenv import load_dotenv
import json


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
            message_data = message["data"].decode("utf-8")
            process_queue(message_data)
            data_from_queue = get_data_from_queue()
            
            if data_from_queue:
                print("Retrieved data from the queue:", data_from_queue)
            else:
                print("Queue is empty")

def process_queue(data):
    r.rpush('queue', json.dumps(data))

def get_data_from_queue():
    # Retrieve and remove the left-most element from the queue
    data = r.lpop('queue')
    if data:
        return json.loads(data.decode('utf-8'))  # Decode JSON data
    else:
        return None  # Queue is empty
    
if __name__ == "__main__":
    asyncio.run(subscribe_to_channel(channel))

    