import stripe
from currency_converter import CurrencyConverter

from config.settings import STRIPE_KEY

stripe.api_key = STRIPE_KEY


def convert_rub_to_usd(rub_amount):
    return CurrencyConverter().convert(rub_amount, "RUB", "USD")


def create_price(amount):
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product_data={"name": "LMS Course"},
    )


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def pay(rub_amount):
    """
    Выполннять платеж
    :param rub_amount: сумма платежа в Российских Рублях
    :return: id сессии, url платежа
    """
    usd_amount = convert_rub_to_usd(rub_amount)
    price = create_price(usd_amount)
    return create_session(price)


def get_session_info(session_id):
    """Получить информацию о сессии по ее id"""
    return stripe.checkout.Session.retrieve(
        session_id,
    )
