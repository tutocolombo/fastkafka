from datetime import datetime
import uuid

from pydantic import BaseModel, StrictStr, validator


class Trade(BaseModel):
    """
    Schema representing a single trade, as it comes from the coincap websocket
    """

    exchange: StrictStr
    message_id: StrictStr = ""
    base: StrictStr
    quote: StrictStr
    direction: StrictStr
    price: float
    volume: float
    timestamp: datetime
    priceUsd: float

    @validator("message_id", pre=True, always=True)
    def set_id_from_name_uuid(cls, v, values):
        if "exchange" in values:
            return f"{values['exchange']}_{uuid.uuid4()}"
        else:
            raise ValueError("exchange not set")

    class Config:
        """
        Extra configuration
        """

        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class ProducerResponse(BaseModel):
    """
    Schema of the response given by the producer api
    """

    message_id: StrictStr
    topic: StrictStr
    timestamp: StrictStr = ""

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())
