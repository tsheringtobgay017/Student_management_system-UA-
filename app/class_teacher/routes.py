import re
from flask import render_template
from flask_login import login_required
from app.class_teacher import blueprint

from app.class_teacher.service import subject_teacher, search_std, update_tbl_academic, get_std_in_class, get_std_class, get_std_marks, get_subject_teacher_info, update_tbl_std_evaluation, editTheTeacher, update_editteacher, delete_Teacher, students, std_time_table, get_time_table
from app.admin.service import is_classTeacher

@blueprint.route('/add-subject-teacher')
@login_required
def add_teacher():
    return render_template('/pages/user-management/add-subject-teacher.html')


@blueprint.route('/teacher-list')
@login_required
def list_teacher():
    return render_template('/pages/user-management/teacher-list.html')

# for time table upload

@blueprint.route('/timetable')
@login_required
def get_student_timetable():
    return render_template('/pages/user-management/timetable.html')


@blueprint.route('/stdtimetable')
@login_required
def upload_studenttimetable():
    return render_template('/pages/user-management/view_time_table.html')


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


@blueprint.route('/get-std-result', methods=['POST'])
def std_results():
    if(is_classTeacher()):
        subject_marks = get_std_marks()
    else:
        subject_marks = []
    return subject_marks

# edit teachers
@blueprint.route('/edit_teacher/<id>', methods=['GET'])
@login_required
def edit_user(id):
    return editTheTeacher(id)
  

# updating modal
@blueprint.route('/updating_teacherlist', methods=['POST'])
@login_required
def updating_the_user():
    if(is_classTeacher()):
        return update_editteacher()
    else:
        return "errorFound"


# delete teacher
@blueprint.route('/deleteTeacher/<id>', methods=['POST'])
def delete_user(id):
    return delete_Teacher(id)
        

# delete student list
@blueprint.route('/deleteStudentList/<id>', methods=['POST'])
def delete_student(id):
    return students(id)

# ädding time table
@blueprint.route('/save-timetable', methods=['POST'])
def student_timetable():
    return std_time_table()

# fetch time table
@blueprint.route('/view-time-table<id>', methods=['POST'])
def std_timetable():
        return get_time_table()
   
