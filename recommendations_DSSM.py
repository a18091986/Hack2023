import pandas as pd
import numpy as np
from datetime import date
# import matplotlib.pyplot as plt
# from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Dict, Text

import tensorflow as tf
# import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs


class MovieLensModel(tfrs.Model):
    # We derive from a custom base class to help reduce boilerplate. Under the hood,
    # these are still plain Keras Models.

    def __init__(
            self,
            user_model: tf.keras.Model,
            movie_model: tf.keras.Model,
            task: tfrs.tasks.Retrieval):
        super().__init__()

        # Set up user and movie representations.
        self.user_model = user_model
        self.movie_model = movie_model

        # Set up a retrieval task.
        self.task = task

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        # Define how the loss is computed.

        user_embeddings = self.user_model(features["user_id"])
        movie_embeddings = self.movie_model(features["id_level3"])

        return self.task(user_embeddings, movie_embeddings)


def DSSM_model():
    print("Start DSSM")

    for chunk in pd.read_csv('datasets_prep/result.csv', chunksize=1000000):
        df_attend_users_groups_dict = chunk
        break

    for chunk in pd.read_csv('datasets_prep/result.csv', chunksize=1000000):
        data = chunk
        break

    # df_attend_users_groups_dict = pd.read_csv('datasets_prep/result.csv')
    # data = pd.read_csv('datasets_prep/result.csv')

    print("Datasets Loaded")

    user_feat = df_attend_users_groups_dict[['user_id', 'id_level3', 'gender', 'age', 'register_time', 'quantity']]
    item_features = df_attend_users_groups_dict[['id_level3', 'markup', 'online_offline', 'id_level2']]

    user_features = user_feat.groupby(['user_id', 'id_level3', 'gender']).agg({'age': ['mean'],
                                                                               'register_time': ['mean'],
                                                                               'quantity': 'sum'}).reset_index()
    user_features.columns = user_features.columns.droplevel(level=1)
    user_features.drop_duplicates(inplace=True)
    item_features.drop_duplicates(inplace=True)
    data.drop_duplicates(inplace=True)

    print("Duplicates Droppped")

    user_features_float = user_features.astype({'user_id': 'str',
                                                'id_level3': 'str'})

    item_features_float = item_features.astype({'id_level3': 'str',
                                                'id_level2': 'str'})

    user_features_2 = tf.data.Dataset.from_tensor_slices(user_features_float.to_dict(orient="list"))
    item_features_2 = tf.data.Dataset.from_tensor_slices(item_features_float.to_dict(orient="list"))

    ratings = user_features_2.map(lambda x: {
        "user_id": x["user_id"],
        "id_level3": x["id_level3"],
        "gender": x["gender"],
        "age": x["age"],
        "register_time": x["register_time"],
        "quantity": x["quantity"]})

    movies = item_features_2.map(lambda x: x["id_level3"])
    user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
    user_ids_vocabulary.adapt(ratings.map(lambda x: x["user_id"]))

    movie_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
    movie_titles_vocabulary.adapt(movies)

    user_model = tf.keras.Sequential([
        user_ids_vocabulary,
        tf.keras.layers.Embedding(user_ids_vocabulary.vocabulary_size(), 64),
        # tf.keras.layers.Dense(24, activation='relu'),
        # tf.keras.layers.Dropout(0.8),
        # tf.keras.layers.Dense(64, activation='relu'),
        # tf.keras.layers.Dropout(0.8),
        # tf.keras.layers.Dense(32, activation='relu'),
    ])
    movie_model = tf.keras.Sequential([
        movie_titles_vocabulary,
        tf.keras.layers.Embedding(movie_titles_vocabulary.vocabulary_size(), 64),
        # tf.keras.layers.Dense(24, activation='relu'),
        # tf.keras.layers.Dropout(0.8),
        # tf.keras.layers.Dense(64, activation='relu'),
        # tf.keras.layers.Dropout(0.8),
        # tf.keras.layers.Dense(32, activation='relu'),
    ])

    # Define your objectives.
    task = tfrs.tasks.Retrieval(metrics=tfrs.metrics.FactorizedTopK(
        movies.batch(128).map(movie_model)
    )
    )

    # Create a retrieval model.
    model = MovieLensModel(user_model, movie_model, task)
    model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))

    # Train for 3 epochs.
    print("Models train start")
    model.fit(ratings.batch(4096), epochs=10)

    index = tfrs.layers.factorized_top_k.BruteForce(model.user_model, k=5)
    index.index_from_dataset(
        movies.batch(100).map(lambda title: (title, movie_model(title))))

    return index, model


if __name__ == '__main__':
    DSSM_model()
