
from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Identity,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    __table_args__ = (
        UniqueConstraint(
            "parking_id",
            "code",
            name="uq_parking_spaces_parking_code",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    parking_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parkings.id"),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
