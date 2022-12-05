import hashlib
import json
import os
from datetime import datetime
import numpy as np
import pandas as pd
import snscrape.modules.reddit as snreddit
import snscrape.modules.twitter as sntwitter
from flask import Flask, render_template, request

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
    project_description=project_details['project_description'], interest_number=project_details['interest_number'], 
    data_of_interest=project_details['data_of_interest'])

@soeye.route('/results')
def results():
    current_directory = os.getcwd()
    project_path = os.path.join(current_directory, 'static\html')
    files = os.listdir(project_path)
    files.remove('.gitkeep')
    files.reverse()
    return render_template('results.html', files=files)

@soeye.route('/search')
def search():
    current_directory = os.getcwd()
    project_path = os.path.join(current_directory, 'static\html')
    files = os.listdir(project_path)
    files.remove('.gitkeep')
    files.reverse()
    return render_template('search.html', files=files)


# Display search results
@soeye.route('/search_result', methods=['POST'])
def search_result():
    form_data = request.form.to_dict()
    data = pd.read_html('static/html/'+form_data['file_name'])
    return render_template('results.html', tables=[data[0].to_html(index=False)], titles=[''])


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
    project_description=project_details['project_description'], interest_number=project_details['interest_number'], data_of_interest=project_details['data_of_interest'])


# Social media search
@soeye.route('/twitter', methods=['POST'])
def twitter():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    twitter_posts = []
    form_data = request.form.to_dict()
    for i, post in enumerate(sntwitter.TwitterSearchScraper('from:'+form_data['username']).get_items()):
        if i>=int(form_data['number']):
            break
        post_data = [post.date, post.sourceLabel, post.likeCount, post.rawContent, post.media, post.links, 
        post.replyCount, post.retweetCount, post.quoteCount, post.retweetedTweet, post.quotedTweet, post.mentionedUsers]
        hash_value = hashlib.md5(json.dumps(post_data, sort_keys=True, default=str).encode('utf-8')).hexdigest()
        post_data.append(hash_value)
        twitter_posts.append(post_data)
    data = pd.DataFrame(twitter_posts, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks', 'Replies', 'Retweets', 
    'Quotes', 'Retweeted', 'Quoted', 'Tagged', 'hashValue'])
    data.to_html('static/html/'+timestamp+'_'+'twitter_posts_'+form_data['username']+'.html', index=False)
    return render_template('results.html', tables=[data.to_html(index=False)], titles=['']) 

@soeye.route('/reddit', methods=['POST'])
def reddit():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    reddit_submissions = []
    reddit_comments = []
    form_data = request.form.to_dict()
    for i, post in enumerate(snreddit.RedditUserScraper(form_data['username']).get_items()):
        if i>=int(form_data['number']):
            break
        if isinstance(post, snreddit.Submission):
            post_data = [post.date, post.url, post.subreddit, post.title, post.selftext, post.link]
            hash_value = hashlib.md5(json.dumps(post_data, sort_keys=True, default=str).encode('utf-8')).hexdigest()
            post_data.append(hash_value)
            reddit_submissions.append(post_data)
        elif isinstance(post, snreddit.Comment):
            post_data = [post.date, post.url, post.subreddit, post.body]
            hash_value = hashlib.md5(json.dumps(post_data, sort_keys=True, default=str).encode('utf-8')).hexdigest()
            post_data.append(hash_value)
            reddit_comments.append(post_data)

    data_submussions = pd.DataFrame(reddit_submissions, columns=['Date', 'Url', 'Subreddit', 'Title', 'Text', 'Media', 'hashValue'])
    data_submussions.to_html('static/html/'+timestamp+'_'+'reddit_submissions_'+form_data['username']+'.html', index=False)
    data_comments = pd.DataFrame(reddit_comments, columns=['Date', 'Url', 'Subreddit', 'Text', 'hashValue'])
    data_comments.to_html('static/html/'+timestamp+'_'+'reddit_comments_'+form_data['username']+'.html', index=False)
    return  render_template('results.html', tables=[data_submussions.to_html(index=False)], titles=['']) 

@soeye.route('/search_keyword', methods=['GET', 'POST'])
def search_keyword():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    form_data = request.form.to_dict()
    substring = form_data['keyword']
    data = pd.read_html('static/html/'+form_data['file_name'])
    df = data[0]
    mask = np.column_stack([df[col].astype(str).str.contains(substring.lower(), case=False, na=False) for col in df])
    df = df.loc[mask.any(axis=1)]
    if df.empty:
        return render_template('results.html', no_result='No results for this search.')
    else:
        df.to_html('static/html/'+timestamp+'_'+'keyword_'+form_data['keyword']+'.html', index=False)
        return render_template('results.html', tables=[df.to_html(index=False)], titles=[''])


# Evidence handling
@soeye.route('/add_evidence', methods=['GET', 'POST'])
def add_evidence():
    json_file = open('static/json/report.json')
    report = json.load(json_file)
    json_file.close()
    report['data_of_interest'].append(request.json)
    report['interest_number'] = len(report['data_of_interest'])
    with open('static/json/report.json', 'w') as f:
        json.dump(report, f, indent=4)
    return render_template('report.html', project_name=report['project_name'], project_number=report['project_number'],
    project_description=report['project_description'], interest_number=report['interest_number'], data_of_interest=report['data_of_interest'])

@soeye.route('/remove_evidence', methods=['GET', 'POST'])
def remove_evidence():
    json_file = open('static/json/report.json')
    report = json.load(json_file)
    json_file.close()
    data = str(request.data)
    data = data.replace("b", "")
    data = data.replace("'", "")
    i = int(data)
    del report['data_of_interest'][i]
    report['interest_number'] = len(report['data_of_interest'])
    with open('static/json/report.json', 'w') as f:
        json.dump(report, f, indent=4)
    return render_template('report.html', project_name=report['project_name'], project_number=report['project_number'],
    project_description=report['project_description'], interest_number=report['interest_number'], data_of_interest=report['data_of_interest'])


if __name__ == "__main__":
    soeye.run(debug=False)