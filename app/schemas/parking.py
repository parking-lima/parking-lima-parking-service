
from pydantic import BaseModel, ConfigDict


class ParkingResponse(BaseModel):
    id: int
    district_id: int
    name: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class ParkingSpaceResponse(BaseModel):
    id: int
    parking_id: int
    code: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
