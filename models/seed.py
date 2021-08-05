from database import db
from models.ddd_cities import DDD, Cities
from models.plans import Plans


def create_plans():
    db.session.add(Plans(name='FaleMais 30', free_min_qty=30))
    db.session.add(Plans(name='FaleMais 60', free_min_qty=60))
    db.session.add(Plans(name='FaleMais 120', free_min_qty=120))
    db.session.commit()


def create_ddd():
    db.session.add(DDD(code='011', free_min_qty=30))


def create_citie():
    db.session.add(Cities(name='São Paulo', free_min_qty=30))


def run_seeds():
    create_plans()
