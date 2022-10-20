import snscrape.modules.reddit as snreddit
import snscrape.modules.twitter as sntwitter
import pandas as pd
import typer
import os

app = typer.Typer()

# Reddit search
@app.command()
def reddit(username: str, post_number: int):
    reddit_submissions = []
    reddit_comments = []
    for i, post in enumerate(snreddit.RedditUserScraper(username).get_items()):
        if i>=post_number:
            break
        if isinstance(post, snreddit.Submission):
            reddit_submissions.append([post.date, post.url, post.subreddit, post.title, post.selftext, post.link])
        elif isinstance(post, snreddit.Comment):
            reddit_comments.append([post.date, post.url, post.subreddit, post.body])

    pd.DataFrame(reddit_submissions, columns=['Date', 'Url', 'Subreddit', 'Title', 'Text', 'Media']).to_csv('SoEye Project/Content View/reddit_submissions.csv', index=False)
    pd.DataFrame(reddit_comments, columns=['Date', 'Url', 'Subreddit', 'Text',]).to_csv('SoEye Project/Content View/reddit_comments.csv', index=False)

# Twitter search
@app.command()
def twitter(username: str, post_number: int):
    twitter_posts = []
    for i, post in enumerate(sntwitter.TwitterSearchScraper('from:'+username).get_items()):
        if i>=post_number:
            break
        twitter_posts.append([post.date, post.sourceLabel, post.likeCount, post.rawContent, post.media, post.links, post.replyCount, 
        post.retweetCount, post.quoteCount, post.retweetedTweet, post.quotedTweet, post.mentionedUsers])
    pd.DataFrame(twitter_posts, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks', 
    'Replies', 'Retweets', 'Quotes', 'Retweeted', 'Quoted', 'Tagged']).to_csv(os.path.join('SoEye Project/Content View/twitter_posts.csv'), index=False)   

# Creates initial folders and files for the investigation project
@app.command()
def init(number: int, file_name: str, description: str):
    global current_directory, project_path, content_view_path, search_results_path, report_path
    current_directory = os.getcwd()
    project_path = os.path.join(current_directory, 'SoEye Project')
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

if __name__ == "__main__":
    app()