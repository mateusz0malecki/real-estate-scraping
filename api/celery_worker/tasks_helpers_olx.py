from models.model_house import House, HouseInfo
from models.model_flat import Flat, FlatInfo
from scraping.olx_scraping_helpers import olx_scraping_house_or_flat


def scrap_houses_info_olx(db):
    instances_to_fill = House.get_empty_houses(db).filter(House.link.contains('www.olx.pl'))

    for instance in instances_to_fill:
        house = olx_scraping_house_or_flat(link=instance.link, for_sale=instance.for_sale)

        if house:
            if not House.get_house_by_scrap_id(db, house.get("id_scrap")):
                instance.id_scrap = house.get("id_scrap")
                instance.title = house.get("title")
                instance.area = house.get("area")
                instance.number_of_rooms = house.get("number_of_rooms")
                instance.price = house.get("price")
                instance.price_per_m2 = house.get("price_per_m2")
                instance.rent_price = house.get("rent_price")
                instance.picture1 = house.get("picture1")
                instance.picture2 = house.get("picture2")
                instance.picture3 = house.get("picture3")
                instance.picture4 = house.get("picture4")
                instance.picture5 = house.get("picture5")
                instance.picture6 = house.get("picture6")
                instance.picture7 = house.get("picture7")
                instance.picture8 = house.get("picture8")

                house_info_to_db = HouseInfo(
                    market=house.get("market"),
                    extras=house.get("extras"),
                    type_of_building=house.get("type_of_building"),
                    bills_monthly=house.get("bills_monthly"),
                    number_of_floors=house.get("number_of_floors")
                )
                db.add(house_info_to_db)
                db.commit()
                db.refresh(house_info_to_db)
            else:
                db.delete(instance)
                db.commit()


def scrap_flats_info_olx(db):
    instances_to_fill = Flat.get_empty_flats(db).filter(Flat.link.contains('www.olx.pl'))

    for instance in instances_to_fill:
        flat = olx_scraping_house_or_flat(link=instance.link, for_sale=instance.for_sale)

        if flat:
            if not Flat.get_flat_by_scrap_id(db, flat.get("id_scrap")):
                instance.id_scrap = flat.get("id_scrap")
                instance.title = flat.get("title")
                instance.area = flat.get("area")
                instance.number_of_rooms = flat.get("number_of_rooms")
                instance.price = flat.get("price")
                instance.price_per_m2 = flat.get("price_per_m2")
                instance.rent_price = flat.get("rent_price")
                instance.picture1 = flat.get("picture1")
                instance.picture2 = flat.get("picture2")
                instance.picture3 = flat.get("picture3")
                instance.picture4 = flat.get("picture4")
                instance.picture5 = flat.get("picture5")
                instance.picture6 = flat.get("picture6")
                instance.picture7 = flat.get("picture7")
                instance.picture8 = flat.get("picture8")

                flat_info_to_db = FlatInfo(
                    market=flat.get("market"),
                    extras=flat.get("extras"),
                    type_of_building=flat.get("type_of_building"),
                    bills_monthly=flat.get("bills_monthly"),
                    flat_floor=flat.get("flat_floor")
                )
                db.add(flat_info_to_db)
                db.commit()
                db.refresh(flat_info_to_db)
            else:
                db.delete(instance)
                db.commit()
