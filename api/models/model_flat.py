from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Flat(Base):
    __tablename__ = "flat"
    flat_id = Column(Integer, primary_key=True, index=True)
    id_scrap = Column(Integer, unique=True)
    for_sale = Column(Boolean)
    link = Column(String(256))
    title = Column(String(128))
    city = Column(String(32))
    district = Column(String(32))
    address = Column(String(32))
    area = Column(String(32))
    number_of_rooms = Column(Integer)
    price = Column(String(32))
    price_per_m2 = Column(String(32))
    rent_price = Column(String(32))
    flat_more_info = relationship("FlatInfo", back_populates='flat', uselist=False, cascade='delete')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FlatInfo(Base):
    __tablename__ = "flat_info"
    flat_info_id = Column(Integer, primary_key=True, index=True)
    flat_floor = Column(String(16))
    bills_monthly = Column(String(16))
    finish_condition = Column(String(32))
    balcony_garden = Column(String(32))
    parking_spot = Column(String(32))
    heating = Column(String(32))
    advertiser = Column(String(32))
    available_from = Column(Date)
    year_of_construction = Column(Integer)
    type_of_building = Column(String(32))
    windows = Column(String(32))
    walls_material = Column(String(32))
    elevator = Column(Boolean)
    utilities_supplied = Column(String(128))
    security_stuff = Column(String(128))
    equipment = Column(String(128))
    property_form = Column(String(32))
    market = Column(String(32))
    deposit = Column(String(32))
    available_for_students = Column(Boolean)
    extras = Column(String(128))
    house_id = Column(Integer, ForeignKey('flat.flat_id', ondelete="CASCADE"))
    house = relationship("Flat", back_populates='flat_info')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
