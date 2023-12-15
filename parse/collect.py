from morelinz_parse import MorelinzParse
from linzaperm_parse import LinzapermParse
from lensgo_parse import LensgoParse
from product_info import ProductInfo
from functools import reduce
from operator import concat


class Collect:
    def __init__(self, query):
        self.query = query
        self.all_products = []

    def collect_products(self):
        self.all_products.append(MorelinzParse(self.query).get_products())
        self.all_products.append(LinzapermParse(self.query).get_products())
        self.all_products.append(LensgoParse(self.query).get_products())

        self.all_products = reduce(concat, self.all_products)

        self.all_products.sort(key=ProductInfo.get_discount_price)

        for product in self.all_products:
            print(product.get_discount_price(), product.get_name(), product.get_img())

        return self.all_products
    
    def new_query(self, new_query):
        self.old_query = self.query
        self.all_products = []
        self.query = new_query
