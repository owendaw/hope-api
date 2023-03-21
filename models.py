from datetime import datetime
from pydantic import BaseModel


class Refill(BaseModel):
    piSerial: str
    startTime: datetime
    endTime: datetime
    quantity: int

    # class Config:
    #     json_encoders = {
    #         datetime: lambda v: v.timestamp()
    #     }


class RefillOut(BaseModel):
    startTime: datetime
    endTime: datetime
    quantity: int


# class FlowOut(BaseModel):
#     stationId: int
#     quantity: int
