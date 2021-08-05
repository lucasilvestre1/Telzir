from ..seeds.ddd_cities import delete_ddd, create_ddd, delete_cities, create_cities
from ..seeds.plans import delete_plans, create_plans


def run_seeds():
    """ Delete old seeds before populate """
    delete_plans()
    create_plans()

    delete_ddd()
    create_ddd()

    delete_cities()
    create_cities()


