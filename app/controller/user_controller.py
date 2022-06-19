from flask import Blueprint, url_for, render_template, g, request, redirect, flash
from app.forms import UserHistoryForm
import functools
from app.logic.rec_logic import Recommadation
from app.logic.user_logic import User_logic
from app.logic.movie_logic import Movie_logic

bp = Blueprint('user', __name__, url_prefix='/user')

def login_required(view):
    try:
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            try:
                if g.user is None:
                    _next = request.url if request.method == 'GET' else ''
                    return redirect(url_for('register.login', next=_next))
                return view(*args, **kwargs)
            except Exception as e1:
                return render_template('error.html', error=e1, text='Error in wrapped_view function. (user_controller.py)')
        return wrapped_view
    except Exception as e2:
        return render_template('error.html', error=e2, text='Error in login_required function. (user_controller.py)')

@bp.route('/mypage/', methods=('GET', 'POST'))
@login_required
def mypage():
    form = UserHistoryForm()
    user_logic = User_logic()
    movie_logic = Movie_logic()
    try:
        user = g.user
        history_list = user.history_set
        history_dic = movie_logic.get_movie_dic(history_list=history_list)
        movie_list = movie_logic.get_movie()
        if request.method == 'POST' and form.validate_on_submit():
            user_logic.update_history(user=user, movie_id=int(movie_logic.get_movie_id(movie_data=form.movie.data)), rating=int(form.rating.data))
            return redirect(url_for('user.mypage'))
        return render_template('user_view.html', history_dic=history_dic, movie_list=movie_list, form=form)

    except Exception as e:
        return render_template('error.html', error=e, text='Error in mypage function. (user_controller.py)')




@bp.route('/delete/<int:history_id>')
@login_required
def delete(history_id):
    try:
        history_set = g.user.history_set
        if len(history_set) > 5:
            User_logic().delete_history(history_id)
        else:
            flash("History는 5개 이상이여야 합니다.")
        return redirect(url_for('user.mypage'))

    except Exception as e:
        return render_template('error.html', error=e, text='Error in delete function (user_controller.py)')

@bp.route('/rec/')
@login_required
def recpage():
    try:
        if g.user is not None:
            rec = Recommadation()
            svd_rec = rec.svd_recommandation()
            user_rec = rec.user_recommandation()
        else:
            svd_rec = None
            user_rec = None
        return render_template('rec_view.html', svd_rec=svd_rec, user_rec=user_rec)
    except Exception as e:
        return render_template('error.html', error=e, text='Error in recpage function. (user_controller.py)')