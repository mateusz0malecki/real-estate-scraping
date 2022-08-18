from bs4 import BeautifulSoup
from requests import get


def scraping_otodom(endpoint):
    page = get(endpoint).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def otodom_scraping_house_or_flat(link, for_sale):
    bs = scraping_otodom(link)

    head = bs.find('head').find('title').get_text().split(',')
    id_scrap = ''.join([i for i in head[-1] if i.isdigit()])
    title = bs.find('h1', class_="css-11kn46p eu6swcv20").get_text()

    scrap = bs.find('a', class_="e1nbpvi60 css-1kforri e1enecw71").get_text().split(',')
    city = scrap[0].strip()
    try:
        district = scrap[1].strip()
    except IndexError:
        district = None
    try:
        address = scrap[-1].strip() if len(scrap) > 2 else None
    except IndexError:
        address = None

    if for_sale:
        price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()
        price = ''.join(n for n in price if n.isdigit())
        price_per_m2 = bs.find('div', class_="css-1p44dor eu6swcv16").get_text()
        price_per_m2 = ''.join(n for n in price_per_m2 if n.isdigit())
        price_per_m2 = ''.join([i for i in price_per_m2 if ord(i) < 128])
        rent_price = None
    else:
        price = None
        price_per_m2 = None
        rent_price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()
        rent_price = ''.join(n for n in rent_price if n.isdigit())

    picture = bs.find('img', alt=title)['src']

    table = bs.find('div', class_="css-wj4wb2 emxfhao1")
    area = table.find(
        'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia"}
    ).get_text()[12:]
    area = None if area == 'zapytaj' else int(area.split()[0].split(',')[0])
    number_of_rooms = table.find(
        'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pokoi"}
    ).get_text()[12:]
    if len(number_of_rooms.split()) > 1:
        numeric_filter = filter(str.isdigit, number_of_rooms)
        number_of_rooms = int("".join(numeric_filter))
    else:
        number_of_rooms = None if number_of_rooms == 'zapytaj' else int(number_of_rooms)

    instance = {
        "id_scrap": int(id_scrap),
        "title": title,
        "city": city,
        "district": district,
        "address": address,
        "area": area,
        "number_of_rooms": number_of_rooms,
        "price": price,
        "price_per_m2": price_per_m2,
        "rent_price": rent_price,
        "picture": picture
    }
    return instance
