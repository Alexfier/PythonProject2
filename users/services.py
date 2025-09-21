import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product():
    product = stripe.Product.create(name="Оплата курса/урока")
    return product


def create_price(amount, product):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product.get("name")},
    )
    return price


def create_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/courses/",
        line_items=[{"price": price_id.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("url")
