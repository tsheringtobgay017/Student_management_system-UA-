from flask import render_template
from app.home import blueprint
from app.home.service import store_student_details, get_dzo_list, get_gewog, get_village


@blueprint.route('/')
def route_default():
    return render_template('index.html')

@blueprint.route('/signin')
def signin_page():
    return render_template('signin.html')


#Route for enroll_student.html and dzongkhang list
@blueprint.route('/enroll-student-detail')
def enroll_page():
   return get_dzo_list()

# Route to store student detail
@blueprint.route('/store-student-info', methods=['POST'])
def store_studentInfo_page():
    return store_student_details()


# Route to fetch gewog list
@blueprint.route("/get-gewog-list", methods=["GET", "POST"])
def get_gewog_list():
    return get_gewog()


# Route to fetch village list
@blueprint.route("/get-village-list", methods=["GET", "POST"])
def get_village_list():
    return get_village()





