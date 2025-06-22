from pydantic import BaseModel
from typing import List

class PassengerSchema(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    validityPeriod: str
    passport: str
    phone: str
    email: str


class OrderCreate(BaseModel):
    flight_id: int
    consultant_id: int
    status: str = "В ожидании"
    passengers: List[PassengerSchema]

class OrderStatusUpdate(BaseModel):
    status: str

