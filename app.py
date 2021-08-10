from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from .seeds.seeds import run_seeds
from .models.ddd_cities import Cities
from .models.plans import Plans
from .models.price import Price
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


@application.route('/quotes')
def quotes():
    all_quotes = get_all_quotes()
    return render_template('quotes.html', quotes=all_quotes, price=Price)


def get_all_quotes():
    return Price.query.order_by(Price.id.desc()).all()


def get_city_name(city_repr):
    """ Remove DDD from City representation"""
    return str(city_repr).split(')')[-1].strip()


@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@application.route('/delete/<int:qid>')
def delete_quote(qid):
    # TODO: !
    all_quotes = get_all_quotes()
    quote_to_delete = Price.query.get_or_404(qid)
    try:
        db.session.delete(quote_to_delete)
        db.session.commit()
        flash('Cotação excluida com sucesso!')
        all_quotes = get_all_quotes()
        return render_template('quotes.html', quotes=all_quotes, price=Price)
    except Exception as e:
        flash('Erro ao excluir a cotação. %s' % e)
        return render_template('quotes.html', quotes=all_quotes, price=Price)


@application.route('/update/<int:qid>', methods=['GET', 'POST'])
def update_quote(qid):
    form = PricingForm()
    quote_to_update = Price.query.get_or_404(qid)
    if form.validate_on_submit():
        price_obj = Price()
        try:
            updated_price = price_obj.pricing_quotation(
                origin_city_id=Cities.query.filter_by(name=get_city_name(form.origin_city.data))[0],
                destiny_city_id=Cities.query.filter_by(name=get_city_name(form.destiny_city.data))[0],
                minutes=form.minutes.data,
                plan_id=Plans.query.filter_by(name=str(form.plan.data))[0],
                quote_to_update=quote_to_update,
            )
            flash('A cotação foi recalculada com sucesso!')
            return render_template('update_quote.html', form=form, quote_to_update=updated_price, updated=True)
        except Exception as e:
            flash('Erro ao tentar recalcular a cotação, %s' % e)
            return render_template('update_quote.html', form=form, quote_to_update=quote_to_update)
    else:
        form.origin_city.data = Cities.query.filter_by(name=quote_to_update.origin_city)[0]
        form.destiny_city.data = Cities.query.filter_by(name=quote_to_update.destiny_city)[0]
        form.plan.data = Plans.query.filter_by(name=quote_to_update.plan)[0]

        return render_template('update_quote.html', form=form, quote_to_update=quote_to_update)


@application.route('/plan/<int:plan>/pricing', methods=['GET', 'POST'])
def pricing_plan(plan):
    return pricing(plan=plan)


@application.route('/pricing', methods=['GET', 'POST'])
def pricing(plan=False):
    form = PricingForm()
    price = None
    if form.validate_on_submit():
        price_obj = Price()
        new_price = price_obj.pricing_quotation(
            origin_city_id=Cities.query.filter_by(name=get_city_name(form.origin_city.data))[0],
            destiny_city_id=Cities.query.filter_by(name=get_city_name(form.destiny_city.data))[0],
            minutes=form.minutes.data,
            plan_id=Plans.query.filter_by(name=str(form.plan.data))[0],
        )
        new_price = Price.query.get_or_404(new_price.id)
        # https://stackoverflow.com/questions/68584469/represent-foreign-key-as-value-from-another-column-in-the-foreign-table
        if new_price:
            form = PricingForm()
            price = new_price
            flash('Calculado Com Sucesso!')

    if plan:
        form.plan.data = Plans.query.filter_by(free_min_qty=plan)[0]

    return render_template('pricing.html', form=form, price=price)


def possible_cities():
    return Cities.query


def possible_plans():
    return Plans.query


# TODO: Mover Form para outro .py


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

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        if self.get_ddd(self.origin_city.data) == self.get_ddd(self.destiny_city.data):
            self.destiny_city.errors.append('Ligações entre o mesmo DDD não são precificadas.')
            result = False

        return result

    @staticmethod
    def get_ddd(city):
        return str(city)[:5]
