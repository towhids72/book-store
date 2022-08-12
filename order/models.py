from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_open = db.Column(db.Boolean, default=False)
    order_items = db.relationship('OrderItem', backref='order_items_set')

    def __repr__(self):
        return f'<{self.id} - {self.user_id}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_items': [item.serialize() for item in self.order_items]
        }


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    book_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, book_id: int, quantity: int):
        self.book_id = book_id
        self.quantity = quantity


    def __repr__(self):
        return f'<{self.id} - {self.order_id} - {self.book_id} - {self.quantity}>'

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'book_id': self.book_id,
            'quantity': self.quantity
        }
