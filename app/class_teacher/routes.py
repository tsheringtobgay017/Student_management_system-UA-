import re
from flask import render_template
from flask_login import login_required
from app.class_teacher import blueprint
from app.class_teacher.service import subject_teacher, search_std
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
    if(is_classTeacher()):
        std_search = search_std()
    else:
        std_search = []
    return std_search



    
