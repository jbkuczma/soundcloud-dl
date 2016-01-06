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
FAILED_MESSAGE = '''
If a song does not download it could because of the following:
------------------------------------------------------------------------------
Email response from SoundCloud on this issue:
The developers have let me know that the problems you are having is
due to issues with RTMP. Currently certain content on SoundCloud is
using a secure streaming method called RTMP. To explain RTMP, even
if a track is set to public and streamable by the artist, if the artist
is under a major label, this label can further control those streaming
permissions. So, it looks like it should stream correctly, however it doesn't.
------------------------------------------------------------------------------
'''

def getTrack():
    return client.get('/resolve', url=SONG_TO_DOWNLOAD)


def isValid(url):
    if "soundcloud.com" in url:
        return True
    print("You did not provide a valid SoundCloud url. Please run again with a valid url")
    return False
    exit(0)


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
            print(FAILED_MESSAGE)


if __name__ == "__main__":
    if (len(sys.argv) == 2):  #link was provided
        SONG_TO_DOWNLOAD = sys.argv[1]
        if isValid(SONG_TO_DOWNLOAD):
            # printInfo() #optional
            makeStreamURL()
            download()
    else:
        print(HELP_MESSAGE)
