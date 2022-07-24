from bs4 import BeautifulSoup
from requests import get


def get_links_to_offers(city, sale_or_rent, estate):
    """
    :param sale_or_rent: defines if estate is listed for sale or rent
    :param estate: defines type of real estate
    :param city: city that you want to get offers from
    :return: list of links to offers from chosen city
    """
    page_number = 1
    links = []
    while True:
        try:
            page = get(
                f'https://www.otodom.pl/pl/oferty/{sale_or_rent}/{estate}/{city}'
                f'?distanceRadius=0&page={page_number}&limit=36'
            ).content
            bs = BeautifulSoup(page, 'html.parser')
            offers = bs.find_all('ul', class_='css-14cy79a e3x1uf06')

            if len(offers) > 1:
                scrap = offers[1].find_all("a", class_="css-rvjxyq es62z2j14")
                page_number += 1
            else:
                break

            for link in scrap:
                price = link.find('span', class_='css-rmqm02 eclomwz0').get_text()
                if price != 'Zapytaj o cenę':
                    links.append(link['href'])

        except Exception as e:
            print(f'Error: {e}')
    return links
