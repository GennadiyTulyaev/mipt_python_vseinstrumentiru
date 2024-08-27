from playwright.sync_api import sync_playwright
from product_info import ProductInfo
from general_functions import price_in_numbers


class MorelinzParse:
    def __init__(self, query: str):
        self.query = query
        self.product = ProductInfo()
        self.products_list = []

    def __get_product_info(self, product_card):
        name = product_card.query_selector('a').get_attribute('title')
        if product_card.query_selector('.items-list__discount-price.discount-block') is None:
            price = product_card.query_selector('.items-list__item-price').inner_text()
            discount_price = price
        else:
            price = product_card.query_selector('.discount-price').inner_text()
            discount_price = product_card.query_selector('.items-list__item-price').inner_text()

        url = 'https://morelinz.ru' + product_card.query_selector('a').get_attribute('href')
        shop = 'morelinz.ru'
        img = 'https://morelinz.ru' + product_card.query_selector('img').get_attribute('src')
        img = img.replace(' ', '%20')

        self.product = ProductInfo(name, price_in_numbers(price), price_in_numbers(discount_price), shop, url, img)
        self.products_list.append(self.product)

    def parse(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            self.context = browser.new_context()
            self.context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/109.0.0.0 Safari/537.36 '
            })
            self.page = self.context.new_page()
            self.page.goto(f"https://morelinz.ru/catalog.html?keyword={self.query}")
            # self.page.wait_for_selector('.row.items-list.items-list--container.browse-view')

            objects = self.page.query_selector_all('.col-md-4.col-xs-6.col-xxs-12.items-list__block')
            for obj in objects:
                self.__get_product_info(obj)

    def get_products(self):
        self.parse()
        return self.products_list
