from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaProducer
import json

app = FastAPI()


KAFKA_BROKER = "kafka:9093"
KAFKA_TOPIC = "events"

producer = AIOKafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
)


async def start_producer():
    await producer.start()


async def stop_producer():
    await producer.stop()


async def send_message(data):
    try:
        message_value = json.dumps(data).encode('utf-8')
        await producer.send_and_wait(KAFKA_TOPIC, value=message_value)
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")
