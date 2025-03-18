import os
import string
from random import choices

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from application.config import Config
from application import db
from application.models.post import Post, Submission, PostAttachment, Course
from application.forms import PostForm, JoinCourseForm, CreateCourseForm


feed = Blueprint('feed', __name__)


def generate_course_code():
    return "".join(choices(string.ascii_uppercase + string.digits, k=8))


@feed.route('/join_course', methods=['GET', 'POST'])
def join_course():
    form = JoinCourseForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(code=form.code.data).first()
        if course:
            current_user.enrolled_courses.append(course)
            db.session.commit()
            flash(f'Вы успешно присоединились к курсу {course.name}', 'success')
        flash('Неверный код курса', 'danger')
    return jsonify({"message": "Вы успешно подключились к курсу!"}), 200


@feed.route('/create_course', methods=['POST'])
@login_required
def create_course():
    form = CreateCourseForm(request.form)
    if form.validate_on_submit():
        new_course = Course(
            name=form.name.data,
            description=form.description.data,
            teacher_id=current_user.id,
            code=generate_course_code()
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Курс успешно создан!"}), 200
    return jsonify({"message": "Ошибка валидации", "errors": form.errors}), 400


@feed.route('/assignments')
@login_required
def assignments():
    form = CreateCourseForm()
    post_form = PostForm()
    if current_user.role == 'student':
        courses_ids = [c.id for c in current_user.enrolled_courses]
        posts = Post.query.join(Post.course).filter(
            Course.id.in_(courses_ids)).order_by(
            Post.date_created.desc()).all()
    else:
        posts = Post.query.order_by(
            Post.date_created.desc()).all()

    courses = Course.query.filter_by(teacher_id=current_user.id).all()

    return render_template("feed/assignments.html", posts=posts, courses=courses, form=form, post_form=post_form)


@feed.route('/assignments/<int:post_id>')
@login_required
def assignment_detail(post_id):
    post = Post.query.get_or_404(post_id)
    submissions = Submission.query.filter_by(post_id=post_id).all()

    return render_template("feed/assignment_detail.html", post=post, submissions=submissions)


@feed.route("/create_assignment", methods=["GET", "POST"])
@login_required
def create_assignment():
    if current_user.role != "teacher":
        flash("У вас нет доступа к этой странице.", "danger")
        return redirect(url_for("feed.assignments"))

    form = PostForm()
    form.student_groups.choices = [(c.id, c.name)
                                   for c in Course.query.filter_by(teacher_id=current_user.id)]

    if form.validate_on_submit():
        new_post = Post(
            user_id=current_user.id,
            caption=form.caption.data,
            body=form.body.data,
            due_date=form.due_date.data
        )

        db.session.add(new_post)

        if form.attached_files.data:
            for file in form.attached_files.data:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(file_path)

                    attachment = PostAttachment(post_id=new_post.id, file_path=f'uploads/{filename}', filename=filename)
                    db.session.add(attachment)

        db.session.commit()

        if request.is_xhr or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": True, "message": "Задание успешно создано!"})

        flash("Задание успешно создано!", "success")
        return redirect(url_for("feed.assignments"))

    return render_template("feed/create_assignment.html", form=form)

