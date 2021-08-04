from .plans import create_plans, delete_plans
from .ddd_cities import create_ddd, delete_ddd, create_cities, delete_cities


def run_seeds():
    delete_plans()
    create_plans()

    delete_ddd()
    create_ddd()

    delete_cities()
    create_cities()


