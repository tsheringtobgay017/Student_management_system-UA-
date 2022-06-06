import re
from flask import render_template
from flask_login import login_required
from app.class_teacher import blueprint
from app.class_teacher.service import subject_teacher, search_std, update_tbl_academic, get_std_in_class, get_std_class, get_std_marks, get_subject_teacher_info,update_tbl_std_evaluation
from app.admin.service import is_classTeacher

@blueprint.route('/add-subject-teacher')
@login_required
def add_teacher():
    return render_template('/pages/user-management/add-subject-teacher.html')


@blueprint.route('/teacher-list')
@login_required
def list_teacher():
    return render_template('/pages/user-management/teacher-list.html')


@blueprint.route('/subject-teacher-list', methods=['POST'])
def subject_teacherList():
    if(is_classTeacher()):
        subject_t = subject_teacher()
    else:
        subject_t = []
    return subject_t


@blueprint.route('/add-std-class')
@login_required
def add_student():
    return render_template('/pages/add-student/add_student_class.html')


@blueprint.route('/search-for-std', methods=['POST', 'GET'])
def search_stdList():
    return search_std()


@blueprint.route('/get-std-list')
@login_required
def get_student_list():
    return render_template('/pages/add-student/student_list_class.html')


# @blueprint.route('/view-std-detail')
# @login_required
# def view_student_detail():
#     return render_template('/pages/add-student/student_detail.html')


# fetch student details
@blueprint.route('/view-std-detail/<id>', methods=['GET'])
def view_student_detail(id):
    return get_std_class(id)


@blueprint.route('/view-std-marks/<id>')
@login_required
def view_student_marks(id):
    return get_subject_teacher_info(id)


@blueprint.route('/view-std-class-marks')
@login_required
def view_student_class_marks():
    return render_template('/pages/add-student/class_teacher_assessment.html')



@blueprint.route('/update-std-details', methods=['POST'])
@login_required
def update_std_class():
    if(is_classTeacher()):
        return update_tbl_academic()
    else:
        return "error"


@blueprint.route('/update-std-evaluation', methods=['POST'])
@login_required
def update_std_evaluation():
    if(is_classTeacher()):
        return update_tbl_std_evaluation()
    else:
        return "errorFound"



@blueprint.route('/student-class-list', methods=['POST'])
def student_classList():
    if(is_classTeacher()):
        student_in_class = get_std_in_class()
    else:
        student_in_class = []
    return student_in_class


@blueprint.route('/get-subject-marks', methods=['POST'])
def subject_marks():
    if(is_classTeacher()):
        subject_marks = get_std_marks()
    else:
        subject_marks = []
    return subject_marks