from ..database import db
from datetime import datetime


class Price(db.Model):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True)
    origin_city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    destiny_city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    plan = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    normal_price = db.Column(db.Float(precision=(7, 2)))
    falemais_price = db.Column(db.Float(precision=(7, 2)))
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % str(self.id)
