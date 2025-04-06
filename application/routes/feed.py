import os
import string
from random import choices

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from application.config import Config
from application import db
from application.models.post import Post, Submission, PostAttachment, Course, CourseUser
from application.forms import PostForm, JoinCourseForm, CreateCourseForm, SubmissionForm, EditPostForm
from ..models.post import SubmissionAttachment

feed = Blueprint('feed', __name__)


def generate_course_code():
    return "".join(choices(string.ascii_uppercase + string.digits, k=8))


@feed.route('/join_course', methods=['POST'])
@login_required
def join_course():
    course_code = request.form.get('code')

    course = Course.query.filter_by(code=course_code).first()

    if course:
        user_in_course = CourseUser.query.filter_by(course_id=course.id, user_id=current_user.id).first()

        if not user_in_course:
            new_course_user = CourseUser(course_id=course.id, user_id=current_user.id)
            db.session.add(new_course_user)
            db.session.commit()
            return jsonify({'message': 'Вы успешно подключились к курсу'})
        else:
            return jsonify({'message': 'Вы уже подключены к этому курсу'})
    else:
        flash('Курс не найден', 'error')

    return redirect(url_for('feed.assignments'))


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
    post_form = PostForm()
    form = CreateCourseForm()
    join_form = JoinCourseForm()
    posts = Post.query.order_by(Post.date_created.desc()).all()

    if current_user.role == 'student':
        courses = Course.query.join(CourseUser).filter(CourseUser.user_id == current_user.id).all()
    elif current_user.role == 'teacher':
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
    else:
        courses = []

    return render_template("feed/assignments.html",
                           form=form,
                           posts=posts,
                           courses=courses,
                           join_form=join_form,
                           post_form=post_form)


@feed.route('/assignment_detail/<int:post_id>', methods=['GET', 'POST'])
@login_required
def assignment_detail(post_id):
    post = Post.query.get_or_404(post_id)
    submission_form = SubmissionForm()
    edit_form = EditPostForm()

    if current_user.role == 'teacher':
        submissions = Submission.query.filter_by(post_id=post.id).all()
    else:
        submissions = None

    if submission_form.validate_on_submit():
        new_submission = Submission(
            post_id=post.id,
            student_id=current_user.id,
        )

        if submission_form.attached_files.data:
            for file in submission_form.attached_files.data:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(file_path)

                    attachment = SubmissionAttachment(
                        submission=new_submission,
                        file_path=filename,
                        filename=filename
                    )
                    db.session.add(attachment)

        db.session.add(new_submission)
        db.session.commit()
        flash('Работа успешно отправлена', 'success')
        return redirect(url_for('feed.assignment_detail', post_id=post.id))

    return render_template("feed/assignment_detail.html",
                           post=post,
                           submissions=submissions,
                           submission_form=submission_form,
                           edit_form=edit_form)


@feed.route('/get_posts_by_course_id', methods=['GET'])
@login_required
def get_posts_by_course_id():
    course_id = request.args.get('courseId')
    posts = Post.query.filter_by(course_id=course_id).all()

    posts_json = []
    for post in posts:
        posts_json.append({
            'id': post.id,
            'caption': post.caption,
            'body': post.body,
            'date_created': post.date_created.strftime("%Y-%m-%d"),
            'due_date': post.due_date.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(posts_json)


@feed.route("/create_assignment", methods=["POST"])
@login_required
def create_assignment():
    if current_user.role != "teacher":
        flash("У вас нет доступа к этой странице.", "danger")
        return redirect(url_for("feed.assignments"))

    form = PostForm()

    if form.validate_on_submit():
        try:
            course_id = form.course_id.data
            new_post = Post(
                user_id=current_user.id,
                course_id=course_id,
                caption=form.caption.data,
                body=form.body.data,
                due_date=form.due_date.data
            )

            db.session.add(new_post)
            db.session.flush()

            if form.attached_files.data:
                for file in form.attached_files.data:
                    if file:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                        file.save(file_path)

                        attachment = PostAttachment(
                            post_id=new_post.id,
                            file_path=f'uploads/{filename}',
                            filename=filename
                        )
                        db.session.add(attachment)

            db.session.commit()
            # return jsonify({"message": "Задание успешно добавлено!"}), 200
            return redirect(url_for('feed.assignment_detail'))

        except Exception as e:
            db.session.rollback()
            flash("Произошла ошибка при создании задания.", "danger")
            return redirect(url_for('feed.assignments'))

    return jsonify({"message": "Ошибка валидации", "errors": form.errors}), 400


@feed.route("/assignment_detail/get_post/<int:post_id>", methods=["GET"])
@login_required
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        return jsonify({
            'id': post.id,
            'due_date': post.due_date.strftime("%Y-%m-%d %H:%M"),
            'caption': post.caption,
            'body': post.body,
        })
    else:
        jsonify({'error': 'Публикация не найдена'}), 404


@feed.route('/assignment_detail/update_post', methods=['POST'])
@login_required
def update_post():
    post_id = request.form.get('post_id')
    post = Post.query.get_or_404(post_id)

    if current_user.role != "teacher" or post.user_id != current_user.id:
        flash("У вас нет прав для редактирования этого задания.", "danger")
        return redirect(url_for('feed.assignments'))

    form = EditPostForm()

    if form.validate_on_submit():
        try:
            post.caption = form.caption.data
            post.body = form.body.data
            post.due_date = form.due_date.data

            if form.attached_files.data:
                for file in form.attached_files.data:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

                        file.save(file_path)

                        attachment = PostAttachment(
                            post_id=post.id,
                            file_path=f'uploads/{filename}',
                            filename=filename
                        )
                        db.session.add(attachment)

            db.session.commit()
            return jsonify({'status': 'success'})

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Ошибка обновления: {str(e)}")
            return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

    return jsonify({'error': form.errors}), 400


@feed.route('/assignment_detail/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Публикация успешно удалена.', 'success')
    return redirect(url_for('feed.assignment_detail', post_id=post_id))
