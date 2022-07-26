from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class House(Base):
    __tablename__ = "house"
    house_id = Column(Integer, primary_key=True, index=True)
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
    house_info = relationship("HouseInfo", back_populates='house', uselist=False, cascade='delete')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HouseInfo(Base):
    __tablename__ = "house_info"
    house_info_id = Column(Integer, primary_key=True, index=True)
    market = Column(String(32))
    deposit = Column(String(32))
    plot_area = Column(String(32))
    type_of_building = Column(String(32))
    heating = Column(String(32))
    finish_condition = Column(String(32))
    year_of_construction = Column(Integer)
    parking_spot = Column(String(32))
    bills_monthly = Column(String(32))
    advertiser = Column(String(32))
    available_from = Column(Date)
    walls_material = Column(String(32))
    windows = Column(String(32))
    number_of_floors = Column(Integer)
    holiday_house = Column(Boolean)
    roof_type = Column(String(32))
    roofing_type = Column(String(32))
    attic = Column(String(32))
    utilities_supplied = Column(String(128))
    security_stuff = Column(String(128))
    fence = Column(String(32))
    drive_access = Column(String(32))
    location = Column(String(32))
    extras = Column(String(128))
    house_id_scrap = Column(Integer, ForeignKey('house.id_scrap', ondelete="CASCADE"))
    house = relationship("House", back_populates='house_info')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
