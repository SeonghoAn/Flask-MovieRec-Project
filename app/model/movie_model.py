from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    link = db.Column(db.Text, nullable=False)
    img_path = db.Column(db.Text, nullable=False)

class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'))
    movie = db.relationship('Movie', backref=db.backref('genre_set'))