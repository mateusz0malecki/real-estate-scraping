from models.model_house import House
from models.model_flat import Flat
from scraping.otodom_scraping_offers_links import otodom_get_links_to_offers
from scraping.olx_scraping_offers_links import olx_get_links_to_offers


def scrap_links(db, estate: str, for_sale: bool, city: str):
    links = otodom_get_links_to_offers(city=city, for_sale=for_sale, estate=estate) + \
            olx_get_links_to_offers(city=city, for_sale=for_sale, estate=estate)

    cities_to_change = {
        'gdansk': "Gdańsk",
        'bialystok': "Białystok",
        'torun': "Toruń",
        'rzeszow': "Rzeszów",
        'krakow': "Kraków",
        'wroclaw': "Wrocław",
        'lodz': "Łódź",
        'poznan': "Poznań",
        'zielona-gora': "Zielona Góra",
        'gorzow-wielkopolski': "Gorzów Wielkopolski",
    }
    for n in cities_to_change.items():
        if city == n[0]:
            city = n[1]

    if estate == 'dom':
        houses_to_init = []
        for link in links:
            if not House.get_house_by_link(db, link):
                house = House(
                    for_sale=for_sale,
                    link=link,
                    city=city.title()
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
        for link in links:
            if not Flat.get_flat_by_link(db, link):
                flat = Flat(
                    for_sale=for_sale,
                    link=link,
                    city=city.title()
                )
                flats_to_init.append(flat)
            else:
                break
        db.add_all(flats_to_init)
        db.commit()
        for instance in flats_to_init:
            db.refresh(instance)
