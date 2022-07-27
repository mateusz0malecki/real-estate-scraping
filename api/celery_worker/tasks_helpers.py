from models.model_house import House, HouseInfo
from models.model_flat import Flat, FlatInfo
from scraping.scraping_offers_links import get_links_to_offers
from scraping.scraping_house import scraping_house, scraping_house_info
from scraping.scraping_flat import scraping_flat, scraping_flat_info


def scrap_links(db, estate: str, for_sale: bool, city: str):
    endpoints = get_links_to_offers(city=city, for_sale=for_sale, estate=estate)

    if estate == 'dom':
        houses_to_init = []
        for endpoint in endpoints:
            if not House.get_house_by_link(db, f"https://www.otodom.pl{endpoint}"):
                house = House(
                    for_sale=for_sale,
                    link=f"https://www.otodom.pl{endpoint}",
                    city=city
                )
                houses_to_init.append(house)
            else:
                break
        db.add_all(houses_to_init)
        db.commit()
        for instance in houses_to_init:
            db.refresh(instance)

    if estate == 'mieszkanie':
        flats_to_init = []
        for endpoint in endpoints:
            if not Flat.get_flat_by_link(db, f"https://www.otodom.pl{endpoint}"):
                flat = Flat(
                    for_sale=for_sale,
                    link=f"https://www.otodom.pl{endpoint}",
                    city=city
                )
                flats_to_init.append(flat)
            else:
                break
        db.add_all(flats_to_init)
        db.commit()
        for instance in flats_to_init:
            db.refresh(instance)


def scrap_houses_info(db):
    instances_to_fill = House.get_empty_houses(db)

    for instance in instances_to_fill:
        house = scraping_house(link=instance.link, for_sale=instance.for_sale)
        houses_info_to_add = []
        house_info = None
        if house:
            house_info = scraping_house_info(link=instance.link, for_sale=instance.for_sale)

            instance.id_scrap = house.get("id_scrap")
            instance.title = house.get("title")
            instance.district = house.get("district")
            instance.address = house.get("address")
            instance.area = house.get("area")
            instance.number_of_rooms = house.get("number_of_rooms")
            instance.price = house.get("price")
            instance.price_per_m2 = house.get("price_per_m2")
            instance.rent_price = house.get("rent_price")

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
            houses_info_to_add.append(house_info_to_db)

        db.add_all(houses_info_to_add)
        db.commit()
        for n in houses_info_to_add:
            db.refresh(n)


def scrap_flats_info(db):
    instances_to_fill = Flat.get_empty_flats(db)

    for instance in instances_to_fill:
        flat = scraping_flat(link=instance.link, for_sale=instance.for_sale)
        flats_info_to_add = []
        flat_info = None
        if flat:
            flat_info = scraping_flat_info(link=instance.link, for_sale=instance.for_sale)

            instance.id_scrap = flat.get("id_scrap")
            instance.title = flat.get("title")
            instance.district = flat.get("district")
            instance.address = flat.get("address")
            instance.area = flat.get("area")
            instance.number_of_rooms = flat.get("number_of_rooms")
            instance.price = flat.get("price")
            instance.price_per_m2 = flat.get("price_per_m2")
            instance.rent_price = flat.get("rent_price")

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
            flats_info_to_add.append(flat_info_to_db)

        db.add_all(flats_info_to_add)
        db.commit()
        for n in flats_info_to_add:
            db.refresh(n)
