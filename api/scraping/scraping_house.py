from .scraping_helpers import scraping_otodom, scraping_house_or_flat


def scraping_house(link: str, for_sale: bool):
    """
    :param link: endpoint to an offer
    :param for_sale: defines if house is listed for sale or rent
    :return: dict filled with data for House model
    """
    try:
        house = scraping_house_or_flat(link, for_sale)
        return house
    except Exception as e:
        print(f"Error: {e} - {link}")


def scraping_house_info(link: str, for_sale: bool):
    """
    :param link: endpoint to an offer
    :param for_sale: defines if house is listed for sale or rent
    :return: dict filled with data for HouseInfo model
    """
    try:
        bs = scraping_otodom(link)
        table = bs.find('div', class_="css-wj4wb2 emxfhao1")

        extras = {}
        scrap = bs.find_all('div', class_='css-f45csg estckra9')
        for info in scrap:
            key = info.find('div', class_='css-1h52dri estckra7').get_text()
            try:
                value = info.find('div', class_='css-1wi2w6s estckra5').get_text()
            except AttributeError:
                value = None
            extras[key] = value

        if extras.get("Dom rekreacyjny"):
            extras["Dom rekreacyjny"] = True if extras["Dom rekreacyjny"] == 'tak' else False
        if extras.get("Liczba pięter"):
            extras["Liczba pięter"] = 0 if extras.get("Liczba pięter").lower() == 'parterowy' \
                else int(extras.get('Liczba pięter').split(' ')[0])
        if extras.get("Rok budowy"):
            extras['Rok budowy'] = int(extras.get("Rok budowy"))

        type_of_building = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Rodzaj zabudowy"}
        ).get_text()[15:]
        extras['Rodzaj zabudowy'] = None if type_of_building == 'zapytaj' else type_of_building

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        extras['Stan wykończenia'] = None if finish_condition == 'zapytaj' else finish_condition

        parking_spot = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Miejsce parkingowe"}
        ).get_text()[18:]
        extras['Miejsce parkingowe'] = None if parking_spot == 'zapytaj' else parking_spot

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        extras['Czynsz'] = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        if for_sale:
            plot_area = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Powierzchnia działki"}
            ).get_text()[20:]
            extras['Powierzchnia działki'] = None if plot_area == 'zapytaj' else plot_area

            heating = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Ogrzewanie"}
            ).get_text()[10:]
            extras['Ogrzewanie'] = None if heating == 'zapytaj' else heating

            year_of_construction = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Rok budowy"}
            ).get_text()[10:]
            extras['Rok budowy'] = None if year_of_construction == 'zapytaj' else int(year_of_construction)

        if not for_sale:
            number_of_floors = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Liczba pięter"}
            ).get_text()[13:]
            if number_of_floors == 'parterowy':
                extras['Liczba pięter'] = 0
            else:
                extras['Liczba pięter'] = None if number_of_floors == 'zapytaj' else int(number_of_floors.split(' ')[0])

            deposit = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Kaucja"}
            ).get_text()[6:]
            extras['Kaucja'] = None if deposit == 'zapytaj' else deposit

            available_from = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Dostępne od"}
            ).get_text()[11:]
            extras['Dostępne od'] = None if available_from == 'zapytaj' else available_from

        house_info = {
            "market": extras.get('Rynek'),
            "deposit": extras.get('Kaucja'),
            "plot_area": extras.get('Powierzchnia działki'),
            "type_of_building": extras.get('Rodzaj zabudowy'),
            "heating": extras.get('Ogrzewanie'),
            "finish_condition": extras.get('Stan wykończenia'),
            "year_of_construction": extras.get('Rok budowy'),
            "parking_spot": extras.get('Miejsce parkingowe'),
            "bills_monthly": extras.get('Czynsz'),
            "advertiser": extras.get('Typ ogłoszeniodawcy'),
            "available_from": extras.get('Dostępne od'),
            "walls_material": extras.get('Materiał budynku'),
            "windows": extras.get('Okna'),
            "number_of_floors": extras.get('Liczba pięter'),
            "holiday_house": extras.get('Dom rekreacyjny'),
            "roof_type": extras.get('Dach'),
            "roofing_type": extras.get('Pokrycie dachu'),
            "attic": extras.get('Poddasze'),
            "utilities_supplied": extras.get('Media'),
            "security_stuff": extras.get('Zabezpieczenia'),
            "fence": extras.get('Ogrodzenie'),
            "drive_access": extras.get('Dojazd'),
            "location": extras.get('Okolica'),
            "extras": extras.get('Informacje dodatkowe')
        }
        return house_info
    except Exception as e:
        print(f"Error: {e} - {link}")
