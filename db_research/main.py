import datetime
import os
import uuid
from datetime import datetime, timezone

from db_research.yt_download import ytdownload
from models.model_app import PredictModel

COLLECTION = "mfcc"
PATH = os.path.join("db_research/")

class mfcc_file():
    def __init__(self, _id=str(uuid.uuid4()),
                 link=None,
                 link_prediction=None,
                 datetime=str(datetime.now(timezone.utc))[:19],
                 name=None,
                 predictedGenre=None):
        self._id = str(uuid.uuid4())
        self.link = link
        self.link_prediction = link_prediction
        self.datetime = datetime
        self.name = name
        self.predictedGenre = predictedGenre

    def add_data(self, link):
        aud_file = ytdownload(link)
        aud_file += ".mp4"

        message, img_file, prediction, self.predictedGenre = PredictModel(
            aud_file)
        self.name = img_file.split("_")[0]
        print("DONE")
        output_path = os.path.join('spectral_output/')
        output_path_prediction = os.path.join('prediction_output/')
        return self.name, message

def main(inp_link):
    f = mfcc_file()
    link = inp_link
    vid_title, message= f.add_data(link)
    # , mfcc_link, prediction 
    return vid_title, message
	# , mfcc_link, prediction
