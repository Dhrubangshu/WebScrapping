import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.amazon.in'
search_term = 'bags'
num_pages = 20

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Product Name', 'Product URL', 'Product Price', 'Rating', 'Number of Reviews']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(1, num_pages+1):
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            product_name = product.find('h2').text.strip()
            product_url = base_url + product.find('a', {'class': 'a-link-normal'})['href']
            product_price = product.find('span', {'class': 'a-price-whole'}).text.replace(',', '').strip()
            rating = product.find('span', {'class': 'a-icon-alt'}).text.split()[0]
            num_reviews = product.find('span', {'class': 'a-size-base'}).text.replace(',', '').strip()

            writer.writerow({'Product Name': product_name, 'Product URL': product_url, 'Product Price': product_price, 'Rating': rating, 'Number of Reviews': num_reviews})
