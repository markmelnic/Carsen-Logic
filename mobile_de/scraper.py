
from requests import get
from bs4 import BeautifulSoup

from settings import HEADERS

def search_url(makes, inp : list) -> list:
    # what each makes index is
    # 0 - make
    # 1 - model
    # 2 - minprice
    # 3 - maxprice
    # 4 - minreg
    # 5 - maxreg
    # 6 - minmileage
    # 7 - maxmileage

    url_params = ''

    if not inp[0].lower() == 'any' or not inp[0] == '':
        car_make = inp[0]
        for make in makes:
            if make['n'].lower() == inp[0].lower():
                car_make = str(make['i'])
                break
        url_params += "&makeModelVariant1.makeId=" + car_make

    # model
    if not inp[1] == '' or not inp[1] == 0 :
        url_params += "&makeModelVariant1.modelDescription=" + str(inp[1])

    # price
    if not inp[2] == '' or not inp[2] == 0:
        url_params += "&minPrice=" + str(inp[2])
    if not inp[3] == '' or not inp[3] == 0:
        url_params += "&maxPrice=" + str(inp[3])

    # registration
    if not inp[4] == '' or not inp[4] == 0:
        url_params += "&minFirstRegistrationDate=" + str(inp[4])
    if not inp[5] == '' or not inp[5] == 0:
        url_params += "&maxFirstRegistrationDate=" + str(inp[5])

    # mileage
    if not inp[6] == '' or not inp[6] == 0:
        url_params += "&minMileage=" + str(inp[6])
    if not inp[7] == '' or not inp[7] == 0:
        url_params += "&maxMileage=" + str(inp[7])

    url = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"

    # check number of pages
    response = get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    checker = soup.find(class_ = "h2 u-text-orange rbt-result-list-headline").get_text()
    checker = int(checker.split(" ")[0].replace(' ', '').replace('.', ''))

    pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
    if len(pagesnr) == 0:
        pagesnr = 1
    else:
        pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

    return url + url_params + "&pageNumber=1", pagesnr

def next_page(current_url : str, current_page : int) -> str:

    if current_page < 10:
        return current_url[:-1] + str(current_page + 1)
    elif current_page >= 10:
        return current_url[:-2] + str(current_page + 1)

def get_car_links(url : str) -> list:

    response = get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    return [link['href'] for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'})]


def get_car_data(url : str) -> list:
    print(url)

    response = get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # title
    car_title = soup.find(id = "rbt-ad-title").get_text()

    # price
    car_price = soup.find(class_ = "h3 rbt-prime-price").get_text().replace('.', '')
    if 'Brutto' in car_price:
        car_price = int(car_price[ : -11])
    else:
        car_price = int(car_price[ : -2])

    # registration
    try:
        car_reg = soup.find(id = "rbt-firstRegistration-v").get_text()
    except AttributeError:
        car_reg = soup.find(id = "rbt-category-v").get_text()
    if 'Neufahrzeug' in car_reg:
            car_reg = 2020
        #elif 'Vorführfahrzeug' in car_reg:
        #    car_reg = 4
        #    #carReg = 'Demo Car'
        #elif 'Jahreswagen' in car_reg:
        #    car_reg = 3
        #    #carReg = 'Employee Car'
        #    #Jahreswagen - employee car
    else:
        car_reg = int(car_reg[3 : ])

    # mileage
    car_mileage = soup.find(id = "rbt-mileage-v").get_text().replace('.', '')[: -4]

    # power
    #car_power = soup.find(id = "rbt-power-v").get_text().split("(")[1][ : -4]

    return car_title, car_reg, car_price, car_mileage#, car_power


def check_car_price(url : str) -> int:

    response = get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    car_price = soup.find(class_ = "h3 rbt-prime-price").get_text().replace('.', '')
    if 'Brutto' in car_price:
        return int(car_price[ : -11])
    else:
        return int(car_price[ : -2])
