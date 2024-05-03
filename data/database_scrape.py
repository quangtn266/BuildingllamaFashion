import requests, re, time, random
from bs4 import BeautifulSoup
import pandas as pd


url_original = 'https://routine.vn/thoi-trang-nam/quan-nam/quan-jean-nam.html'

product_list = []
    #url_page = ((url) + str(page_number))

    # Parse HTML and pull all href links
    #response = requests.get(url_page)
response = requests.get(url_original)
main_page_items = BeautifulSoup(response.text, 'html.parser')

hrefs = []
data_product_skus = []
prices = []
items = []
brands = []

products = main_page_items.find_all('div', class_ ='product details product-item-details')

#print(main_page_items)

for i in products:
    link = i.find("a", class_="product-item-link").get("href")
    brand = link.split("https://")[1].split("/")[0]
    price = i.find("span", class_="price-wrapper").get("data-price-amount")
    data_product_sku = i.find("div").get("data-product-id")

    hrefs.append(link)
    prices.append(price)
    data_product_skus.append(data_product_sku)
    brands.append(brand)

    onclicks = i.find("a").get("onclick")
    item_list_names = onclicks[onclicks.index("item_list_name") + len("item_list_name"): onclicks.index("items")]
    items.append(item_list_names)

basic_scrape = pd.DataFrame({
            'Link': hrefs,
            'Category_Type': items,
            'Product_sku': data_product_skus,
            'Price': prices,
            'Brand': brands})

#print(basic_scrape)

basic_scrape.to_csv('./page_number.csv', index=False, header=True)
