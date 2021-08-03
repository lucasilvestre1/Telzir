from ..database import db
from datetime import datetime


class Plans(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    free_min_qty = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % self.name
