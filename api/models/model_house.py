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
    house_info = relationship("HouseInfo", back_populates='house', uselist=False, cascade='delete')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def get_house_by_link(db, link):
        return db.query(House).filter(House.link == link).first()

    @staticmethod
    def get_house_by_scrap_id(db, id_scrap):
        return db.query(House).filter(House.id_scrap == id_scrap).first()

    @staticmethod
    def get_empty_houses(db):
        return db.query(House).filter(House.title == None)

    @staticmethod
    def get_all_houses(db):
        return db.query(House).all()


class HouseInfo(Base):
    __tablename__ = "house_info"
    house_info_id = Column(Integer, primary_key=True, index=True)
    market = Column(String(32))
    deposit = Column(String(32))
    plot_area = Column(String(32))
    type_of_building = Column(String(64))
    heating = Column(String(64))
    finish_condition = Column(String(64))
    year_of_construction = Column(Integer)
    parking_spot = Column(String(64))
    bills_monthly = Column(String(32))
    advertiser = Column(String(32))
    available_from = Column(Date)
    walls_material = Column(String(64))
    windows = Column(String(64))
    number_of_floors = Column(Integer)
    holiday_house = Column(Boolean)
    roof_type = Column(String(64))
    roofing_type = Column(String(64))
    attic = Column(String(64))
    utilities_supplied = Column(String(256))
    security_stuff = Column(String(256))
    fence = Column(String(128))
    drive_access = Column(String(128))
    location = Column(String(128))
    extras = Column(String(256))
    house_id_scrap = Column(Integer, ForeignKey('house.id_scrap', ondelete="CASCADE"))
    house = relationship("House", back_populates='house_info')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
