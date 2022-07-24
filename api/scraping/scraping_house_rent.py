from bs4 import BeautifulSoup
from requests import get


def get_house_info_rent(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for HouseRent model
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

        house_area = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia"}
        ).get_text()[12:]
        house_area = None if house_area == 'zapytaj' else house_area

        number_of_rooms = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pokoi"}
        ).get_text()[12:]
        number_of_rooms = None if number_of_rooms == 'zapytaj' else int(number_of_rooms)

        type_of_building = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Rodzaj zabudowy"}
        ).get_text()[15:]
        type_of_building = None if type_of_building == 'zapytaj' else type_of_building

        number_of_floors = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pięter"}
        ).get_text()[13:]
        number_of_floors = None if number_of_floors == 'zapytaj' else int(number_of_floors.split(' ')[0])

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        bills_monthly = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        deposit = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Kaucja"}
        ).get_text()[6:]
        deposit = None if deposit == 'zapytaj' else deposit

        parking_spot = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Miejsce parkingowe"}
        ).get_text()[18:]
        parking_spot = None if parking_spot == 'zapytaj' else parking_spot

        available_from = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Dostępne od"}
        ).get_text()[11:]
        available_from = None if available_from == 'zapytaj' else available_from

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        finish_condition = None if finish_condition == 'zapytaj' else finish_condition

        house = {
            "id_scrap": int(id_scrap),
            "link": link,
            "title": title,
            "city": city,
            "district": district,
            "address": address,
            "rent_price": rent_price,
            "house_area": house_area,
            "number_of_rooms": number_of_rooms,
            "type_of_building": type_of_building,
            "number_of_floors": number_of_floors,
            "bills_monthly": bills_monthly,
            "deposit": deposit,
            "parking_spot": parking_spot,
            "available_from": available_from,
            "finish_condition": finish_condition
        }
        return house

    except Exception as e:
        print(f"Error: {e}")


def get_house_extra_info_rent(endpoint):
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

        if extras["Dom rekreacyjny"]:
            extras["Dom rekreacyjny"] = True if extras["Dom rekreacyjny"] == 'tak' else False

        house_more_info = {
            "advertiser": extras['Typ ogłoszeniodawcy'],
            "heating": extras['Ogrzewanie'],
            "year_of_construction": int(extras['Rok budowy']),
            "utilities_supplied": extras['Media'],
            "plot_area": extras['Powierzchnia działki'],
            "windows": extras['Okna'],
            "holiday_house": extras['Dom rekreacyjny'],
            "security_stuff": extras['Zabezpieczenia'],
            "fence": extras['Ogrodzenie'],
            "drive_access": extras['Dojazd'],
            "location": extras['Okolica'],
            "walls_material": extras['Materiał budynku'],
            "roof_type": extras['Dach'],
            "roofing_type": extras['Pokrycie dachu'],
            "attic": extras['Poddasze'],
            "extras": extras['Informacje dodatkowe']
        }
        return house_more_info

    except Exception as e:
        print(f"Error: {e}")
