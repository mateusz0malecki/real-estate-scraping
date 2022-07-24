from bs4 import BeautifulSoup
from requests import get


def get_flat_info_sale(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for FlatSale model
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

        price = bs.find('strong', class_="css-8qi9av eu6swcv19").get_text()
        price_per_m2 = bs.find('div', class_="css-1p44dor eu6swcv16").get_text()

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

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        bills_monthly = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        property_form = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Forma własności"}
        ).get_text()[15:]
        property_form = None if property_form == 'zapytaj' else property_form

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        finish_condition = None if finish_condition == 'zapytaj' else finish_condition

        balcony_garden = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Balkon / ogród / taras"}
        ).get_text()[22:]
        balcony_garden = None if balcony_garden == 'zapytaj' else balcony_garden

        parking_spot = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Miejsce parkingowe"}
        ).get_text()[18:]
        parking_spot = None if parking_spot == 'zapytaj' else parking_spot

        heating = table.find('div', {"class": "css-1ccovha estckra9", "aria-label": "Ogrzewanie"}).get_text()[10:]
        heating = None if heating == 'zapytaj' else heating

        flat = {
            "id_scrap": int(id_scrap),
            "link": link,
            "title": title,
            "city": city,
            "district": district,
            "address": address,
            "price": price,
            "price_per_m2": price_per_m2,
            "flat_area": flat_area,
            "number_of_rooms": number_of_rooms,
            "flat_floor": flat_floor,
            "bills_monthly": bills_monthly,
            "property_form": property_form,
            "finish_condition": finish_condition,
            "balcony_garden": balcony_garden,
            "parking_spot": parking_spot,
            "heating": heating
        }
        return flat

    except Exception as e:
        print(f"Error: {e}")


def get_flat_extra_info_sale(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for HouseMoreInfoSale model
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

        flat_more_info = {
            "market": extras['Rynek'],
            "advertiser": extras['Typ ogłoszeniodawcy'],
            "available_from": extras['Dostępne od'],
            "year_of_construction": extras['Rok budowy'],
            "type_of_building": extras['Rodzaj zabudowy'],
            "windows": extras['Okna'],
            "walls_material": extras['Materiał budynku'],
            "elevator": extras["Winda"],
            "utilities_supplied": extras['Media'],
            "security_stuff": extras['Zabezpieczenia'],
            "equipment": extras['Wyposażenie'],
            "extras": extras['Informacje dodatkowe']
        }
        return flat_more_info

    except Exception as e:
        print(f"Error: {e}")
