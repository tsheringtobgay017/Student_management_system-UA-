import re
from flask import render_template
from flask_login import login_required
from app.class_teacher import blueprint
from app.class_teacher.service import subject_teacher, search_std
from app.admin.service import is_classTeacher, get_std_by_id

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


# fetch student details
@blueprint.route('/std-detials/<id>', methods=['GET'])
def std_details(id):
    return get_std_by_id(id)


@blueprint.route('/view-std-detail')
@login_required
def view_student_detail():
    return render_template('/pages/add-student/student_detail.html')


@blueprint.route('/view-std-marks')
@login_required
def view_student_marks():
    return render_template('/pages/add-student/view_std_mark.html')


@blueprint.route('/view-std-class-marks')
@login_required
def view_student_class_marks():
    return render_template('/pages/add-student/class_teacher_assessment.html')

    
