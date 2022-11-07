import requests
from bs4 import BeautifulSoup
from re import findall
from time import sleep


def find_cheap_forza():
    url = "https://gg.deals/pack/forza-horizon-5-premium-edition"

    payload = ""
    headers = {}

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        titles = soup.find_all('div', class_='game-info-title-wrapper')
        prices = soup.find_all('a', class_='price')
        shops = soup.find_all('img', class_='shop-image-white')
        hrefs = soup.find_all('div', class_='game-cta')

        offers = []

        for title, price, shop, href in zip(titles, prices, shops, hrefs):
            offers.append({
                'name': title.text.strip(),
                'price': float(findall('[0-9]+,[0-9]+', price.text.strip())[0].replace(',', '.')),
                'shop': shop['alt'],
                'href': f"https://gg.deals{title.find('a')['href']}"
            })

        sorted_offers = sorted(offers, key=lambda d: d['price'])

        if sorted_offers[0]['price'] < 300:
            return f'''fh5 premium w dobrej cenie:
{sorted_offers[0]["name"]}
{sorted_offers[0]["price"]}
{sorted_offers[0]["shop"]}
{sorted_offers[0]["href"]}'''
        else:
            sleep(60)
            pass

    else:
        return f'error: {response.status_code}'


while True:
    print(find_cheap_forza())
