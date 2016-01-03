#SoundCloud-dl
Easily download any SoundCloud track even if a download link is not provided.

##*Requirements*
    This script uses python3
  SoundCloud's python wrapper is necessary. 
  
    pip install soundcloud
  You will also need to have a Client ID from SoundCloud. To receive one you need to create an app [here](http://soundcloud.com/you/apps/new). Once you have created an app and received your Client ID, download the source code and edit the code so your Client ID is used along with the folder location of where you want the files saved to.

##*Usage*
  From the terminal run the following:
  
    python3 soundcloud_dl.py [soundcloud url]
  Only one track can be downloaded at a time. If you wish to download more tracks, simply run the script with a different url!

##*In Development*
  *Check if link provided is a valid SoundCloud link

  *Add proper mp3 tags and artwork that is provided via SoundCloud
  
  *Allow for a playlist to be downloaded
  
  *Allow a certain number of a user's reposted and favorited tracks to be downloaded

----
***This was developed entirely for educational purposes.***

  
