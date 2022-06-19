from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from app.logic.movie_logic import Movie_logic

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    try:
        return redirect(url_for('main._list'))
    except Exception as e:
        return render_template('error.html', error=e, text='Error in index function. (main_controller.py)')

@bp.route('/list/')
def _list():
    try:
        movie_logic = Movie_logic()
        page = request.args.get('page', type=int, default=1)
        kw = request.args.get('kw', type=str, default='')
        if kw:
            search = '%%{}%%'.format(kw)
            movie_list = movie_logic.filter_movie(search=search, page=page)
        else:
            movie_list = movie_logic.page_movie(page=page)
        return render_template('main_view.html', movie_list=movie_list, page=page, kw=kw)
    except Exception as e:
        return render_template('error.html', error=e, text='Error in _list function. (main_controller.py)')