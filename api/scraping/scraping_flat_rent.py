from bs4 import BeautifulSoup
from requests import get


def get_flat_info_rent(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for FlatRent model
    """
    try:
        page = get(
            f"https://www.otodom.pl{endpoint}"
        ).content
        bs = BeautifulSoup(page, 'html.parser')

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
            address = scrap[2].strip()
        except IndexError:
            address = None

        rent_price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()

        table = bs.find('div', class_="css-wj4wb2 emxfhao1")

        flat_area = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia"}
        ).get_text()[12:]
        flat_area = None if flat_area == 'zapytaj' else flat_area

        number_of_rooms = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pokoi"}
        ).get_text()[12:]
        number_of_rooms = None if number_of_rooms == 'zapytaj' else int(number_of_rooms)

        flat_floor = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Piętro"}
        ).get_text()[6:]
        flat_floor = None if flat_floor == 'zapytaj' else flat_floor

        available_from = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Dostępne od"}
        ).get_text()[11:]
        available_from = None if available_from == 'zapytaj' else available_from

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        bills_monthly = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        deposit = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Kaucja"}
        ).get_text()[6:]
        deposit = None if deposit == 'zapytaj' else deposit

        type_of_building = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Rodzaj zabudowy"}
        ).get_text()[15:]
        type_of_building = None if type_of_building == 'zapytaj' else type_of_building

        balcony_garden = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Balkon / ogród / taras"}
        ).get_text()[22:]
        balcony_garden = None if balcony_garden == 'zapytaj' else balcony_garden

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        finish_condition = None if finish_condition == 'zapytaj' else finish_condition

        flat = {
            "id_scrap": int(id_scrap),
            "link": link,
            "title": title,
            "city": city,
            "district": district,
            "address": address,
            "rent_price": rent_price,
            "flat_area": flat_area,
            "number_of_rooms": number_of_rooms,
            "flat_floor": flat_floor,
            "available_from": available_from,
            "bills_monthly": bills_monthly,
            "deposit": deposit,
            "type_of_building": type_of_building,
            "balcony_garden": balcony_garden,
            "finish_condition": finish_condition
        }
        return flat

    except Exception as e:
        print(f"Error: {e}")


def get_flat_extra_info_rent(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for HouseMoreInfoRent model
    """
    try:
        page = get(
            f"https://www.otodom.pl{endpoint}"
        ).content
        bs = BeautifulSoup(page, 'html.parser')

        extras = {}
        scrap = bs.find_all('div', class_='css-f45csg estckra9')
        for info in scrap:
            key = info.find('div', class_='css-1h52dri estckra7').get_text()
            try:
                value = info.find('div', class_='css-1wi2w6s estckra5').get_text()
            except AttributeError:
                value = None
            extras[key] = value

        if extras["Winda"]:
            extras["Winda"] = True if extras["Winda"] == 'tak' else False
        if extras["Wynajmę również studentom"]:
            extras["Wynajmę również studentom"] = True if extras["Wynajmę również studentom"] == 'tak' else False

        flat_more_info = {
            "advertiser": extras['Typ ogłoszeniodawcy'],
            "available_for_students": extras["Wynajmę również studentom"],
            "equipment": extras['Wyposażenie'],
            "utilities_supplied": extras['Media'],
            "security_stuff": extras['Zabezpieczenia'],
            "windows": extras['Okna'],
            "elevator": extras["Winda"],
            "parking_spot": extras["Miejsce parkingowe"],
            "year_of_construction": int(extras['Rok budowy']),
            "walls_material": extras['Materiał budynku'],
            "extras": extras['Informacje dodatkowe']
        }
        return flat_more_info

    except Exception as e:
        print(f"Error: {e}")
