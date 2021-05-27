import os
from markupsafe import Markup
from flask import (Flask, flash, render_template, request)

from db_research.main import main as mfcc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

__package__ = None
@app.route('/', methods=['GET', 'POST'])
@app.route("/ytlink", methods=['GET', 'POST'])
def yt_link():
    if request.method == "POST":
        link = request.form["nm"]
        if "youtu" in link:
            vid_title, message= mfcc(link)
            flash(f"Link Received: {link}", category="info")
            flash(f"Title: {vid_title}", category="info")
            flash(f"{message}\n")
            mfcc_img = os.path.join(f"spectral_output/{vid_title}_spectrogram.png" )
            prediction_img = os.path.join(f"prediction_output/{vid_title}_prediction.png")
            firstSplit = link.split('://')[-1]
            if firstSplit.split('/')[0] == "www.youtube.com":
                embedlink = firstSplit.split('=')[-1]
            elif firstSplit.split('/')[0] == "youtu.be":
                embedlink = firstSplit.split('/')[-1]
            embedcode = f'<iframe src="https://www.youtube.com/embed/{embedlink}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
            return render_template('ytpage.html', mfcc_link=mfcc_img, prediction_link=prediction_img, embedcode = Markup(embedcode))
        else:
            flash(f"Invalid Link Received", category="info")
            return render_template('ytpage.html')
		
    else:
        return render_template('ytpage.html')

def root_dir():
    return app. instance_path

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port = 8000)