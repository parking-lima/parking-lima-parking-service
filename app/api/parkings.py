
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.parking import Parking
from app.models.parking_space import ParkingSpace
from app.schemas.parking import (
    ParkingResponse,
    ParkingSpaceResponse,
)

router = APIRouter(
    prefix="/api/v1/parkings",
    tags=["Parkings"],
)


@router.get("", response_model=list[ParkingResponse])
def get_parkings(
    district_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    statement = select(Parking)

    if district_id is not None:
        statement = statement.where(
            Parking.district_id == district_id
        )

    statement = statement.order_by(Parking.id)

    return db.scalars(statement).all()


@router.get("/{parking_id}", response_model=ParkingResponse)
def get_parking(
    parking_id: int,
    db: Session = Depends(get_db),
):
    parking = db.get(Parking, parking_id)

    if parking is None:
        raise HTTPException(
            status_code=404,
            detail="Parking not found",
        )

    return parking


@router.get(
    "/{parking_id}/spaces",
    response_model=list[ParkingSpaceResponse],
)
def get_parking_spaces(
    parking_id: int,
    db: Session = Depends(get_db),
):
    parking = db.get(Parking, parking_id)

    if parking is None:
        raise HTTPException(
            status_code=404,
            detail="Parking not found",
        )

    statement = (
        select(ParkingSpace)
        .where(ParkingSpace.parking_id == parking_id)
        .order_by(ParkingSpace.id)
    )

    return db.scalars(statement).all()
