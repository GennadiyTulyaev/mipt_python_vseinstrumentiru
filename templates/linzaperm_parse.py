from time import sleep
from playwright.sync_api import sync_playwright
from product_info import ProductInfo
from general_functions import price_in_numbers


class LinzapermParse:
    def __init__(self, query: str):
        self.query = query
        self.product = ProductInfo()

    def __get_product_info(self, product_card):
        name = product_card.query_selector('.dark_link').inner_text()
        price = product_card.query_selector('.price_value').inner_text()
        discount_price = price

        url = 'https://linzaperm.ru' + product_card.query_selector('a').get_attribute('href')
        shop = 'linzaperm.ru'
        img = 'https://linzaperm.ru' + product_card.query_selector('img').get_attribute('src')

        self.product = ProductInfo(name, price_in_numbers(price),
                                   price_in_numbers(discount_price), shop, url,
                                   img)


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
            self.page.goto(f"https://linzaperm.ru/catalog/?q={self.query}")

            objects = self.page.query_selector_all('.item_block.col-4.col-md-3.col-sm-6.col-xs-6')
            for obj in objects:
                self.__get_product_info(obj)
