from bs4 import BeautifulSoup
from requests import get


def scraping_olx(endpoint):
    page = get(endpoint).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def olx_scraping_house_or_flat(link, for_sale):
    bs = scraping_olx(link)

    id_scrap = bs.find('span', class_='css-9xy3gn-Text eu5v0x0').get_text()
    id_scrap = ''.join([i for i in id_scrap if i.isdigit()])
    print(id_scrap)

    title = bs.find('h1', class_='css-r9zjja-Text eu5v0x0').get_text()
    print(title)

    city = bs.find('p', class_='css-7xdcwc-Text eu5v0x0').get_text().split(",")[0]
    print(city)

    district = bs.find('span', class_="css-1c0ed4l").get_text()
    print(district)

    area = None
    number_of_rooms = None
    flat_floor = None
    extras = None
    type_of_building = None
    bills_monthly = None
    market = None
    number_of_floors = None

    table = bs.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    for element in table:
        detail = element.get_text()
        if detail.startswith('Powierzchnia'):
            area = int(detail.split(' ')[1])
        if detail.startswith('Liczba pokoi'):
            number_of_rooms = int(detail.split(' ')[2])
        if detail.startswith('Poziom'):
            flat_floor = detail.split(' ')[1]
        if detail.startswith('Umeblowane'):
            extras = 'Umeblowane' if detail.split(' ')[1] == 'Tak' else None
        if detail.startswith('Rodzaj zabudowy'):
            type_of_building = detail.split(' ')[2]
        if detail.startswith('Czynsz'):
            bills_monthly = int(detail.split(' ')[2])
        if detail.startswith('Rynek'):
            market = detail.split(' ')[1]
        if detail.startswith('Liczba pięter'):
            number_of_floors = detail.split(' ')[2]

    instance = {
        "id_scrap": int(id_scrap),
        "title": title,
        "city": city,
        "district": district,
        "area": area,
        "number_of_rooms": number_of_rooms,
        "flat_floor": flat_floor,
        "extras": extras,
        "type_of_building": type_of_building,
        "bills_monthly": bills_monthly,
        "market": market,
        "number_of_floors": number_of_floors,
        "price": price,
        "price_per_m2": price_per_m2,
        "rent_price": rent_price,
        "picture": picture
    }
    return instance
