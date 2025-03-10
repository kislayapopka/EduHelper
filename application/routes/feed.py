import os

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from application.config import Config
from application import db
from application.models.post import Post, Submission, PostAttachment
from application.forms import PostForm

feed = Blueprint('feed', __name__)


@feed.route('/assignments')
@login_required
def assignments():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("feed/assignments.html", posts=posts)


@feed.route('/assignments/<int:post_id>')
@login_required
def assignment_detail(post_id):
    post = Post.query.get_or_404(post_id)
    submissions = Submission.query.filter_by(post_id=post_id).all()

    return render_template("feed/assignment_detail.html", post=post, submissions=submissions)


@feed.route("/assignment/new", methods=["GET", "POST"])
@login_required
def create_assignment():
    if current_user.role != "teacher":
        flash("У вас нет доступа к этой странице.", "danger")
        return redirect(url_for("feed.assignments"))

    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            user_id=current_user.id,
            caption=form.caption.data,
            body=form.body.data,
            due_date=form.due_date.data
        )
        db.session.add(new_post)
        db.session.commit()

        if form.attached_files.data:
            for file in form.attached_files.data:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(file_path)

                    attachment = PostAttachment(post_id=new_post.id, file_path=f'uploads/{filename}', filename=filename)
                    db.session.add(attachment)

        db.session.commit()
        flash("Задание успешно создано!", "success")
        return redirect(url_for("feed.assignments"))

    return render_template("feed/create_assignment.html", form=form)
