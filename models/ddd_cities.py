from ..database import db
from datetime import datetime


class DDD(db.Model):
    __tablename__ = 'ddd'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False, unique=True)
    cities = db.relationship('Cities', backref='ddd', lazy=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % self.code


class Cities(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    ddd_code = db.Column(db.Integer, db.ForeignKey('ddd.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % self.name
