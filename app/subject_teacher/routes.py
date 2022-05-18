import re
from flask import render_template
from flask_login import login_required
from app.subject_teacher import blueprint
from app.admin.service import is_subjectTeacher



