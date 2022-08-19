from models.model_house import House, HouseInfo
from models.model_flat import Flat, FlatInfo
from scraping.otodom_scraping_house import otodom_scraping_house, otodom_scraping_house_info
from scraping.otodom_scraping_flat import otodom_scraping_flat, otodom_scraping_flat_info


def scrap_houses_info_otodom(db):
    instances_to_fill = House.get_empty_houses(db).filter(House.link.contains('www.otodom.pl'))

    for instance in instances_to_fill:
        house = otodom_scraping_house(link=instance.link, for_sale=instance.for_sale)
        house_info = None
        if house:
            house_info = otodom_scraping_house_info(link=instance.link, for_sale=instance.for_sale)

            instance.id_scrap = house.get("id_scrap")
            instance.title = house.get("title")
            instance.city = house.get("city")
            instance.district = house.get("district")
            instance.address = house.get("address")
            instance.area = house.get("area")
            instance.number_of_rooms = house.get("number_of_rooms")
            instance.price = house.get("price")
            instance.price_per_m2 = house.get("price_per_m2")
            instance.rent_price = house.get("rent_price")
            instance.picture1 = house.get("picture1")

        if house_info:
            house_info_to_db = HouseInfo(
                market=house_info.get("market"),
                deposit=house_info.get("deposit"),
                plot_area=house_info.get("plot_area"),
                type_of_building=house_info.get("type_of_building"),
                heating=house_info.get("heating"),
                finish_condition=house_info.get("finish_condition"),
                year_of_construction=house_info.get("year_of_construction"),
                parking_spot=house_info.get("parking_spot"),
                bills_monthly=house_info.get("bills_monthly"),
                advertiser=house_info.get("advertiser"),
                available_from=house_info.get("available_from"),
                walls_material=house_info.get("walls_material"),
                windows=house_info.get("windows"),
                number_of_floors=house_info.get("number_of_floors"),
                holiday_house=house_info.get("holiday_house"),
                roof_type=house_info.get("roof_type"),
                roofing_type=house_info.get("roofing_type"),
                attic=house_info.get("attic"),
                utilities_supplied=house_info.get("utilities_supplied"),
                security_stuff=house_info.get("security_stuff"),
                fence=house_info.get("fence"),
                drive_access=house_info.get("drive_access"),
                location=house_info.get("location"),
                extras=house_info.get("extras"),
                house_id_scrap=instance.id_scrap
            )
            db.add(house_info_to_db)
            db.commit()
            db.refresh(house_info_to_db)


def scrap_flats_info_otodom(db):
    instances_to_fill = Flat.get_empty_flats(db).filter(Flat.link.contains('www.otodom.pl'))

    for instance in instances_to_fill:
        flat = otodom_scraping_flat(link=instance.link, for_sale=instance.for_sale)
        flat_info = None
        if flat:
            flat_info = otodom_scraping_flat_info(link=instance.link, for_sale=instance.for_sale)

            instance.id_scrap = flat.get("id_scrap")
            instance.title = flat.get("title")
            instance.district = flat.get("district")
            instance.address = flat.get("address")
            instance.area = flat.get("area")
            instance.number_of_rooms = flat.get("number_of_rooms")
            instance.price = flat.get("price")
            instance.price_per_m2 = flat.get("price_per_m2")
            instance.rent_price = flat.get("rent_price")
            instance.picture1 = flat.get("picture1")

        if flat_info:
            flat_info_to_db = FlatInfo(
                flat_floor=flat_info.get("flat_floor"),
                bills_monthly=flat_info.get("bills_monthly"),
                finish_condition=flat_info.get("finish_condition"),
                balcony_garden=flat_info.get("balcony_garden"),
                parking_spot=flat_info.get("parking_spot"),
                heating=flat_info.get("heating"),
                advertiser=flat_info.get("advertiser"),
                available_from=flat_info.get("available_from"),
                year_of_construction=flat_info.get("year_of_construction"),
                type_of_building=flat_info.get("type_of_building"),
                windows=flat_info.get("windows"),
                walls_material=flat_info.get("walls_material"),
                elevator=flat_info.get("elevator"),
                utilities_supplied=flat_info.get("utilities_supplied"),
                security_stuff=flat_info.get("security_stuff"),
                equipment=flat_info.get("equipment"),
                property_form=flat_info.get("property_form"),
                market=flat_info.get("market"),
                deposit=flat_info.get("deposit"),
                available_for_students=flat_info.get("available_for_students"),
                extras=flat_info.get("extras"),
                flat_id_scrap=instance.id_scrap
            )
            db.add(flat_info_to_db)
            db.commit()
            db.refresh(flat_info_to_db)
