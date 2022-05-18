import re
from flask import render_template
from flask_login import login_required
from app.subject_teacher import blueprint
from app.admin.service import is_subjectTeacher


@blueprint.route('/view-std-table')
def view_std_table():
    return render_template('/pages/view-student-table/view-std.html')



@blueprint.route('/view-std-info')
def view_std_info():
    return render_template('/pages/view-student-table/std_detail.html')