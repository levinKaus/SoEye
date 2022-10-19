import snscrape.modules.reddit as snreddit
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os

# Lists to append data to
reddit_submissions = []
reddit_comments = []
twitter_posts = []

# paths
current_directory, project_path, content_view_path, search_results_path, report_path = '', '', '', '', ''

# Reddit search
def reddit(username):
    for i, post in enumerate(snreddit.RedditUserScraper(username).get_items()):
        if i>number_of_posts_to_investigate:
            break
        if isinstance(post, snreddit.Submission):
            reddit_submissions.append([post.date, post.url, post.subreddit, post.title, post.selftext, post.link])
        elif isinstance(post, snreddit.Comment):
            reddit_comments.append([post.date, post.url, post.subreddit, post.body])

    pd.DataFrame(reddit_submissions, columns=['Date', 'Url', 'Subreddit', 'Title', 'Text', 'Media']).to_csv(os.path.join(content_view_path, 'reddit_submissions.csv'), index=False)
    pd.DataFrame(reddit_comments, columns=['Date', 'Url', 'Subreddit', 'Text',]).to_csv(os.path.join(content_view_path, 'reddit_comments.csv'), index=False)

# Twitter search
def twitter(username):
    for i, post in enumerate(sntwitter.TwitterSearchScraper('from:'+username).get_items()):
        if i>number_of_posts_to_investigate:
            break
        twitter_posts.append([post.date, post.sourceLabel, post.likeCount, post.rawContent, post.media, post.links, post.replyCount, 
        post.retweetCount, post.quoteCount, post.retweetedTweet, post.quotedTweet, post.mentionedUsers])
    pd.DataFrame(twitter_posts, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks', 
    'Replies', 'Retweets', 'Quotes', 'Retweeted', 'Quoted', 'Tagged']).to_csv(os.path.join(content_view_path, 'twitter_posts.csv'), index=False)   

# Creates initial folders and files for the investigation project
def create_project(number, file_name, description):
    global current_directory, project_path, content_view_path, search_results_path, report_path
    current_directory = os.getcwd()
    project_path = os.path.join(current_directory, 'project - '+file_name)
    content_view_path = os.path.join(project_path, 'Content View')
    search_results_path = os.path.join(project_path, 'Search Results')
    report_path = os.path.join(project_path, 'Report.html')
    os.makedirs(project_path)
    os.mkdir(content_view_path)
    os.mkdir(search_results_path)
    report_file = open(report_path, 'a')
    report_file.write('<html><head><title>'+file_name+'</title></head><body><p><b><u style="color:red">Evidence Report for Project:</u></b> '+
    file_name + '</p><p><b style="color:blue">Project Number: </b>'+ str(number) +'</p><p><b style="color:blue">Project Description:</b> ' +
    description + '</p><p><b style="color:blue">Evidence of Interest:</b></p><p>Toal Evidence Items of Interest: 0</p></body></html>')
    report_file.close()
    
# User inputs
project_number = input('Project number: ')
project_file_name = input('Project file name: ')
project_description = input('Project description: ')
create_project(project_number, project_file_name, project_description)

username_reddit = input('Reddit username (Leave blank for not searching reddit): ')
username_twitter = input('Twitter username (Leave blank for not searching twitter): ')
number_of_posts_to_investigate = int(input('Number of posts you wish to investigate: '))

# Function calls
if username_reddit:
    reddit(username_reddit)
if username_twitter:
    twitter(username_twitter)