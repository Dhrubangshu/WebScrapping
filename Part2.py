import requests
from bs4 import BeautifulSoup
import csv
import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
]
# Create a list to store all the data
data = []

import requests


for i in range(1, 20):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
    user_agent = random.choice(user_agents)
    headers = {"User-Agent": user_agent}
    response = requests.get(url,)
    time.sleep(5)
    if response.status_code == 200:
   
     soup = BeautifulSoup(response.content, 'html.parser')
     products = soup.find_all('div', {'data-component-type': 's-search-result'})

     for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'})
        if product_name is not None:
            product_name = product_name.text.strip()
        product_price = product.find('span', {'class': 'a-price-whole'})
        if product_price is not None:
            product_price = product_price.text.strip()
        product_rating = product.find('span', {'class': 'a-icon-alt'})
        if product_rating is not None:
            product_rating = product_rating.text.split()[0]
        product_num_reviews = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if product_num_reviews is not None:
            product_num_reviews = product_num_reviews.text.strip()
        
        # Hit the product URL to fetch additional information
        retry_count = 0
        while retry_count < 3:
            product_response = requests.get(product_url)
            if product_response.status_code == 200:
                product_soup = BeautifulSoup(product_response.content, 'html.parser')
                break
            else:
                retry_count += 1
                time.sleep(5)
        
        # Fetch additional information if present
        description_element = product_soup.find('div', {'id': 'productDescription'})
        if description_element is not None:
            product_description = description_element.text.strip()
        else:
            product_description = ''
        asin_element = product_soup.find('div', {'id': 'detailBulletsWrapper_feature_div'})
        if asin_element is not None:
         asin_span = asin_element.find('span', {'class': 'a-text-bold'})
         if asin_span is not None:
          asin = asin_span.text.strip().split(':')[-1]
         else:
           asin = ''
        else:
         asin = ''
        manufacturer_element = product_soup.find('a', {'id': 'bylineInfo'})
        if manufacturer_element is not None:
           manufacturer = manufacturer_element.text.strip()
        else:
          manufacturer = ''
        overview_element = product_soup.find('div', {'id': 'productOverview_feature_div'})
        if overview_element is not None:
          description_element = overview_element.find('p')
          if description_element is not None:
            description = description_element.text.strip()
          else:
           description = ''
        else:
         description = ''
        
        # Add all the data to the list
        data.append([product_name, product_price, product_rating, product_num_reviews, asin, manufacturer, description, product_description, product_url])

# Export the data to a CSV file
with open('amazon_bags_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Name', 'Product Price', 'Product Rating', 'Number of Reviews', 'ASIN', 'Manufacturer', 'Description', 'Product Description', 'Product URL'])
    writer.writerows(data)
