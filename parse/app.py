from flask import Flask, render_template, request
from collect import Collect
import psycopg2
from config import dbname, user, password, host
from product_info import ProductInfo


class Database:
    def __init__(self):
        with psycopg2.connect(dbname=dbname, user=user, password=password,
                              host=host) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS bookmarks ('
                        'name TEXT, '
                        'price INTEGER, '
                        'discount_price INTEGER, '
                        'shop TEXT'
                        'url TEXT, '
                        'img TEXT)')
            conn.commit()

    def add_to_db(self, product: ProductInfo):
        with psycopg2.connect(dbname=dbname, user=user, password=password,
                              host=host) as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO bookmarks VALUES"
                        f" ('{product.get_name()}', {product.get_price()}, "
                        f"{product.get_discount_price()}, "
                        f"'{product.get_shop()}', '{product.get_url()}', "
                        f"'{product.get_img()}')")
            conn.commit()

    def get_from_db(self):
        with psycopg2.connect(dbname=dbname, user=user, password=password,
                              host=host) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM bookmarks')
            products = []
            for product in cur.fetchall():
                products.append(ProductInfo(product[0], product[1], product[2],
                                            product[3], product[4],
                                            in_bookmarks=True))
            return products

    def delete_from_db(self, url):
        with psycopg2.connect(dbname=dbname, user=user, password=password,
                              host=host) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM bookmarks WHERE url = '{url}'")
            conn.commit()


app = Flask(__name__)

collect = Collect('sth')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search')
def search():
    query = request.form['search-query']
    collect.new_query(query)
    return render_template('result.html', search_products=enumerate(collect.collect_products(), search_query=query))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
