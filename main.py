from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from functools import wraps
from flask_login import current_user
from flask_gravatar import Gravatar
import json
from amazonproducts import get_amazon_products, get_single_amazon_product
from lazadaproducts import get_lazada_products, get_single_lazada_product
from qootenproducts import get_qooten_products, get_single_qooten_product


# This file is responsible for the overall functions of the API
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR KEY'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def get_home_page():
    return render_template('home.html')

@app.route('/amazon/<item>')
def get_all_amazon(item):
    items = get_amazon_products(item)
    return json.dumps(items)

@app.route('/amazon/single/<path:url>')
def get_single_amazon(url):
    item = get_single_amazon_product(url)
    return json.dumps(item)

@app.route('/lazada/<item>')
def get_all_lazada(item):
    items = get_lazada_products(item)
    return json.dumps(items)

@app.route('/lazada/single/<path:url>')
def get_single_lazada(url):
    item = get_single_lazada_product(url)
    return json.dumps(item)

@app.route('/qooten/<item>')
def get_all_qooten(item):
    items = get_qooten_products(item)
    return json.dumps(items)

@app.route('/qooten/single/<path:url>')
def get_single_qooten(url):
    item = get_single_qooten_product(url)
    return json.dumps(item)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
