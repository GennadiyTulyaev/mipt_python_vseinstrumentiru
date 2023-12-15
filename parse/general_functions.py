def price_in_numbers(price: str):
    num_price = ''.join([x for x in price if x.isdigit()])
    return num_price
