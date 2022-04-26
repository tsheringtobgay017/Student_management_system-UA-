from flask import render_template
from app.home import blueprint


@blueprint.route('/')
def route_default():
    return render_template('index.html')

@blueprint.route('/signin')
def signin_page():
    return render_template('signin.html')


@blueprint.route('/shop-detail-info')
def shopDetail_page():
    return render_template('detail.html')


@blueprint.route('/cart-info')
def shopCart_page():
    return render_template('cart.html')


@blueprint.route('/checkout-info')
def checkout_page():
    return render_template('checkout.html')


@blueprint.route('/contact-info')
def contact_page():
    return render_template('contact.html')

