from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class HouseSale(Base):
    __tablename__ = "house_sale"
    house_id = Column(Integer, primary_key=True, index=True)
    id_scrap = Column(Integer, unique=True)
    link = Column(String(256))
    title = Column(String(128))
    city = Column(String(32))
    district = Column(String(32))
    address = Column(String(32))
    price = Column(String(32))
    price_per_m2 = Column(String(32))
    house_area = Column(String(32))
    plot_area = Column(String(32))
    type_of_building = Column(String(32))
    number_of_rooms = Column(Integer)
    heating = Column(String(32))
    finish_condition = Column(String(32))
    year_of_construction = Column(Integer)
    parking_spot = Column(String(32))
    bills_monthly = Column(String(32))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    house_more_info = relationship("HouseMoreInfoSale", back_populates='house', uselist=False, cascade='delete')


class HouseMoreInfoSale(Base):
    __tablename__ = "house_more_info_sale"
    house_info_id = Column(Integer, primary_key=True, index=True)
    market = Column(String(32))
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
    house_id = Column(Integer, ForeignKey('house_sale.house_id', ondelete="CASCADE"))
    house = relationship("HouseSale", back_populates='house_more_info')


class HouseRent(Base):
    __tablename__ = "house_rent"
    house_id = Column(Integer, primary_key=True, index=True)
    id_scrap = Column(Integer, unique=True)
    link = Column(String(256))
    title = Column(String(128))
    city = Column(String(32))
    district = Column(String(32))
    address = Column(String(32))
    rent_price = Column(String(32))
    house_area = Column(String(32))
    number_of_rooms = Column(Integer)
    type_of_building = Column(String(32))
    number_of_floors = Column(Integer)
    bills_monthly = Column(String(32))
    deposit = Column(String(32))
    parking_spot = Column(String(32))
    available_from = Column(Date)
    finish_condition = Column(String(32))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    house_more_info = relationship("HouseMoreInfoRent", back_populates='house', uselist=False, cascade='delete')


class HouseMoreInfoRent(Base):
    __tablename__ = "house_more_info_rent"
    house_info_id = Column(Integer, primary_key=True, index=True)
    advertiser = Column(String(32))
    heating = Column(String(32))
    year_of_construction = Column(Integer)
    utilities_supplied = Column(String(128))
    plot_area = Column(String(32))
    windows = Column(String(32))
    holiday_house = Column(Boolean)
    security_stuff = Column(String(128))
    fence = Column(String(32))
    drive_access = Column(String(32))
    location = Column(String(32))
    walls_material = Column(String(32))
    roof_type = Column(String(32))
    roofing_type = Column(String(32))
    attic = Column(String(32))
    extras = Column(String(128))
    house_id = Column(Integer, ForeignKey('house_rent.house_id', ondelete="CASCADE"))
    house = relationship("HouseRent", back_populates='house_more_info')
