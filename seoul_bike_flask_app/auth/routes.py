from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from seoul_bike_flask_app import db
from seoul_bike_flask_app import login_manager
from seoul_bike_flask_app.auth.forms import SignupForm, LoginForm
from seoul_bike_flask_app.models import User, Blog, UserBlogStars

auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    if id is not None:
        return User.query.get(int(id))
    return None


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        logout_user()
    except Exception as e:
        pass

    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(
                f"Hello, {user.first_name} {user.last_name}. You are signed up.",
                'info')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        logout_user()
    except Exception as e:
        pass

    login_form = LoginForm()
    print('signin', "login_form.validate_on_submit(): ",
          login_form.validate_on_submit())
    if login_form.validate_on_submit():

        try:
            print("login_form.email: ", login_form.email.data)
            print("login_form.validate_password(): ", dir(login_form))
            user = User.query.filter_by(email=login_form.email.data).first()
            login_user(user)
        except Exception as e:
            print("E: ", e)

        flash(f"You are logged in as {login_form.email.data}")
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=login_form)


@auth_bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        pass
    return redirect("/signin")


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@auth_bp.route("/blog/submit_post", methods=["GET", "POST"])
@login_required
def submit_post():
    print("current_user: ", current_user)
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        title = str(title).strip()
        content = str(content).strip()

        if title and content:
            try:
                blog = Blog(
                    title=title,
                    content=content,
                )
                current_user.article_list.append(blog)
                db.session.commit()
                flash(f"You are create new blog")
            except Exception as e:
                print("E: ", e)

    return render_template("blog_post.html")


@auth_bp.route("/blog", methods=["GET", "POST"])
@login_required
def blog():
    search = request.args.get("search", "")
    search = str(search).strip()

    if search:
        blogs = Blog.query.filter(
            Blog.title.like("%" + search + "%"),
        )
    else:
        blogs = Blog.query.filter()

    return render_template("blog.html", blogs=blogs)


@auth_bp.route("/blog/<post_id>", methods=["GET", "POST"])
@login_required
def post_id(post_id):
    blog = Blog.query.get(post_id)
    if not blog:
        return redirect("/blog")
    obj = UserBlogStars.query.filter_by(uid=current_user.id,
                                        bid=post_id).first()
    if obj:
        blog.count = obj.count
    else:
        blog.count = 0

    star_index = request.args.get("star_index")
    if star_index:
        if str(star_index).isdigit():
            star_index = int(star_index)
        else:
            star_index = 0
        print("OBJ: ", obj)
        if obj:
            obj.count = star_index
        else:
            ubg = UserBlogStars(uid=current_user.id, bid=post_id,
                                count=star_index)
            db.session.add(ubg)
        db.session.commit()
        return redirect("/blog/" + post_id)

    return render_template("post_id.html", blog=blog)


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in (
    'http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'
