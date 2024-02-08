from flask import Flask, request
from textblob import TextBlob
import googleapiclient.discovery
import googleapiclient.errors

app = Flask(__name__)

@app.get('/analysis')
def analysis_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    comments = get_comments(video_id)

    positive = 0
    neutral = 0
    negative = 0

    for comment in comments:
        mood = get_mood(comment, threshold=0.1)
        if mood == "positive":
            positive = positive + 1
        elif mood == "negative":
            negative = negative + 1
        else:
            neutral = neutral + 1
    
    positive_score = positive / len(comments)
    neutral_score = neutral / len(comments)
    negative_score = negative / len(comments)

    overall_score = str(positive_score) + "," + str(neutral_score) + "," + str(negative_score)

    return overall_score, 200

def get_mood(input_text, threshold):
    sentiment = TextBlob(input_text).sentiment.polarity

    friendly_threshold = threshold
    hostile_threshold = -threshold

    if sentiment >= friendly_threshold:
        return "positive"
    elif sentiment <= hostile_threshold:
        return "negative"
    else:
        return "neutral"

def get_comments(vidID):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBYPNUXqgnRg1-5tnZsn_lbVib-WjG6IAM"

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.commentThreads().list(
    part="snippet",
    videoId=vidID,
    maxResults=200)

    response = request.execute()

    comment_list = []

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = comment.replace("<" , "~")
        comment = comment.replace(">" , "~")
        comment = comment.replace("&#39;", "")
        comment = comment.replace("&quot;", '"')
        commentArr = []
        commentArr = comment.split("~")
        for comment in commentArr:
            if "href" in comment:
                commentArr.remove(comment)
            if "/a" in comment:
                commentArr.remove(comment)
        comment = "".join(commentArr)
        comment_list.append(str(comment))
    
    return comment_list

if __name__ == '__main__':
    app.run()