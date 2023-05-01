from datetime import datetime
from pydantic import BaseModel


class Refill(BaseModel):
    piSerial: str
    startTime: datetime
    endTime: datetime
    quantity: int


class RefillOut(BaseModel):
    startTime: datetime
    endTime: datetime
    quantity: int
