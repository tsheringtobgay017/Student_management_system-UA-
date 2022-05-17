import re
from flask import render_template
from flask_login import login_required
from app.class_teacher import blueprint
from app.admin.service import is_classTeacher

@blueprint.route('/add-subject-teacher')
def add_teacher():
    return render_template('/pages/user-management/add-subject-teacher.html')


@blueprint.route('/teacher-list')
def list_teacher():
    return render_template('/pages/user-management/teacher-list.html')

    