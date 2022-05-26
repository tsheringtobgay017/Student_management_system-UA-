from flask import render_template
from flask_login import login_required
from app.admin import blueprint
from app.admin.service import save_user_table, save_user_detail_table, application_update, all_users, is_admin,is_classTeacher, get_user_by_id, delete_user_by_id, get_std_by_id, all_std, user_quries


@blueprint.route('/dashboard')
@login_required
def dashboard():
    if(is_admin()):
        return render_template('admin.html')

    elif(is_classTeacher()):
        return render_template('class_teacherDash.html')  
    
    else:
        return render_template('subject_teacherDash.html')
   

@blueprint.route('/admin-add-user')
@login_required
def admin_add_user():
    return render_template('/pages/user-management/add-new-user.html')


@blueprint.route('/admin-user-list')
@login_required
def admin_user_list():
    return render_template('/pages/user-management/user-list.html')


@blueprint.route('/admin-typography')
@login_required
def admin_typography():
    return render_template('/pages/ui-features/typography.html')


@blueprint.route('/admin-student-application-list')
@login_required
def admin_std_app_list():
    return render_template('/pages/student-applications/student_application_list.html')


@blueprint.route('/admin-basic-tables')
@login_required
def admin_basic_tables():
    return render_template('/pages/tables/basic-table.html')


@blueprint.route('/feedback')
@login_required
def usrfeedback():
    return render_template('/pages/user-feedback/feedback.html')


@blueprint.route('/admin-icons')
@login_required
def admin_icons():
    return render_template('/pages/icons/mdi.html')


@blueprint.route('/admin-login')
@login_required
def admin_login():
    return render_template('/pages/samples/login.html')


@blueprint.route('/admin-register')
@login_required
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


# fetch user details
@blueprint.route('/user/<id>', methods=['GET'])
def users(id):
    user = get_user_by_id(id)
    return user


@blueprint.route('/users-std', methods=['POST'])
def stdList():
    if(is_admin()):
        users_st = all_std()
    else:
        users_st = []

    return users_st

# fetch student details
@blueprint.route('/std-detials/<id>', methods=['GET'])
def std_details(id):
    return get_std_by_id(id)
    

@blueprint.route('/delete/<id>', methods=['POST'])
def delete_user(id):
    delete = delete_user_by_id(id)
    if(delete):
        return 'success', 200
    else:
        return 'error', 500


@blueprint.route('/update-status', methods=['POST'])
def update_app_status():
    if(is_admin()):
        return application_update()
    else:
        return "Failed"



@blueprint.route('/users-queries', methods=['POST'])
def queryList():
    if(is_admin()):
        users_query = user_quries()
    else:
        users_query = []

    return users_query

 