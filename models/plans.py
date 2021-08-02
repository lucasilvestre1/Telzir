from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plans(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column()