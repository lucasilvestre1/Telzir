from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Telzir-Quotation-FaleMais'
#db = SQLAlchemy()


class PricingForm(FlaskForm):
    origin_city = QuerySelectField('De qual cidade irá fazer a ligação?', validators=[DataRequired()])
    destiny_city = QuerySelectField('Para qual cidade deseja ligar?', validators=[DataRequired()])
    minutes = IntegerField('Quantos minutos de duração', validators=[DataRequired()])
    plain = QuerySelectField('Escolha um plano', validators=[DataRequired()])
    submit = SubmitField("Calcular")


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    # plans = conn.execute('SELECT * FROM plans').fetchall()
    plans = {}
    conn.close()
    return render_template('index.html', plans=plans)


@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    form = PricingForm()
    if form.validate_on_submit():
        pass
    return render_template('pricing.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
