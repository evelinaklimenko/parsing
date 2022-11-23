import requests
from bs4 import BeautifulSoup
import csv

def write_to_csv(data):
    with open('cars.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data ['title'], data['price'], data['img'], data['description']])

def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    list_page = soup.find('ul', class_='pagination').find_all("li", class_="page-item")
    # print(list_page)
    last_page = list_page[-1]
    total_pages = last_page.find('a').get('href').split('=')
    return int(total_pages[-1])

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find_all('div', class_='list-item list-label')
    for car in cars:
        try:
            title = car.find('h2', class_='name').text.strip()
        except:
            title = ''
        try: 
            price = car.find('div', class_='block price').find('strong').text
        except:
            price = ''
        try:
            img = car.find('img').get('data-src')
        except:
            img = ''
        try:
            description = ' '.join(car.find('div', class_= 'block info-wrapper item-info-wrapper').text.split())
        except:
            description = ''
        print(description)
        data = {
            'title':title,
            'price': price,
            'img': img,
            'description': description
        }

        write_to_csv(data)

def main():
    url_= 'https://www.mashina.kg/search/all/'
    html = get_html(url_)
    
    number = get_total_pages(html)
    
    i = 1
    while i <= number:
        print(i)
        url_= f'https://www.mashina.kg/search/all/{i}'
        html = get_html(url_)
        number = int(get_total_pages(html))
        if not BeautifulSoup(html, 'lxml').find('div', class_='table-view-list'):
            break

        get_data(html)
        i+=1
        print(number)
with open('cars.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['title','price', 'img', 'description'])

main()