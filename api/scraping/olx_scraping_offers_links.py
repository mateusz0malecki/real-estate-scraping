import logging
from bs4 import BeautifulSoup
from requests import get

logging.getLogger(__name__)


def olx_get_links_to_offers(city: str, for_sale: bool, estate: str):
    """
    :param for_sale: defines if estate is listed for sale or rent
    :param estate: defines type of real estate
    :param city: city that you want to get offers from
    :return: list of links to offers from chosen city
    """
    page_number = 1
    links = []
    if city == 'zielona-gora':
        city = 'zielonagora'
    if city == 'gorzow-wielkopolski':
        city = 'gorzow'

    sale_or_rent = None
    if for_sale is True:
        sale_or_rent = 'sprzedaz'
    if for_sale is False:
        sale_or_rent = 'wynajem'

    estate = "mieszkania" if estate == "mieszkanie" else "domy"

    while True:
        try:
            page = get(
                f'https://www.olx.pl/d/nieruchomosci/{estate}/{sale_or_rent}/{city}/?page={page_number}',
                allow_redirects=False
            ).content
            bs = BeautifulSoup(page, 'html.parser')
            offers = bs.find_all('div', class_='css-14fnihb')

            scrap = offers[0].find_all("a", class_="css-1bbgabe")
            page_number += 1

            for endpoint in scrap:
                if not endpoint['href'].startswith('http'):
                    link = 'https://www.olx.pl' + endpoint['href']
                    links.append(link)

            if bs.find('div', class_='css-wsrviy'):
                break

        except Exception as e:
            logging.error(f'olx_get_links_to_offers: {e}')
    return links
