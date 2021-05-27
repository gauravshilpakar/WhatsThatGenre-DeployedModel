import os

import librosa
import librosa.display as display
import matplotlib.pyplot as plt
import numpy as np

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

PATH = "..\\db_research\\"

__package__ = None


def get_features(y, sr, n_fft=1024, hop_length=512):
    # Features to concatenate in the final dictionary
    features = {'centroid': None, 'roloff': None, 'flux': None, 'rmse': None,
                'zcr': None, 'contrast': None, 'bandwidth': None, 'flatness': None}

    # Count silence
    if 0 < len(y):
        y_sound, _ = librosa.effects.trim(
            y, frame_length=n_fft, hop_length=hop_length)
    features['sample_silence'] = len(y) - len(y_sound)

    # Using librosa to calculate the features
    features['centroid'] = librosa.feature.spectral_centroid(
        y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['roloff'] = librosa.feature.spectral_rolloff(
        y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['zcr'] = librosa.feature.zero_crossing_rate(
        y, frame_length=n_fft, hop_length=hop_length).ravel()
    features['rmse'] = librosa.feature.rms(
        y, frame_length=n_fft, hop_length=hop_length).ravel()
    features['flux'] = librosa.onset.onset_strength(y=y, sr=sr).ravel()
    features['contrast'] = librosa.feature.spectral_contrast(y, sr=sr).ravel()
    features['bandwidth'] = librosa.feature.spectral_bandwidth(
        y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['flatness'] = librosa.feature.spectral_flatness(
        y, n_fft=n_fft, hop_length=hop_length).ravel()

    # MFCC treatment
    mfcc = librosa.feature.mfcc(
        y, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)
    for idx, v_mfcc in enumerate(mfcc):
        features['mfcc_{}'.format(idx)] = v_mfcc.ravel()

    # Get statistics from the vectors
    def get_moments(descriptors):
        result = {}
        for k, v in descriptors.items():
            result['{}_max'.format(k)] = np.max(v)
            result['{}_min'.format(k)] = np.min(v)
            result['{}_mean'.format(k)] = np.mean(v)
            result['{}_std'.format(k)] = np.std(v)
            result['{}_kurtosis'.format(k)] = kurtosis(v)
            result['{}_skew'.format(k)] = skew(v)
        return result

    dict_agg_features = get_moments(features)
    dict_agg_features['tempo'] = librosa.beat.tempo(y, sr=sr)[0]

    return dict_agg_features


"""
@description: Method to split a song into multiple songs using overlapping windows
"""


def splitsongs(X, overlap=0.5):
    # Empty lists to hold our results
    temp_X = []

    # Get the input song array size
    xshape = X.shape[0]
    chunk = 33000
    offset = int(chunk * (1. - overlap))

    # Split the song and create new ones on windows
    spsong = [X[i:i + chunk]
              for i in range(0, xshape - chunk + offset, offset)]
    for s in spsong:
        if s.shape[0] != chunk:
            continue

        temp_X.append(s)

    return np.array(temp_X)


"""
@description: Method to convert a list of songs to a np array of melspectrograms
"""


def mfcc_calc(filename):
    f = os.path.join("audio_file/") + filename
    x, fs = librosa.load(f, offset=60, duration=30)
    mfcc = librosa.feature.melspectrogram(
        x, sr=fs, power=2.0, n_fft=2048, hop_length=512)

    power_db = librosa.power_to_db(mfcc)
    with plt.style.context('dark_background'):
        plt.figure(dpi=200)
        plt.title("MFCC Spectrogram")
        display.specshow(power_db, sr=fs, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')

        formatted_filename = f"{filename.split('.')[0]}_spectrogram.png"

        plt.savefig(
            f"./static/spectral_output/{formatted_filename}", dpi=200)

    print(f"\nSaving to file: {filename.split('.')[0]}.png\n")

    output_file = formatted_filename
    print(f"IMGfile= {output_file}")
    return output_file


def to_melspectrogram(songs, n_fft=1024, hop_length=256):
    # Transformation function
    def melspec(x):
        return librosa.feature.melspectrogram(x, n_fft=n_fft,
                                              hop_length=hop_length, n_mels=128)[:, :, np.newaxis]

    # map transformation of input songs to melspectrogram using log-scale
    tsongs = map(melspec, songs)
    # np.array([librosa.power_to_db(s, ref=np.max) for s in list(tsongs)])
    return np.array(list(tsongs))

def make_dataset_dl(args):
    # Convert to spectrograms and split into small windows

    signal, sr = librosa.load(
        path=os.path.join("audio_file/") + args, sr=None)

    # Convert to dataset of spectograms/melspectograms
    signals = splitsongs(signal)

    # Convert to "spec" representation
    specs = to_melspectrogram(signals)
    mfcc_image = mfcc_calc(filename=args)

    return specs, mfcc_image
