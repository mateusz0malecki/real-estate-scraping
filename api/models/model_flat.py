from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class FlatSale(Base):
    __tablename__ = "flat_sale"
    flat_id = Column(Integer, primary_key=True, index=True)
    id_scrap = Column(Integer, unique=True)
    link = Column(String(256))
    title = Column(String(128))
    city = Column(String(32))
    district = Column(String(32))
    address = Column(String(32))
    price = Column(String(32))
    price_per_m2 = Column(String(32))
    flat_area = Column(String(32))
    number_of_rooms = Column(Integer)
    flat_floor = Column(String(16))
    bills_monthly = Column(String(16))
    property_form = Column(String(32))
    finish_condition = Column(String(32))
    balcony_garden = Column(String(32))
    parking_spot = Column(String(32))
    heating = Column(String(32))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    flat_more_info = relationship("FlatMoreInfoSale", back_populates='flat', uselist=False, cascade='delete')


class FlatMoreInfoSale(Base):
    __tablename__ = "flat_more_info_sale"
    flat_info_id = Column(Integer, primary_key=True, index=True)
    market = Column(String(32))
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
    extras = Column(String(128))
    house_id = Column(Integer, ForeignKey('flat_sale.flat_id', ondelete="CASCADE"))
    house = relationship("FlatSale", back_populates='flat_more_info')


class FlatRent(Base):
    __tablename__ = "flat_rent"
    flat_id = Column(Integer, primary_key=True, index=True)
    id_scrap = Column(Integer, unique=True)
    link = Column(String(256))
    title = Column(String(128))
    city = Column(String(32))
    district = Column(String(32))
    address = Column(String(32))
    rent_price = Column(String(32))
    number_of_rooms = Column(Integer)
    flat_floor = Column(String(16))
    available_from = Column(Date)
    bills_monthly = Column(String(32))
    deposit = Column(String(32))
    type_of_building = Column(String(32))
    balcony_garden = Column(String(32))
    finish_condition = Column(String(32))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    flat_more_info = relationship("FlatMoreInfoRent", back_populates='flat', uselist=False, cascade='delete')


class FlatMoreInfoRent(Base):
    __tablename__ = "flat_more_info_rent"
    flat_info_id = Column(Integer, primary_key=True, index=True)
    advertiser = Column(String(32))
    available_for_students = Column(Boolean)
    equipment = Column(String(128))
    utilities_supplied = Column(String(128))
    heating = Column(String(32))
    security_stuff = Column(String(128))
    windows = Column(String(32))
    elevator = Column(Boolean)
    parking_spot = Column(String(32))
    year_of_construction = Column(Integer)
    walls_material = Column(String(32))
    extras = Column(String(128))
    house_id = Column(Integer, ForeignKey('flat_rent.flat_id', ondelete="CASCADE"))
    house = relationship("FlatRent", back_populates='flat_more_info')
