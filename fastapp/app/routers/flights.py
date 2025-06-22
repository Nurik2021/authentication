# routers/flights.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from fastapp.app.flight.models import Flight
from fastapp.app.core.database import get_db
from typing import List
from sqlalchemy import func


router = APIRouter()

@router.get("/search")
def search_flights(
    from_city: str = Query(..., alias="from_city"),
    to_city: str = Query(..., alias="to_city"),
    date: str = Query(...),  # YYYY-MM-DD
    db: Session = Depends(get_db)
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    flights = db.query(Flight).filter(
        Flight.departure_city == from_city,
        Flight.arrival_city == to_city,
        func.date(Flight.departure_date) == target_date

    ).all()

    return {"flights" :flights}
