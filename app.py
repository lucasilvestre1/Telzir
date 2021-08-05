from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from .seeds.seeds import run_seeds
from .models.ddd_cities import Cities
from .models.plans import Plans
from .database import db
from . import settings


def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)

    with app.app_context():
        db.create_all()
        run_seeds()
    return None


application = create_app()


@application.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@application.route('/')
def index():
    # conn = get_db_connection()
    # plans = conn.execute('SELECT * FROM plans').fetchall()
    plans = {}
    # conn.close()
    return render_template('index.html', plans=plans)


@application.route('/pricing', methods=['GET', 'POST'])
def pricing():
    form = PricingForm()
    price = None
    if form.validate_on_submit():
        price = form.normal_price
    return render_template('pricing.html', form=form, price=price)


def possible_cities():
    return Cities.query


def possible_plans():
    return Plans.query


class PricingForm(FlaskForm):
    origin_city = QuerySelectField(
        'De qual cidade irá fazer a ligação?', validators=[DataRequired()], query_factory=possible_cities)
    destiny_city = QuerySelectField(
        'Para qual cidade deseja ligar?', validators=[DataRequired()], query_factory=possible_cities)
    minutes = IntegerField('Quantos minutos de duração', validators=[DataRequired()])
    plan = QuerySelectField('Escolha um plano', validators=[DataRequired()], query_factory=possible_plans)
    submit = SubmitField("Calcular")
    normal_price = DecimalField('Preço normal')
    falemais_price = DecimalField('Com o FaleMais')
