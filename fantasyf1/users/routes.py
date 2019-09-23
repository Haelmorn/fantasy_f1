from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from fantasyf1 import db, bcrypt
from fantasyf1.models import User, Post, Team
from fantasyf1.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, CreateTeamForm)
from fantasyf1.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}!. You can now log in into the site.",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Welcome, {user.username}", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please, check your credentials.", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pictures/" + current_user.image_file
    )
    return render_template(
        "account.html", title="account", image_file=image_file, form=form
    )

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(per_page=8, page=page)
    )
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send. Click the link to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That token is invalid or expired.", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pw
        db.session.commit()
        flash(
            f"Your password has been updated. You should be now able to log in using your new password.",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset password", form=form)


@users.route("/user/<string:username>/my_team")
def user_team(username):
    user = User.query.filter_by(username=username).first_or_404()
    team = Team.query.filter_by(head=user).first()
    if team is not None:
        return render_template("team.html", title='My team', team=team, user=user)
    else:
        abort(404)

@users.route("/user/<string:username>/create_team", methods=['POST', 'GET'])
@login_required
def create_user_team(username):
    form = CreateTeamForm()
    if form.validate_on_submit():
        team = Team(name=form.team_name.data, primary_driver=form.primary_driver.data, secondary_driver=form.secondary_driver.data,
        team=form.team.data, head=current_user)
        db.session.add(team)
        db.session.commit()
        flash("Your team has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_team.html", title="Create your team", form=form)