# AutoMash
Automatically create YouTube mashups. For a given list of videos and a text, AutoMash will cut the videos together so the speakers in the video says the given text. This is best understood by considering the following two examples.

[First example](https://www.youtube.com/watch?v=r4mD1MQhz1g). This was created automatically from [this](https://www.youtube.com/watch?v=c-41IY0bOGU) video and the following text.

`In today's video I'm gonna tell you why you will waste four years of your life when you study computer science. With a computer science degree you can easily get outsourced within your first few years. The reason you clicked on this video is because you wanted to know how to get a job. However a computer science degree will not do that for you, study math or physics instead.`

### How it works
AutoMash will download the given YouTube videos and then send their audio to IBM Watson which will return a transcript of the videos. Then AutoMash uses a greedy algorithm to find the longest sequence of words in the transcript that fit the words in the given text. In the end AutoMash extracts the video sequences that corresponds to these sequences of words and cuts them together into the final video.

## How to install
### Install the repository
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

### Get access to IBM Watson
AutoMash needs a text to speech interface to work, currently it can only use IBM Watson. For this you need a free account which will allow you to transform 500 minutes of audio into text for free.

1. Register [here](https://cloud.ibm.com/registration). Sometimes account creation fails, this seems to be a faulty IBM anti fraud measure it helps to try different email addresses, private browsing / incognito mode mode or different browsers. For me it worked under Firefox with private browsing and a gmail address.
2. Go to the tutorial [here](https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-gettingStarted) and follow the pointrts under `IBM Cloud® only` to get the API key and URL.
3. Create a file called `watson.key` that has the shape
```
Url
API Key
```

Now you have finished installing AutoMash.

## How to use AutoMash
Before you can create the mashup you will need to decide on a list of YouTube videos that you want to use for this. Next we will get a transcript for these videos by querying IBM Watson, then we will write the text for the final video and create a video plan. Afterwards we can create the video and if necessary finetune the cuts. 

### Query IBM Watson
Use ```python src\create_lexicon.py PROJECT_NAME YT_URL_1 YT_URL2 ... ``` to send the audios to IBM Watson and retrieve the transcripts. Here `PROJECT_NAME` is the name of your project which will be used to name newly created files, `YT_URL_1 YT_URL2 ... ` is a list of URLs of YouTube videos separated by spaces.

### Create a video plan
The above step will have created a file called `PROJECT_NAME.txt` in the `AutoMash\tmp` directory. This text file is called the lexicon and contains all the video transcripts and is there to help you create the text for the mashup video. When writing your text ensure that you only use words that appear in the lexicon. The final video will sound better if you use longer sequences of words that appear exactly the same in the lexicon. You can also use punctuation (`,`, `.` and `;`) which will create small pauses between the speakers words.
When you have decided on a text you can use ```python src\plan_video.py PROJECT_NAME "TEXT"``` to create the video plan. Here `TEXT` is the text you just came up with, note that it needs to be wrapped in `"`s.


### Create the video
You can now create the final video with ```python src\create_video.py PROJECT_NAME```. This will create the video named `PROJECT_NAME.mp4` directly in the AutoMash directory.

If you are unhappy with how the video turns out you can either change the text by doing the steps under `Create a video plan` again, or you can finetune the cuts and length of video sequences as explained in the section below.

### (Optional) Manually edit the video plan
Maybe some of the cuts in the video bother you, for example some video sequence ends to quickly or starts too late. Then you can manually edit the video plan to fix this. The video plan can be found under `tmp\PROJECT_NAME_video_plan.txt` and has the shape

```
some words	0	0	0
some more words even longer sentences	0	0	0
```
Here each line corresponds to a video sequence that will be directly cut out from a youtube video. The three numbers influence the length of this sequence.
The first number controls the beginning of the sequence, setting it to 0.5 will mean the sequence starts 0.5 seconds earlier and setting it to -0.5 will mean it starts 0.5 seconds later. The second number controls the end of the sequence, here setting it to 0.5 will let the sequence end 0.5 seconds later and setting it to -0.5 will mean the sequence ends 0.5 seconds earlier. The last number controls the pause between the speakers words, setting it to 0.5 will add a 0.5 second pause after this phrase (during the pause the video will continue but no audio will be played). 

Afterwards, you can just create the video like mentioned above.


