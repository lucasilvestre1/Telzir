from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from .models.cities import Cities
from .models.plans import Plans
from .database import db
# import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Telzir-Quotation-FaleMais'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telzir.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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


# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn


@app.route('/')
def index():
    # conn = get_db_connection()
    # plans = conn.execute('SELECT * FROM plans').fetchall()
    plans = {}
    # conn.close()
    return render_template('index.html', plans=plans)


@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    form = PricingForm()
    if form.validate_on_submit():
        pass
    return render_template('pricing.html', form=form)


db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)


