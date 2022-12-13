import re
from flask import render_template
from flask_login import login_required
from app.HR import blueprint
from app.admin.service import is_human_resource
from app.HR.service import get_student_fee


@blueprint.route('/transaction_list')
def view_payment_list():
    return render_template('/pages/payment.html')


@blueprint.route('/summit_fees', methods=['POST'])
def submit_fee():
    if(is_human_resource()):
        student_fee = get_student_fee()
    else:
        student_fee = []
    return student_fee
