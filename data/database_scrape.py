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
imagebacks = []
imagefronts = []

for num in range(1, 2):
    if num == 1:
        url = url_original
    else:
        url = url_original + "?p=%d".format(num)

    response = requests.get(url_original)
    main_page_items = BeautifulSoup(response.text, 'html.parser')
    products = main_page_items.find_all('div',class_="product-item-info")

    for i in products:
        image_back = i.find('span', class_ = "product-image-container").find("img", class_="product-image-photo").get("data-catalog_image_hovering")
        image_front = i.find('span', class_ = "product-image-container").find("img", class_="product-image-photo").get("src")
        description = i.find("span", class_ = "product-image-container").find("img", class_="product-image-photo").get("alt")
        if "nam" in description.lower():
            items.append("male")
        elif "nữ" in description.lower():
            items.append("female")
        link = i.find("a", class_="product-item-link").get("href")
        brand = link.split("https://")[1].split("/")[0]
        price = i.find("span", class_="price-wrapper").get("data-price-amount")
        data_product_sku = i.find('div', class_ ='price-box price-final_price').get("data-price-box")

        hrefs.append(link)
        prices.append(price)
        data_product_skus.append(data_product_sku)
        brands.append(brand)
        descriptions.append(description)
        imagebacks.append(image_back)
        imagefronts.append(image_front)




basic_scrape = pd.DataFrame({
            'Link': hrefs,
            'Category_Type': items,
            'Image Front': imagefronts,
            'Image Back': imagebacks,
            'Product_ID': data_product_skus,
            'Description': descriptions,
            'Price': prices,
            'Brand': brands})

basic_scrape.to_csv('./page_number.csv', index=False, header=True)