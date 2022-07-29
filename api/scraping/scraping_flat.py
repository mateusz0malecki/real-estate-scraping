import logging
from .scraping_helpers import scraping_otodom, scraping_house_or_flat

logging.getLogger(__name__)


def scraping_flat(link: str, for_sale: bool):
    """
    :param link: endpoint to an offer
    :param for_sale: defines if flat is listed for sale or rent
    :return: dict filled with data for Flat model
    """
    try:
        flat = scraping_house_or_flat(link, for_sale)
        return flat
    except Exception as e:
        logging.error(f"scraping_flat: {e} - {link}")


def scraping_flat_info(link: str, for_sale: bool):
    """
    :param link: endpoint to an offer
    :param for_sale: defines if flat is listed for sale or rent
    :return: dict filled with data for FlatInfo model
    """
    try:
        bs = scraping_otodom(link)
        table = bs.find('div', class_="css-wj4wb2 emxfhao1")

        extras = {}
        scrap = bs.find_all('div', class_='css-f45csg estckra9')
        for info in scrap:
            if info is not None:
                key = info.find('div', class_='css-1h52dri estckra7').get_text()
                try:
                    value = info.find('div', class_='css-1wi2w6s estckra5').get_text()
                except AttributeError:
                    value = None
                extras[key] = value

        if extras.get("Winda"):
            extras["Winda"] = True if extras["Winda"] == 'tak' else False
        if extras.get("Wynajmę również studentom"):
            extras["Wynajmę również studentom"] = True if extras["Wynajmę również studentom"] == 'tak' else False
        if extras.get("Rok budowy"):
            extras['Rok budowy'] = int(extras.get("Rok budowy"))

        flat_floor = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Piętro"}
        ).get_text()[6:]
        extras['Piętro'] = None if flat_floor == 'zapytaj' else flat_floor

        bills_monthly = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Czynsz"}
        ).get_text()[6:]
        extras['Czynsz'] = None if bills_monthly == 'zapytaj' else bills_monthly.split('/')[0]

        finish_condition = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Stan wykończenia"}
        ).get_text()[16:]
        extras['Stan wykończenia'] = None if finish_condition == 'zapytaj' else finish_condition

        balcony_garden = table.find(
            'div', {"class": "css-1ccovha estckra9", "aria-label": "Balkon / ogród / taras"}
        ).get_text()[22:]
        extras['Balkon / ogród / taras'] = None if balcony_garden == 'zapytaj' else balcony_garden

        if for_sale:
            property_form = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Forma własności"}
            ).get_text()[15:]
            extras['Forma własności'] = None if property_form == 'zapytaj' else property_form

            parking_spot = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Miejsce parkingowe"}
            ).get_text()[18:]
            extras['Miejsce parkingowe'] = None if parking_spot == 'zapytaj' else parking_spot

            heating = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Ogrzewanie"}
            ).get_text()[10:]
            extras['Ogrzewanie'] = None if heating == 'zapytaj' else heating

        if not for_sale:
            available_from = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Dostępne od"}
            ).get_text()[11:]
            extras['Dostępne od'] = None if available_from == 'zapytaj' else available_from

            deposit = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Kaucja"}
            ).get_text()[6:]
            extras['Kaucja'] = None if deposit == 'zapytaj' else deposit

            type_of_building = table.find(
                'div', {"class": "css-1ccovha estckra9", "aria-label": "Rodzaj zabudowy"}
            ).get_text()[15:]
            extras['Rodzaj zabudowy'] = None if type_of_building == 'zapytaj' else type_of_building

        flat_info = {
            "flat_floor": extras.get('Piętro'),
            "bills_monthly": extras.get('Czynsz'),
            "finish_condition": extras.get('Stan wykończenia'),
            "balcony_garden": extras.get('Balkon / ogród / taras'),
            "parking_spot": extras.get("Miejsce parkingowe"),
            "heating": extras.get('Ogrzewanie'),
            "advertiser": extras.get('Typ ogłoszeniodawcy'),
            "available_from": extras.get('Dostępne od'),
            "year_of_construction": extras.get('Rok budowy'),
            "type_of_building": extras.get('Rodzaj zabudowy'),
            "windows": extras.get('Okna'),
            "walls_material": extras.get('Materiał budynku'),
            "elevator": extras.get("Winda"),
            "utilities_supplied": extras.get('Media'),
            "security_stuff": extras.get('Zabezpieczenia'),
            "equipment": extras.get('Wyposażenie'),
            "property_form": extras.get('Forma własności'),
            "market": extras.get('Rynek'),
            "deposit": extras.get('Kaucja'),
            "available_for_students": extras.get("Wynajmę również studentom"),
            "extras": extras.get('Informacje dodatkowe')
        }
        return flat_info
    except Exception as e:
        logging.error(f"scraping_flat_info: {e} - {link}")
