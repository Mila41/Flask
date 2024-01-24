# Flask
online shop
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'shop.db' )
db = SQLAlchemy(app)


# БД - Таблица - записи
# Таблица:
# id   name   price   isActive
# 1    Some   100     True
# 2    Some2  200     False - нет в наличии
# 3    Some3  40      True
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # text = db.Colum(db.Text, nullable=False)

    def __repr__(self):
        return self.name
with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,   # id компании
              secret_key='test')     # секретный ключ компании
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        item = Item(name=name, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
