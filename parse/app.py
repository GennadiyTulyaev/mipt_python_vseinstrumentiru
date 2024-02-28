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
                        'shop TEXT, '
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
                                            product[3], product[4], product[5],
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
db = Database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/', methods=["POST"])
def search():
    query = request.form['search-query']
    collect.new_query(query)
    return render_template('result.html', search_products=enumerate(collect.collect_products()), search_query=query,
                           len=len(collect.collect_products()))

    # return render_template('result.html', search_products=enumerate(collect.collect_products()), search_query=query, len=len(collect.collect_products()))


@app.route('/show_bookmarks/')
def show_bookmarks():
    return render_template('bookmarks.html', search_products=db.get_from_db(), len=len(db.get_from_db()))

@app.route('/add_delete_bookmarks/', methods=["POST"])
def add_to_bookmarks():
    product_id = int(request.form.get('card-product-id'))
    product = collect.collect_products()[product_id]
    if product.is_in_bookmarks():
        db.delete_from_db(product.get_url())
    else:
        db.add_to_db(product)

    return render_template('result.html', search_products=enumerate(collect.collect_products()), search_query=collect.query,
                           len=len(collect.collect_products()))



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
