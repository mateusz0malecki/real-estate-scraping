from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

from .schemas_helpers import lower_camel, EstatePagination


class EstateBase(BaseModel):
    id_scrap: int
    for_sale: bool
    link: str
    title: str
    city: str
    district: Optional[str]
    address: Optional[str]
    area: Optional[int]
    number_of_rooms: Optional[int]
    picture1: Optional[str]
    picture2: Optional[str]
    picture3: Optional[str]
    picture4: Optional[str]
    picture5: Optional[str]
    picture6: Optional[str]
    picture7: Optional[str]
    picture8: Optional[str]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        alias_generator = lower_camel
        allow_population_by_field_name = True


class EstateSale(EstateBase):
    price: int
    price_per_m2: int


class EstateRent(EstateBase):
    rent_price: int


class EstateSalePagination(EstatePagination):
    records: List[EstateSale] = []


class EstateRentPagination(EstatePagination):
    records: List[EstateRent] = []


class HouseInfo(BaseModel):
    market: Optional[str]
    deposit: Optional[str]
    plot_area: Optional[str]
    type_of_building: Optional[str]
    heating: Optional[str]
    finish_condition: Optional[str]
    year_of_construction: Optional[int]
    parking_spot: Optional[str]
    bills_monthly: Optional[str]
    advertiser: Optional[str]
    available_from: Optional[date]
    walls_material: Optional[str]
    windows: Optional[str]
    number_of_floors: Optional[int]
    holiday_house: Optional[bool]
    roof_type: Optional[str]
    roofing_type: Optional[str]
    attic: Optional[str]
    utilities_supplied: Optional[str]
    security_stuff: Optional[str]
    fence: Optional[str]
    drive_access: Optional[str]
    location: Optional[str]
    extras: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = lower_camel
        allow_population_by_field_name = True


class FlatInfo(BaseModel):
    flat_floor: Optional[str]
    bills_monthly: Optional[str]
    finish_condition: Optional[str]
    balcony_garden: Optional[str]
    parking_spot: Optional[str]
    heating: Optional[str]
    advertiser: Optional[str]
    available_from: Optional[date]
    year_of_construction: Optional[int]
    type_of_building: Optional[str]
    windows: Optional[str]
    walls_material: Optional[str]
    elevator: Optional[bool]
    utilities_supplied: Optional[str]
    security_stuff: Optional[str]
    equipment: Optional[str]
    property_form: Optional[str]
    market: Optional[str]
    deposit: Optional[str]
    available_for_students: Optional[bool]
    extras: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = lower_camel
        allow_population_by_field_name = True


class HouseWithDetails(EstateBase):
    price: Optional[int]
    price_per_m2: Optional[int]
    rent_price: Optional[int]
    house_info: Optional[HouseInfo]


class FlatWithDetails(EstateBase):
    price: Optional[int]
    price_per_m2: Optional[int]
    rent_price: Optional[int]
    flat_info: Optional[FlatInfo]

