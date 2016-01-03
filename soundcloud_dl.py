import urllib
import soundcloud
import os
import sys

CLIENT_ID = "***" #your client ID
client = soundcloud.Client(client_id=CLIENT_ID)
SONG_TO_DOWNLOAD = ""
STREAM_URL = ""
FOLDER_LOCATION = "***" #where you want the file saved to
HELP_MESSAGE = '''
* SoundCloud Downloader *

* Only one song can be downloaded at a time. Please use the following format: *
----------------------------------------------------
* python3 soundcloud_dl.py [soundcloud url] *
----------------------------------------------------
* This was developed entirely for educational purposes *

* Thank you and enjoy! *
            '''

def getTrack():
    return client.get('/resolve', url=SONG_TO_DOWNLOAD)


def printInfo():
    print("##################################")
    print(getTrack().title)
    print(getTrack().user["username"])
    print("Genre: " + getTrack().genre)
    print("Plays: " + str(getTrack().playback_count))
    print("Favorites: " + str(getTrack().favoritings_count))
    print("BPM: " + str(getTrack().bpm))
    print("ID: " + str(getTrack().id))
    print("License: " + getTrack().license)
    print("##################################")


def makeStreamURL():
    global STREAM_URL
    STREAM_URL += "http://api.soundcloud.com/tracks/%s/stream?client_id=%s" % (getTrack().id, CLIENT_ID)
    return STREAM_URL


def download():
    if not os.path.exists(FOLDER_LOCATION):
        os.makedirs(FOLDER_LOCATION)
    os.chdir(FOLDER_LOCATION)
    # path = os.path.join(FOLDER_LOCATION, setTrack().user["username"] + " - " + setTrack().title + ".mp3") #will add username of who uploaded the track to the name of the file
    path = os.path.join(FOLDER_LOCATION, getTrack().title + ".mp3")
    if os.path.isfile(path):
        print("Skipped. This file already exists")
    else:
        try:
            print("Starting download")
            urllib.request.urlretrieve(STREAM_URL, path)
            print("Download complete!")
        except:
            print("Download failed.")


if __name__ == "__main__":
    if (len(sys.argv) == 2):  # a link was provided
        SONG_TO_DOWNLOAD = sys.argv[1]
        # printInfo() #optional
        download()
    else:
        print(HELP_MESSAGE)
