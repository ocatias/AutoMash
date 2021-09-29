# AutoMash
Automatically create YouTube mashups: for a given list of videos and a text query, will cut the videos together so the speakers in the video say the given text. Consider this example:

This was created from the videos [] with the text "".

# How to Install
## Install the repository
Get the repository:
  * Clone the repository ```git clone https://github.com/ocatias/AutoMash```
  * Go to directory ```cd AutoMash```
  * Create a folder for the virtual environment ```mkdir virtual_env```
  * Create virtual environment ```python3 -m venv virtual_env```
  * Activate virtual environment: for Windows):
     * For Windows: ```.\virtual_env\Scripts\activate.bat```
     * For Linux: ```source virtual_env/bin/activate```
 
  * If you want to have text subtitles in your videos (they can be activated in ```src\helpers.py```) then you need to install [ImageMagick](https://imagemagick.org/index.php) before installing the other dependencies
  * Install dependencies ```pip install -r requirements.txt```

## Get access to IBM Watson
AutoMash needs a text to speech interface to work, currently it can only use IBM Watson. For this you need a free account which will allow you to transform 500 minutes of audio into text for free.

1. Register [here](https://cloud.ibm.com/registration). Sometimes account creation fails, this seems to be a faulty IBM anti fraud measure it helps to try different email addresses, private browsing / incognito mode mode or different browsers. For me it worked under Firefox with private browsing and a gmail address.
2. Go to the tutorial [here](https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-gettingStarted) and follow the pointrts under `IBM Cloud® only` to get the API key and URL.
3. Create a file called `watson.key` that has the shape
```
Url
API Key
```

Now you have finished installing AutoMash.

# How to use AutoMash
