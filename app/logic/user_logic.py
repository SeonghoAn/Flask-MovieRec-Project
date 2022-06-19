from app.model.user_model import User, History
from app import db

class User_logic():
    def __init__(self):
        self.user = User
        self.history = History

    def filter_user(self, username):
        return self.user.query.filter_by(username=username).first()

    def update_user(self, username, password, email, movie_id1, movie_id2, movie_id3, movie_id4, movie_id5, rating1, rating2, rating3, rating4, rating5):
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        history1 = History(user=user, movie_id=movie_id1, rating=rating1)
        history2 = History(user=user, movie_id=movie_id2, rating=rating2)
        history3 = History(user=user, movie_id=movie_id3, rating=rating3)
        history4 = History(user=user, movie_id=movie_id4, rating=rating4)
        history5 = History(user=user, movie_id=movie_id5, rating=rating5)
        db.session.add(history1)
        db.session.add(history2)
        db.session.add(history3)
        db.session.add(history4)
        db.session.add(history5)
        db.session.commit()

    def get_user(self, user_id):
        return self.user.query.get(user_id)

    def delete_history(self, history_id):
        history = self.history.query.get_or_404(history_id)
        db.session.delete(history)
        db.session.commit()

    def update_history(self, user, movie_id, rating):
        history = user.history_set
        for his in history:
            if int(his.movie_id) == movie_id:
                self.delete_history(his.id)
        newHistory = self.history(user=user, movie_id=movie_id, rating=rating)
        db.session.add(newHistory)
        db.session.commit()
