class ProductInfo:
    def __init__(self, name='', price='', discount_price='', shop='', url='', img='', in_bookmarks=False):
        self._name = name
        self._price = price
        self._discount_price = discount_price
        self._shop = shop
        self._url = url
        self._img = img
        self.in_bookmarks = in_bookmarks

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_discount_price(self):
        return self._discount_price

    def get_shop(self):
        return self._shop

    def get_url(self):
        return self._url

    def get_img(self):
        return self._img

    def set_bookmark(self, flag):
        self.in_bookmarks = flag

    def is_in_bookmarks(self):
        return self.in_bookmarks
