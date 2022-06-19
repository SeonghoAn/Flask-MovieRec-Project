from app.model.movie_model import Movie

class Movie_logic():
    def __init__(self):
        self.movie = Movie

    def get_movie(self):
        return self.movie.query.order_by(self.movie.date.desc())

    def filter_movie(self, search, page):
        return self.get_movie().filter(self.movie.title.ilike(search)).paginate(page, per_page=10)

    def page_movie(self, page):
        return self.get_movie().paginate(page, per_page=10)

    def get_movie_dic(self, history_list):
        history_dic = {}
        for history in history_list:
            movie = self.movie.query.get(history.movie_id)
            history_dic[movie.title] = [history, movie]
        return history_dic

    def get_movie_id(self, movie_data):
        return self.movie.query.filter(self.movie.title.ilike("%%{}%%".format(movie_data))).first().id