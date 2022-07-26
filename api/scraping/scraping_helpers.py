from bs4 import BeautifulSoup
from requests import get


def scraping_otodom(endpoint):
    page = get(
        f"https://www.otodom.pl{endpoint}"
    ).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def scraping_house_or_flat(endpoint, for_sale):
    bs = scraping_otodom(endpoint)

    head = bs.find('head').find('title').get_text()
    id_scrap = head.split()[-3]
    link = f"https://www.otodom.pl{endpoint}"
    title = bs.find('h1', class_="css-11kn46p eu6swcv20").get_text()

    scrap = bs.find('a', class_="e1nbpvi60 css-1kforri e1enecw71").get_text().split(',')
    city = scrap[0].strip()
    try:
        district = scrap[1].strip()
    except IndexError:
        district = None
    try:
        address = scrap[-1].strip()
    except IndexError:
        address = None

    if for_sale:
        price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()
        price_per_m2 = bs.find('div', class_="css-1p44dor eu6swcv16").get_text()
        rent_price = None
    else:
        price = None
        price_per_m2 = None
        rent_price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()

    table = bs.find('div', class_="css-wj4wb2 emxfhao1")
    area = table.find(
        'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia"}
    ).get_text()[12:]
    area = None if area == 'zapytaj' else area
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
        "for_sale": for_sale,
        "link": link,
        "title": title,
        "city": city,
        "district": district,
        "address": address,
        "area": area,
        "number_of_rooms": number_of_rooms,
        "price": price,
        "price_per_m2": price_per_m2,
        "rent_price": rent_price,
    }
    return instance
