import requests, re, time, random
from bs4 import BeautifulSoup
import pandas as pd


url_original = 'https://routine.vn/thoi-trang-nam/quan-nam/quan-jean-nam.html'
product_list = []
response = requests.get(url_original)
main_page_items = BeautifulSoup(response.text, 'html.parser')

hrefs = []
product_list = []

products = main_page_items.find_all('div', class_ ='product details product-item-details')


for i in products:
    link = i.find("a", class_="product-item-link").get("href")
    price = i.find("span", class_="price-wrapper").get("data-price-amount")
