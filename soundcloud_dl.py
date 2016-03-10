import urllib
import soundcloud
import os
import sys
import requests
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3 as OldID3
from mutagen.id3 import APIC

CLIENT_ID = "***" #your client ID
FOLDER_LOCATION = "***" #where you want the file saved to
client = soundcloud.Client(client_id=CLIENT_ID)
SONG_TO_DOWNLOAD = ""
STREAM_URL = ""
URLS_TO_DOWNLOAD = []
HELP_MESSAGE = '''
* SoundCloud Downloader *

* Please use the following format: *
----------------------------------------------------
* python3 soundcloud_dl.py [soundcloud url] *
----------------------------------------------------
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


# helper function that is used to obtain information about the song (title, artist, genre, etc).
def getTrack():
    return client.get('/resolve', url=SONG_TO_DOWNLOAD)


# creates the stream url from the link provided. This url is then used later to download the song
def makeStreamURL():
    global STREAM_URL
    STREAM_URL += "http://api.soundcloud.com/tracks/%s/stream?client_id=%s" % (getTrack().id, CLIENT_ID)
    return STREAM_URL


# check if the url provided is a valid SoundCloud link
def isValid(url):
    if "soundcloud.com" in url:
        return True
    print("You did not provide a valid SoundCloud url. Please run again with a valid url")
    return False
    exit(0)


# check if url provided is a valid SoundCloud playlist link
def isPlayList(url):
    if "soundcloud.com" and "/sets/" in url:
        return True
    return False


# displays info regarding the url provided. This is completely optional and will not affect the outcome of the downloaded file
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


# adds url of each song in playlist to a list that is used for downloading
def getSongURLFromSet(set):
    global SONG_TO_DOWNLOAD
    playlistID = getTrack().id
    playlist = client.get('/playlists/%s' % (playlistID))
    for song in playlist.tracks:
        url = song["permalink_url"]
        URLS_TO_DOWNLOAD.append(url)


# applies ID3 tags and artwork to the mp3 file based on what is provided from SoundCloud
def addTags(file):
    try:
        audio = EasyMP3(file)
        audio.tags = None
        audio["artist"] = getTrack().user["username"] #depending on who uploaded the song, this may not always be the actual artist of the song
        audio["title"] = getTrack().title
        audio["genre"] = getTrack().genre
        audio.save()
        artworkURL = getTrack().artwork_url  #gets url of artwork for song provided...
        if "large" in artworkURL:  #...but we need to replace "large" with "t500x500"...
            artworkURL = artworkURL.replace("large", "t500x500")  #...to get a decent sized photo that isn't pixelated for the cover art of the mp3
        image_data = requests.get(artworkURL).content
        mime = 'image/jpeg'
        if '.jpg' in artworkURL:
            mime = 'image/jpeg'
        if '.png' in artworkURL:
            mime = 'image/png'
        audio = MP3(file, ID3=OldID3)
        audio.tags.add(
                APIC(
                    encoding=3,  #3 is for utf-8
                    mime=mime,
                    type=3,  #3 is for the cover image
                    desc='Cover',
                    data=image_data
                )
            )
        audio.save()
    except Exception as e:
        print(e)

#gets file size of song to be downloaded
def getFileSize():
    return getTrack().original_content_size


# creates save destination if that directory doesn't exist. Proceeds to download the audio file(s)
def downloadSongs(songs):
    global SONG_TO_DOWNLOAD
    i = 1
    if not os.path.exists(FOLDER_LOCATION):
        os.makedirs(FOLDER_LOCATION)
    os.chdir(FOLDER_LOCATION)
    for song in songs:
        SONG_TO_DOWNLOAD = song
        path = os.path.join(FOLDER_LOCATION, getTrack().title + ".mp3")
        if os.path.isfile(path):
            print("Skipped. This file already exists")
        else:
            try:
                makeStreamURL()
                print("Starting download: Song " + str(i) + " of " + str(len(URLS_TO_DOWNLOAD)))
                urllib.request.urlretrieve(STREAM_URL, path)
                addTags(path)
                i+=1
            except:
                print("Download failed.")
                print(FAILED_MESSAGE)
                i+=1
    print("Download complete!")


if __name__ == "__main__":
    if (len(sys.argv) == 2):  # a link was provided
        SONG_TO_DOWNLOAD = sys.argv[1]
        if isValid(SONG_TO_DOWNLOAD):
            if isPlayList(SONG_TO_DOWNLOAD):
                getSongURLFromSet(SONG_TO_DOWNLOAD)
                downloadSongs(URLS_TO_DOWNLOAD)
                exit(0)
            # printInfo() #optional
            URLS_TO_DOWNLOAD.append(SONG_TO_DOWNLOAD)
            downloadSongs(URLS_TO_DOWNLOAD)
    else:
        print(HELP_MESSAGE)
