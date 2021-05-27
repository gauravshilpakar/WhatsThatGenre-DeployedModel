import os
import sys
import argparse

from joblib import load
from tensorflow.keras.models import load_model
from models.make_dataset import make_dataset_dl
import numpy as np
import matplotlib.pyplot as plt


class AppManager:
    def __init__(self, args, model, genres):
        self.args = args
        self.genres = genres
        self.model = model

    def run(self):
        X, image = make_dataset_dl(self.args)
        model = load_model(self.model)
        preds = model.predict(X)
        votes = majority_voting(preds, self.genres)
        message = "\nIt is a '{}' song.\n Most likely genres are: {}".format(
            votes[0][0].upper(), votes[:3])
        predicted_genre = votes[0][0]
        prediction = f"{self.args.split('.')[0]}_prediction.png"
        with plt.style.context('dark_background'):
            x = []
            y = []
            for k, v in votes:
                x.append(k)
                y.append(round((v * 100), 2))

            fig, ax = plt.subplots(dpi=200)

            plt.title("Predictions")
            ax.bar(x, y)
            ax.set_xlabel('Genres')
            ax.set_ylabel('Probability')
            xlocs, xlabs = plt.xticks()
            plt.xticks(fontsize=7)
            plt.savefig(f"./static/prediction_output/{prediction}", dpi=200)
            for i, v in enumerate(y):
                ax.text(xlocs[i] - 0.25, v + 0.25, str(v), color="white")
            plt.tight_layout()
        # plt.show()
        print(message)
        return message, image, prediction, predicted_genre


# Constants
genres = {
    'metal': 0, 'disco': 1, 'classical': 2, 'hiphop': 3, 'jazz': 4,
    'country': 5, 'pop': 6, 'blues': 7, 'reggae': 8, 'rock': 9
}

# @RUN: Main function to call the appmanager


def majority_voting(scores, dict_genres):
    preds = np.argmax(scores, axis=1)
    values, counts = np.unique(preds, return_counts=True)
    counts = np.round(counts / np.sum(counts), 2)
    votes = {k: v for k, v in zip(values, counts)}
    votes = {k: v for k, v in sorted(
        votes.items(), key=lambda item: item[1], reverse=True)}
    return [(get_genres(x, dict_genres), prob) for x, prob in votes.items()]


def get_genres(key, dict_genres):
    # Transforming data to help on transformation
    labels = []
    tmp_genre = {v: k for k, v in dict_genres.items()}

    return tmp_genre[key]


def PredictModel(args):
    # if args.type not in ["dl", "ml"]:
    #     raise ValueError("Invalid type for the application. You should use dl or ml.")
    # args = "../music/cant_stop.mp3"
    model = os.path.join('models/MyModel.h5')
    app = AppManager(args, model, genres)
    message, image, prediction, predictedGenre = app.run()
    return message, image, prediction, predictedGenre


if __name__ == '__main__':
    # # Parse command line arguments
    # parser = argparse.ArgumentParser(description='Music Genre Recognition on GTZAN')

    # # Required arguments
    # parser.add_argument('-t', '--type', help='dl or ml for Deep Learning or Classical ML approaches, respectively.', type=str, required=True)

    # # Nearly optional arguments. Should be filled according to the option of the requireds
    # parser.add_argument('-m', '--model', help='Path to trained model', type=str, required=True)
    # parser.add_argument('-s', '--song', help='Path to song to classify', type=str, required=True)
    # args = parser.parse_args()

    # # Call the main function
    args = "Taylor Swift - End Game ft Ed Sheeran Future.mp4"

    PredictModel(args)
