from app.model.movie_model import Movie
from flask import g
import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD
from surprise.dataset import DatasetAutoFolds
from sklearn.metrics.pairwise import cosine_similarity
import os

class Recommadation():
    def __init__(self):
       self.top_n = 5
       self.rating_df = pd.read_csv('./app/static/data/ratings.csv')[['userId', 'movieId', 'rating']]
       self.movie_df = pd.read_csv('./app/static/data/movies.csv')
       self.userid = int((self.rating_df['userId'].max())+1)
       self.history = g.user.history_set
       self.cnt = self.rating_df.shape[0]
       for his in self.history:
          self.rating_df.loc[self.cnt] = [self.userid, his.movie_id, his.rating]
          self.cnt+=1
       self.rating_matrix = self.rating_df.pivot_table('rating', index='userId', columns='movieId').fillna(0)
       # self.reader = Reader(rating_scale=(0.5, 5))
       # self.data = Dataset.load_from_df(self.rating_df[['userId', 'movieId', 'rating']], reader=self.reader).build_full_trainset()
       self.rating_df.to_csv('./df.csv', header=None, index=False)
       self.reader = Reader(line_format='user item rating', sep=',', rating_scale=(0.5, 5))
       self.data_folds = DatasetAutoFolds(ratings_file='./df.csv', reader=self.reader)
       self.svd = SVD(n_factors=50, n_epochs=20, random_state=42)

    def svd_recommandation(self):
       trainset = self.data_folds.build_full_trainset()
       self.svd.fit(trainset)
       seen_movies = self.rating_df[self.rating_df['userId'] == self.userid]['movieId'].tolist()
       total_movies = self.movie_df['movieId'].tolist()
       unseen_movies = [movie for movie in total_movies if movie not in seen_movies]
       predictions = [self.svd.predict(str(self.userid), str(movieId)) for movieId in unseen_movies]
       def sortkey_est(pred):
          return pred.est
       predictions.sort(key=sortkey_est, reverse=True)
       top_predictions = predictions[:self.top_n]
       top_movie_ids = [int(pred.iid) for pred in top_predictions]
       top_movie = []
       for id in top_movie_ids:
          top_movie.append(Movie.query.get(id))
       os.remove('./df.csv')
       return top_movie

    def user_recommandation(self):
       user_sim = cosine_similarity(self.rating_matrix, self.rating_matrix)
       user_sim_df = pd.DataFrame(data=user_sim, index=self.rating_matrix.index, columns=self.rating_matrix.index)
       top_sim_user = user_sim_df[self.userid].sort_values(ascending=False)[1:4].index
       top_user_history = []
       for user in top_sim_user:
          temp = self.rating_df[self.rating_df['userId'] == user]
          temp = temp.sort_values(by='rating', ascending=False)
          temp = temp['movieId']
          if len(temp) > 5:
             temp = temp[:5]
          temp2 = []
          for id in temp:
             temp2.append(Movie.query.get(id))
          top_user_history.append(temp2)
       return top_user_history
