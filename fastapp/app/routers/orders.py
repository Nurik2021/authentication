from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload


from fastapp.app.flight.models import Order, OrderPassenger,Flight
from fastapp.app.schema.order import OrderCreate, OrderStatusUpdate
from fastapp.app.core.database import get_db

router = APIRouter()

@router.post("/create")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        flight_id=order_data.flight_id,
        consultant_id=order_data.consultant_id,
        status=order_data.status
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for p in order_data.passengers:
        passenger = OrderPassenger(
            order_id=order.id,
            first_name=p.first_name,
            last_name=p.last_name,
            date_of_birth=p.date_of_birth,
            gender=p.gender,
            validity_period=p.validityPeriod,
            passport=p.passport,
            phone=p.phone,
            email=p.email,
        )
        db.add(passenger)

    db.commit()
    return {"status": "ok", "order_id": order.id}


@router.get("/consultant")
def get_orders_by_consultant(consultant_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.passengers),
        joinedload(Order.flight)
    ).filter(Order.consultant_id == consultant_id).all()

    result = []
    for order in orders:
        flight_info = f"{order.flight.departure_city}-{order.flight.arrival_city}" if order.flight else f"ID: {order.flight_id}"

        result.append({
            "id": order.id,
            "flight_id": order.flight_id,
            "flight_info": flight_info,
            "status": order.status,
            "consultant_id": order.consultant_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            # Добавляем информацию о рейсе с правильной сериализацией
            "flight": {
                "departure_date": order.flight.departure_date.isoformat() if order.flight.departure_date else None,
                "departure_time": order.flight.departure_time.strftime(
                    "%H:%M:%S") if order.flight.departure_time else None,
                "arrival_date": order.flight.arrival_date.isoformat() if order.flight.arrival_date else None,
                "arrival_time": order.flight.arrival_time.strftime("%H:%M:%S") if order.flight.arrival_time else None,
            } if order.flight else None,
            "passengers": [
                {
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "passport": p.passport,
                    "phone": p.phone,
                    "email": p.email
                }
                for p in order.passengers
            ]
        })

    return result

@router.get("/passport")
def get_orders_by_passport(passport: str, db: Session = Depends(get_db)):
    orders = db.query(Order).join(OrderPassenger).filter(OrderPassenger.passport == passport).all()

    result = []
    for order in orders:
        flight = db.query(Flight).filter(Flight.id == order.flight_id).first()
        result.append({
            "id": order.id,
            "status": order.status,
            "created_at": order.created_at,
            "departure_city": flight.departure_city,
            "arrival_city": flight.arrival_city,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "duration": flight.duration,
            "price": flight.price,
            "baggage": flight.baggage,
        })

    return result


@router.patch("/{order_id}")
def update_order_status(order_id: int, order_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    order.status = order_update.status

    try:
        db.commit()
        db.refresh(order)
        return {"message": "Статус заказа успешно обновлен", "order_id": order.id, "new_status": order.status}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при обновлении заказа")