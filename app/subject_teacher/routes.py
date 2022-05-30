from flask import render_template,request
from flask_login import login_required
from app.subject_teacher import blueprint
from app.admin.service import is_subjectTeacher
from app.subject_teacher.service import get_std_subject_teacher,get_std_marks,get_std_subject_class, store_student_assessment_details,check_exist


@blueprint.route('/view-std-table')
def view_std_table():
    return render_template('/pages/view-student-table/view-std.html')


@blueprint.route('/view-std-info/<id>')
def view_std_info(id):
    return get_std_subject_class(id)


@blueprint.route('/get-student-class-list', methods=['POST'])
def get_student_classList():
    if(is_subjectTeacher()):
        get_student_in_class = get_std_subject_teacher()
    else:
        get_student_in_class = []
    return get_student_in_class



# Route to store student detail
@blueprint.route('/store-std-marks', methods=['POST'])
def store_student_marks():
     # try:
    id = request.form.get('std_id')
    check = check_exist(id)
    if check:
        return "Error"
    else:
       return store_student_assessment_details()



@blueprint.route('/view-std-gradings')
def view_std_gradings():
    return render_template('/pages/view-student-table/view_std_marks.html')


@blueprint.route('/get-std-grade', methods=['POST'])
def get_student_grade():
    if(is_subjectTeacher()):
        student_grade = get_std_marks()
    else:
        student_grade = []
    return student_grade