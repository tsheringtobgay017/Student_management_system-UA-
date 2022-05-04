from flask import render_template, jsonify, request
from flask_login import login_required
from app.admin import blueprint
from app.admin.service import save_user_table, save_user_detail_table, all_users, is_admin


@blueprint.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin.html')


@blueprint.route('/admin-add-user')
def admin_buttons():
    return render_template('/pages/user-management/add-new-user.html')


@blueprint.route('/admin-user-list')
def admin_dropdowns():
    return render_template('/pages/user-management/user-list.html')


@blueprint.route('/admin-typography')
def admin_typography():
    return render_template('/pages/ui-features/typography.html')


@blueprint.route('/admin-basic-elements')
def admin_basic_elements():
    return render_template('/pages/forms/basic_elements.html')


@blueprint.route('/admin-basic-tables')
def admin_basic_tables():
    return render_template('/pages/tables/basic-table.html')


@blueprint.route('/admin-charts')
def admin_charts():
    return render_template('/pages/charts/chartjs.html')


@blueprint.route('/admin-icons')
def admin_icons():
    return render_template('/pages/icons/mdi.html')


@blueprint.route('/admin-login')
def admin_login():
    return render_template('/pages/samples/login.html')


@blueprint.route('/admin-register')
def admin_register():
    return render_template('/pages/samples/register.html')


@blueprint.route('/admin-error-404')
def admin_error_404():
    return render_template('/pages/samples/error-404.html')


@blueprint.route('/admin-error-500')
def admin_error_500():
    return render_template('/pages/samples/error-500.html')


@blueprint.route('/admin-documentation')
def admin_documentation():
    return render_template('/pages/documentation/documentation.html'),


@blueprint.route('/users', methods=['POST'])
def usersList():
    if(is_admin()):
        users = all_users()
    else:
        users = []

    return users
    

# For storing admin details
@blueprint.route("/save-user", methods=['POST'])
def save_user():
        user_id = save_user_table()
        return save_user_detail_table(user_id)
        