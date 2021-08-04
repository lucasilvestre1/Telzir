from ..models.plans import Plans
from ..database import db


def create_plans():
    db.session.add(Plans(name='FaleMais 30', free_min_qty=30))
    db.session.add(Plans(name='FaleMais 60', free_min_qty=60))
    db.session.add(Plans(name='FaleMais 120', free_min_qty=120))
    db.session.commit()


def delete_plans():
    db.session.execute('DELETE FROM plans;')
    db.session.commit()
