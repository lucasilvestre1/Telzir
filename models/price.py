from ..database import db
from datetime import datetime
import locale


class Price(db.Model):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True)
    origin_city = db.Column(db.String(60), db.ForeignKey('cities.name'), nullable=False)
    destiny_city = db.Column(db.String(60), db.ForeignKey('cities.name'), nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    plan = db.Column(db.String(60), db.ForeignKey('plans.name'), nullable=False)
    normal_price = db.Column(db.Float(precision=(7, 2)))
    falemais_price = db.Column(db.Float(precision=(7, 2)))
    valid_call = db.Column(db.Boolean, default=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '%s' % str(self.id)

    @staticmethod
    def get_formatted_price(price):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(price, grouping=True, symbol='R$')

    def pricing_quotation(self, origin_city_id, destiny_city_id, minutes, plan_id):
        """
        Create Pricing FaleMais-Telzir
        :param obj origin_city_id: City origin
        :param obj destiny_city_id: City destiny
        :param int minutes: minutes quantity
        :param obj plan_id: Plan
        :return: Price created
        """
        origin_ddd, destiny_ddd = self.get_ddd(origin_city_id, destiny_city_id)
        minute_price = self.get_minute_price(origin_ddd, destiny_ddd)
        if type(minute_price) is float:
            valid_call = True
            free_min = plan_id.free_min_qty
            normal_price = round(minute_price * minutes, 2)
            falemais_price = self.get_falemais_price(minutes, minute_price, free_min)
        else:  # Invalid Origin DDD vs Destiny DDD
            valid_call = False
            normal_price = 0.00
            falemais_price = 0.00

        new_price = Price(
            origin_city=origin_city_id.name,
            destiny_city=destiny_city_id.name,
            minutes=minutes,
            plan=plan_id.name,
            normal_price=normal_price,
            falemais_price=falemais_price,
            valid_call=valid_call,
        )

        db.session.add(new_price)
        db.session.commit()

        return new_price
    
    @staticmethod
    def get_ddd(origin_city_id, destiny_city_id):
        origin_ddd = origin_city_id.ddd_code
        destiny_ddd = destiny_city_id.ddd_code

        return origin_ddd, destiny_ddd

    @staticmethod
    def get_minute_price(origin_ddd, destiny_ddd):
        """
        Origem  Destino  $/min
        011     016      1.90
        016     011      2.90
        011     017      1.70
        017     011      2.70
        011     018      0.90
        018     011      1.90
        """
        if origin_ddd == '011' and destiny_ddd == '016':
            return 1.90
        elif origin_ddd == '011' and destiny_ddd == '017':
            return 1.70
        elif origin_ddd == '011' and destiny_ddd == '018':
            return 0.90
        elif origin_ddd == '016' and destiny_ddd == '011':
            return 2.90
        elif origin_ddd == '017' and destiny_ddd == '011':
            return 2.70
        elif origin_ddd == '018' and destiny_ddd == '011':
            return 1.90
        else:
            return False

    @staticmethod
    def get_falemais_price(minutes, min_price, free_min):
        """
        Com o novo produto FaleMais da Telzir o cliente adquire um plano e pode falar de graça até
        um determinado tempo (em minutos) e só paga os minutos excedentes. Os minutos
        excedentes tem um acréscimo de 10% sobre a tarifa normal do minuto. Os planos são
        FaleMais 30 (30 minutos), FaleMais 60 (60 minutos) e FaleMais 120 (120 minutos).

        :param int minutes: minutes quantity
        :param float min_price: price per minute
        :param int free_min: quantity of free minutes
        :return: falemais_price value
        """
        if minutes <= free_min:
            return 0.00  # de graça até um determinado tempo (em minutos)

        min_tax = min_price + (min_price / 100) * 10  # acréscimo de 10% sobre a tarifa normal do minuto
        min_to_pay = minutes - free_min  # só paga os minutos excedentes

        falemais_price = round(min_to_pay * min_tax, 2)
        return falemais_price
