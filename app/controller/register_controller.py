from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.forms import UserCreateForm, UserLoginForm
from app.logic.movie_logic import Movie_logic
from app.logic.user_logic import User_logic

bp = Blueprint('register', __name__, url_prefix='/reg')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    movie_logic = Movie_logic()
    user_logic = User_logic()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            user = user_logic.filter_user(username=form.username.data)
            if not user:
                user_logic.update_user(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data,
                                       movie_id1=int(movie_logic.get_movie_id(form.movie1.data)), movie_id2=int(movie_logic.get_movie_id(form.movie2.data)),
                                       movie_id3=int(movie_logic.get_movie_id(form.movie3.data)), movie_id4=int(movie_logic.get_movie_id(form.movie4.data)),
                                       movie_id5=int(movie_logic.get_movie_id(form.movie5.data)), rating1=int(form.rating1.data),
                                       rating2=int(form.rating2.data), rating3=int(form.rating3.data), rating4=int(form.rating4.data), rating5=int(form.rating5.data))
                return redirect(url_for('main.index'))
            else:
                flash('이미 존재하는 사용자입니다.')
        movie_list = movie_logic.get_movie()
        return render_template('register_view.html', form=form, movie_list=movie_list)
    except Exception as e:
        return render_template('error.html', error=e, text='Error in signup function. (register_controller.py)')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    user_logic = User_logic()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            error = None
            user = user_logic.filter_user(username=form.username.data)
            if not user:
                error = "존재하지 않는 사용자입니다."
            elif not check_password_hash(user.password, form.password.data):
                error = "비밀번호가 올바르지 않습니다."
            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('main.index'))
            flash(error)
        return render_template('login_view.html', form=form)
    except Exception as e:
        return render_template('error.html', error=e, text='Error in login function. (register_controller.py)')

@bp.before_app_request
def load_logged_in_user():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User_logic().get_user(user_id=user_id)
    except Exception as e:
        return render_template('error.html', error=e, text='Error in load_logged_in_user function. (register_controller.py)')

@bp.route('/logout/')
def logout():
    try:
        session.clear()
        return redirect(url_for('main.index'))
    except Exception as e:
        return render_template('error.html', error=e, text='Error in logout function. (register_controller.py)')