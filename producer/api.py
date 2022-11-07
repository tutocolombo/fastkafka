import asyncio

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from producer.core.schemas.schema import ProducerResponse, Trade

app = FastAPI()


loop = asyncio.get_event_loop()
aio_producer = AIOKafkaProducer(loop=loop, bootstrap_servers="localhost:9093")


@app.on_event("startup")
async def startup_event():
    await aio_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aio_producer.stop()


@app.post("/producer", status_code=200, response_model=ProducerResponse)
async def kafka_produce(msg: Trade):
    """

    :param msg: Json containing trade information
    :return: ProducerResponse
    """
    topic = msg.exchange
    await aio_producer.send(topic, msg.json().encode("ascii"))
    response = ProducerResponse(message_id=msg.message_id, topic=topic)
    return response


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
