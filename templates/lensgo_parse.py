from time import sleep
from playwright.sync_api import sync_playwright
from product_info import ProductInfo
from general_functions import price_in_numbers


class MorelinzParse:
    def __init__(self, query: str):
        self.query = query
        self.product = ProductInfo()

    def __get_product_info(self, product_card):
        name = product_card.query_selector('.name').inner_text()
        if product_card.query_selector('.price-old-action') is None:
            price = product_card.query_selector('.price-normal').inner_text()
            discount_price = price
        else:
            price = product_card.query_selector('.price-old-action').inner_text()
            discount_price = product_card.query_selector('.price-normal').inner_text()

        url = product_card.query_selector('.product-img.has-second-image').get_attribute('href')
        shop = 'lensgo.ru'
        img = product_card.query_selector('img').get_attribute('src')

        self.product = ProductInfo(name, price_in_numbers(price), price_in_numbers(discount_price), shop, url, img)

    def parse(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/109.0.0.0 Safari/537.36 '
            })
            self.page = self.context.new_page()
            self.page.goto(f"https://lensgo.ru/search?search={self.query}")

            objects = self.page.query_selector_all('.product-layout.has-countdown.has-extra-button')
            for obj in objects:
                self.__get_product_info(obj)
