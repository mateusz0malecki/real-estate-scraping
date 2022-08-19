import logging
from bs4 import BeautifulSoup
from requests import get

logging.getLogger(__name__)


def otodom_get_links_to_offers(city: str, for_sale: bool, estate: str):
    """
    :param for_sale: defines if estate is listed for sale or rent
    :param estate: defines type of real estate
    :param city: city that you want to get offers from
    :return: list of links to offers from chosen city
    """
    page_number = 1
    links = []
    while True:

        sale_or_rent = None
        if for_sale is True:
            sale_or_rent = 'sprzedaz'
        if for_sale is False:
            sale_or_rent = 'wynajem'

        try:
            page = get(
                f'https://www.otodom.pl/pl/oferty/{sale_or_rent}/{estate}/{city}?market=ALL&page={page_number}'
            ).content
            bs = BeautifulSoup(page, 'html.parser')
            offers = bs.find_all('ul', class_='css-14cy79a e3x1uf06')

            if len(offers) > 2:
                scrap = offers[3].find_all("a", class_="css-b2mfz3 es62z2j16")
                page_number += 1
            else:
                break

            for endpoint in scrap:
                price = endpoint.find('span', class_='css-s8wpzb eclomwz1').get_text()
                if price != 'Zapytaj o cenę':
                    link = 'https://www.otodom.pl' + endpoint['href']
                    links.append(link)

        except Exception as e:
            logging.error(f'otodom_get_links_to_offers: {e}')
    return links
