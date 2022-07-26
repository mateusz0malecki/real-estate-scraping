from models.model_house import House
from scraping.scraping_offers_links import get_links_to_offers


def scrap_links(db, estate: str, for_sale: bool, city: str):
    endpoints = get_links_to_offers(city=city, for_sale=for_sale, estate=estate)

    houses_to_init = []
    for endpoint in endpoints:
        house = House(
            for_sale=for_sale,
            link=endpoint
        )
        houses_to_init.append(house)

    db.add_all(houses_to_init)
    db.commit()
    for instance in houses_to_init:
        db.refresh(instance)
    return {"message": "Done."}
