from time import sleep
from playwright.sync_api import sync_playwright
from product_info import ProductInfo


class MorelinzParse:
    def __init__(self, query: str):
        self.query = query
        self.product = ProductInfo()

    def __get_product_info(self, product_card):
        name = product_card.query_selector('a').get_attribute('title')
        url = product_card.query_selector('a').get_attribute('href')
        if product_card.query_selector('span').get_attribute('.items'
                                                             '-list__discount-price discount-block') is None:
            price = product_card.query_selector('.items-list__item-price').inner_text()
        else:
            discount_price = product_card.query_selector('.items'
                                                         '-list__discount'
                                                         '-price '
                                                         'discount-block').inner_text()
            price = product_card.query_selector('.items-list__item-price').inner_text()
        shop = 'morelinz.ru'
        img = product_card.query_selector('img').get_attribute('src')
        print(name, url, price, discount_price, shop, img)


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
            self.page.goto(f"https://morelinz.ru/catalog.html?keyword={self.query}")
            sleep(2)
            self.__get_product_info(self.page.query_selector('.col-md-4 col-xs-6 col-xxs-12 items-list__block'))

            sleep(3)


if __name__ == "__main__":
    MorelinzParse("1-day acuvue oasys 30").parse()
    sleep(10)
