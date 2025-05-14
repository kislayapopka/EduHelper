from collections import defaultdict
from datetime import datetime

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from calendar import monthcalendar

from application.models.post import CourseUser, Post

calendar = Blueprint('calendar', __name__)


@calendar.route('/calendar')
@login_required
def index():
    year = request.args.get('year', default=datetime.now().year, type=int)
    month = request.args.get('month', default=datetime.now().month, type=int)

    user_courses = CourseUser.query.filter_by(user_id=current_user.id).all()
    course_ids = [c.course_id for c in user_courses]

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    assignments = Post.query.filter(
        Post.course_id.in_(course_ids),
        Post.due_date >= start_date,
        Post.due_date < end_date
    ).all()

    assignments_by_day = defaultdict(list)
    for assignment in assignments:
        day = assignment.due_date.day
        if day not in assignments_by_day:
            assignments_by_day[day] = []
        assignments_by_day[day].append(assignment)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    cal = monthcalendar(year, month)

    return render_template(
        'feed/calendar.html',
        calendar=cal,
        current_date=datetime.now(),
        year=year,
        month=month,
        assignments=assignments_by_day,
        month_name=datetime(year, month, 1).strftime('%B'),
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )
