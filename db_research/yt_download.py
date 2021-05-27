from pytube import YouTube
import os
SAVE_PATH = os.path.join("audio_file/")
TRASH = list(",.:*|?/'" + '"' + "'")


def ytdownload(link):
    '''
    params: 
        link: link of the youtube video to download
    returns:
        mp4 file of audio
    '''
    yt_file = YouTube(link)
    mp4_ = yt_file.streams.filter(only_audio=True, subtype="mp4")
    mp4_[-1].download(SAVE_PATH)
    print("\nAudio Downloaded Successfully!")
    TITLE = yt_file.title
    TITLE = TITLE.split(".mp4")[0]

    for t in TRASH:
        TITLE = TITLE.replace(t, '')
    print(TITLE)
    return (TITLE)

    # try:
    #     mp4_ = yt_file.streams.filter(only_audio=True, subtype="mp4")
    #     mp4_[-1].download(SAVE_PATH)
    #     print("\nAudio Downloaded Successfully!")
    #     TITLE = yt_file.title
    #     TITLE = TITLE.split(".mp4")[0]

    #     for t in TRASH:
    #         TITLE = TITLE.replace(t, '')

    #     print(TITLE)
    #     return (TITLE)

    # except:
    #     return "Download Failed!"


if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=e8CLsYzE5wk"
    print(ytdownload(link))
