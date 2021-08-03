from ..database import db
from datetime import datetime


class Cities(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    ddd_code = db.Column(db.Integer, db.ForeignKey('ddd.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % self.name
