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

    title = bs.find('h1', class_='css-r9zjja-Text eu5v0x0').get_text()

    area = None
    number_of_rooms = None
    flat_floor = None
    extras = None
    type_of_building = None
    bills_monthly = None
    market = None
    number_of_floors = None
    price_per_m2 = None

    table = bs.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    for element in table:
        detail = element.get_text()
        if detail.startswith('Powierzchnia'):
            area = detail.split(': ')[1]
            area = int(area.split(' ')[0].split('.')[0].split(',')[0])
        if detail.startswith('Liczba pokoi'):
            if detail.split(' ')[2] == "Kawalerka":
                number_of_rooms = 1
            else:
                number_of_rooms = int(detail.split(' ')[2])
        if detail.startswith('Poziom'):
            flat_floor = detail.split(' ')[1]
        if detail.startswith('Umeblowane'):
            extras = 'Umeblowane' if detail.split(' ')[1] == 'Tak' else None
        if detail.startswith('Rodzaj zabudowy'):
            type_of_building = ''.join([i for i in detail.split(': ')[1]])
        if detail.startswith('Czynsz'):
            bills_monthly = int(detail.split(' ')[2])
        if detail.startswith('Rynek'):
            market = detail.split(' ')[1]
        if detail.startswith('Liczba pięter'):
            if detail.split(' ')[2] == 'Parterowy':
                number_of_floors = 1
            elif detail.split(' ')[2] == 'Jednopiętrowy':
                number_of_floors = 2
            else:
                number_of_floors = 3
        if detail.startswith('Cena za'):
            price_per_m2 = detail.split(' ')[3]
            price_per_m2 = int(price_per_m2.split('.')[0].split(',')[0])

    if for_sale:
        rent_price = None
        price = bs.find('h3', class_='css-okktvh-Text eu5v0x0').get_text()
        price = ''.join([i for i in price if i.isdigit()])
    else:
        price = None
        rent_price = bs.find('h3', class_='css-okktvh-Text eu5v0x0').get_text()
        rent_price = ''.join([i for i in rent_price if i.isdigit()])

    img = bs.find_all('img', alt=title)
    images = []
    for i in img:
        try:
            images.append(i['src'])
        except KeyError:
            try:
                images.append(i['data-src'].split(' ')[0])
            except KeyError:
                pass

    picture1 = images[0] if len(images) > 1 else None
    picture2 = images[1] if len(images) > 2 else None
    picture3 = images[2] if len(images) > 3 else None
    picture4 = images[3] if len(images) > 4 else None
    picture5 = images[4] if len(images) > 5 else None
    picture6 = images[5] if len(images) > 6 else None
    picture7 = images[6] if len(images) > 7 else None
    picture8 = images[7] if len(images) > 8 else None

    instance = {
        "id_scrap": int(id_scrap),
        "title": title,
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
        "picture1": picture1,
        "picture2": picture2,
        "picture3": picture3,
        "picture4": picture4,
        "picture5": picture5,
        "picture6": picture6,
        "picture7": picture7,
        "picture8": picture8
    }
    return instance
