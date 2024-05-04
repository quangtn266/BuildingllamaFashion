import requests, re, time, random
from bs4 import BeautifulSoup
import pandas as pd


url_original = 'https://routine.vn/thoi-trang-nam.html'  #'https://dirtycoins.vn/t-shirts-polos'

hrefs = []
data_product_skus = []
prices = []
items = []
brands = []
descriptions = []

for num in range(1, 100):
    if num == 1:
        url = url_original
    else:
        url = url_original + "?p=%d".format(num)

    response = requests.get(url_original)
    main_page_items = BeautifulSoup(response.text, 'html.parser')
    products = main_page_items.find_all('div', class_ ='product details product-item-details')

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
        item_list_names = item_list_names.removeprefix('":"').replace('","', '')
        items.append(item_list_names)

        description = i.find("a")
        descriptions.append(description.text)

        #print(i.find("a"))


basic_scrape = pd.DataFrame({
            'Link': hrefs,
            'Category_Type': items,
            'Product_ID': data_product_skus,
            'Description': descriptions,
            'Price': prices,
            'Brand': brands})

basic_scrape.to_csv('./page_number.csv', index=False, header=True)