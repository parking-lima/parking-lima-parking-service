
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.district import District
from app.schemas.district import DistrictResponse

router = APIRouter(
    prefix="/api/v1/districts",
    tags=["Districts"],
)


@router.get("", response_model=list[DistrictResponse])
def get_districts(db: Session = Depends(get_db)):
    statement = select(District).order_by(District.id)

    return db.scalars(statement).all()
