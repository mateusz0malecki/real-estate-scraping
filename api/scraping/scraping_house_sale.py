from bs4 import BeautifulSoup
from requests import get


def get_house_info_sale(endpoint):
    """
    :param endpoint: endpoint to an offer
    :return: dict filled with data for HouseSale model
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

        house_area = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia"}
        ).get_text()[12:]
        house_area = None if house_area == 'zapytaj' else house_area

        plot_area = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia działki"}
        ).get_text()[20:]
        plot_area = None if plot_area == 'zapytaj' else plot_area

        type_of_building = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Rodzaj zabudowy"}
        ).get_text()[15:]
        type_of_building = None if type_of_building == 'zapytaj' else type_of_building

        number_of_rooms = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pokoi"}
        ).get_text()[12:]
        number_of_rooms = None if number_of_rooms == 'zapytaj' else int(number_of_rooms)

        heating = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Ogrzewanie"}
        ).get_text()[10:]
        heating = None if heating == 'zapytaj' else heating

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        finish_condition = None if finish_condition == 'zapytaj' else finish_condition

        year_of_construction = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Rok budowy"}
        ).get_text()[10:]
        year_of_construction = None if year_of_construction == 'zapytaj' else int(year_of_construction)

        parking_spot = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Miejsce parkingowe"}
        ).get_text()[18:]
        parking_spot = None if parking_spot == 'zapytaj' else parking_spot

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        bills_monthly = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        house = {
            "id_scrap": int(id_scrap),
            "link": link,
            "title": title,
            "city": city,
            "district": district,
            "address": address,
            "price": price,
            "price_per_m2": price_per_m2,
            "house_area": house_area,
            "plot_area": plot_area,
            "type_of_building": type_of_building,
            "number_of_rooms": number_of_rooms,
            "heating": heating,
            "finish_condition": finish_condition,
            "year_of_construction": year_of_construction,
            "parking_spot": parking_spot,
            "bills_monthly": bills_monthly
        }
        print(house)
        return house

    except Exception as e:
        print(f"Error: {e}")


def get_house_extra_info_sale(endpoint):
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

        if extras["Dom rekreacyjny"]:
            extras["Dom rekreacyjny"] = True if extras["Dom rekreacyjny"] == 'tak' else False

        house_more_info = {
            "market": extras['Rynek'],
            "advertiser": extras['Typ ogłoszeniodawcy'],
            "available_from": extras['Dostępne od'],
            "walls_material": extras['Materiał budynku'],
            "windows": extras['Okna'],
            "number_of_floors": int(extras['Liczba pięter'].split(' ')[0]),
            "holiday_house": extras['Dom rekreacyjny'],
            "roof_type": extras['Dach'],
            "roofing_type": extras['Pokrycie dachu'],
            "attic": extras['Poddasze'],
            "utilities_supplied": extras['Media'],
            "security_stuff": extras['Zabezpieczenia'],
            "fence": extras['Ogrodzenie'],
            "drive_access": extras['Dojazd'],
            "location": extras['Okolica'],
            "extras": extras['Informacje dodatkowe']
        }
        return house_more_info

    except Exception as e:
        print(f"Error: {e}")


get_house_info_sale('/pl/oferta/4-pokojowy-dom-131m2-ogrodek-bezposrednio-ID4e9zp')
