from market import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email_address = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float, nullable=False, default=1000)
    items = db.relationship("Item", backref="owned_by", lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Item {self.id}"

    def assign_owner(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell_item(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
