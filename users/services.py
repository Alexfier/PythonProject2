import stripe

from config.settings import SECRET_KEY_API

stripe.api_key = SECRET_KEY_API


def creating_product_stripe(course):
    """Создание продукта в страйпе"""
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product


def creating_price_stripe(payment_amount, product_id):
    """Создание цены в страйпе"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(payment_amount * 100),
        product=product_id,
    )
    return price


def creating_session_stripe(price_id):
    """Создание сессии для получения ссылки на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url="https://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}",
    )
    return session.id, session.url
