from flask import Flask, render_template, request
import snscrape.modules.twitter as sntwitter
import snscrape.modules.reddit as snreddit
from datetime import datetime
import pandas as pd
import json
import os

soeye = Flask(__name__)

# Website navigation
@soeye.route('/')
@soeye.route('/start')
def start():
    return render_template('start.html')

@soeye.route('/about')
def about():
    return render_template('about.html')

@soeye.route('/report')
def report():
    json_file = open('static/json/report.json')
    project_details = json.load(json_file)
    json_file.close()
    return render_template('report.html', project_name=project_details['project_name'], project_number=project_details['project_number'],
    project_description=project_details['project_description'], interest_number=project_details['interest_number'])

@soeye.route('/results')
def results():
    current_directory = os.getcwd()
    project_path = os.path.join(current_directory, 'static\json')
    files = os.listdir(project_path)
    files.remove('report.json')
    return render_template('results.html', files=files)

@soeye.route('/search')
def search():
    return render_template('search.html')


# Display search results
@soeye.route('/search_result', methods=['POST'])
def search_result():
    form_data = request.form.to_dict()
    json_file = open('static/json/'+form_data['file_name'])
    data = pd.DataFrame(json.load(json_file))
    json_file.close()
    return render_template('results.html', tables=[data.to_html()], titles=[''])


# Set project details
@soeye.route('/set_details', methods=['POST'])
def set_details():
    form_data = request.form.to_dict()
    json_file = open('static/json/report.json')
    project_details = json.load(json_file)
    json_file.close()
    project_details['project_name'] = form_data['project_name']
    project_details['project_number'] = form_data['project_number']
    project_details['project_description'] = form_data['project_description']
    with open('static/json/report.json', 'w') as f:
        json.dump(project_details, f, indent=4)
    return render_template('report.html', project_name=project_details['project_name'], project_number=project_details['project_number'],
    project_description=project_details['project_description'], interest_number=project_details['interest_number'])


# Social media search
@soeye.route('/twitter', methods=['POST'])
def twitter():
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    twitter_posts = []
    form_data = request.form.to_dict()
    for i, post in enumerate(sntwitter.TwitterSearchScraper('from:'+form_data['username']).get_items()):
        if i>=int(form_data['number']):
            break
        twitter_posts.append([post.date, post.sourceLabel, post.likeCount, post.rawContent, post.media, post.links, 
        post.replyCount, post.retweetCount, post.quoteCount, post.retweetedTweet, post.quotedTweet, post.mentionedUsers])
    data = pd.DataFrame(twitter_posts, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks', 'Replies', 'Retweets', 
    'Quotes', 'Retweeted', 'Quoted', 'Tagged'])
    data.to_json('static/json/twitter_posts_'+form_data['username']+' '+timestamp+'.json', indent=4)
    return render_template('results.html', tables=[data.to_html()], titles=['']) 

@soeye.route('/reddit', methods=['POST'])
def reddit():
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    reddit_submissions = []
    reddit_comments = []
    form_data = request.form.to_dict()
    for i, post in enumerate(snreddit.RedditUserScraper(form_data['username']).get_items()):
        if i>=int(form_data['number']):
            break
        if isinstance(post, snreddit.Submission):
            reddit_submissions.append([post.date, post.url, post.subreddit, post.title, post.selftext, post.link])
        elif isinstance(post, snreddit.Comment):
            reddit_comments.append([post.date, post.url, post.subreddit, post.body])

    data_submussions = pd.DataFrame(reddit_submissions, columns=['Date', 'Url', 'Subreddit', 'Title', 'Text', 'Media'])
    data_submussions.to_json('static/json/reddit_submissions_'+form_data['username']+' '+timestamp+'.json', indent=4)
    data_comments = pd.DataFrame(reddit_comments, columns=['Date', 'Url', 'Subreddit', 'Text',])
    data_comments.to_json('static/json/reddit_comments_'+form_data['username']+' '+timestamp+'.json', indent=4)
    return  render_template('results.html', tables=[data_submussions.to_html()], titles=['']) 


if __name__ == "__main__":
    soeye.run(debug=False)