from zeeguu.model.cohort import Cohort
from zeeguu.model.teacher import Teacher

from . import account, login_first
import flask


@account.route("/students/<int:cohort_id>")
@login_first
def students(cohort_id: int):
    teacher = Teacher.from_user(flask.g.user)
    cohort = Cohort.find(cohort_id)
    students = cohort.get_students()

    return flask.render_template("students.html", teacher=teacher, cohort=cohort, students=students)


@account.route("/cohorts")
@login_first
def cohorts():
    teacher = Teacher.from_user(flask.g.user)
    the_cohorts = teacher.get_cohorts()

    return flask.render_template("cohorts.html", teacher=teacher, cohorts=the_cohorts)
