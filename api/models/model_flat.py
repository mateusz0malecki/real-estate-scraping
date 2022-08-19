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
    address = Column(String(64))
    area = Column(Integer)
    number_of_rooms = Column(Integer)
    price = Column(Integer)
    price_per_m2 = Column(Integer)
    rent_price = Column(Integer)
    picture1 = Column(String(256))
    picture2 = Column(String(256))
    picture3 = Column(String(256))
    picture4 = Column(String(256))
    picture5 = Column(String(256))
    picture6 = Column(String(256))
    picture7 = Column(String(256))
    picture8 = Column(String(256))
    flat_info = relationship("FlatInfo", back_populates='flat', uselist=False, cascade='delete')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def get_flat_by_link(db, link):
        return db.query(Flat).filter(Flat.link == link).first()

    @staticmethod
    def get_flat_by_scrap_id(db, id_scrap):
        return db.query(Flat).filter(Flat.id_scrap == id_scrap).first()

    @staticmethod
    def get_empty_flats(db):
        return db.query(Flat).filter(Flat.title == None)

    @staticmethod
    def get_all_flats(db):
        return db.query(Flat).all()


class FlatInfo(Base):
    __tablename__ = "flat_info"
    flat_info_id = Column(Integer, primary_key=True, index=True)
    flat_floor = Column(String(16))
    bills_monthly = Column(String(16))
    finish_condition = Column(String(64))
    balcony_garden = Column(String(64))
    parking_spot = Column(String(64))
    heating = Column(String(64))
    advertiser = Column(String(32))
    available_from = Column(Date)
    year_of_construction = Column(Integer)
    type_of_building = Column(String(64))
    windows = Column(String(64))
    walls_material = Column(String(64))
    elevator = Column(Boolean)
    utilities_supplied = Column(String(256))
    security_stuff = Column(String(256))
    equipment = Column(String(256))
    property_form = Column(String(64))
    market = Column(String(32))
    deposit = Column(String(32))
    available_for_students = Column(Boolean)
    extras = Column(String(256))
    flat_id_scrap = Column(Integer, ForeignKey('flat.id_scrap', ondelete="CASCADE"))
    flat = relationship("Flat", back_populates='flat_info')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
