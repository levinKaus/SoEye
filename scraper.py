import snscrape.modules.reddit as snreddit
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Lists to append data to
reddit_submissions = []
reddit_comments = []
twitter_posts = []

# Reddit search
def reddit(username):
    for i, post in enumerate(snreddit.RedditUserScraper(username).get_items()):
        if i>number_of_posts_to_investigate:
            break
        if isinstance(post, snreddit.Submission):
            reddit_submissions.append([post.date, post.url, post.subreddit, post.title, post.selftext, post.link])
        elif isinstance(post, snreddit.Comment):
            reddit_comments.append([post.date, post.url, post.subreddit, post.body])

    pd.DataFrame(reddit_submissions, columns=['Date', 'Url', 'Subreddit', 'Title', 'Text', 'Media']).to_csv('reddit_submissions.csv', index=False)
    pd.DataFrame(reddit_comments, columns=['Date', 'Url', 'Subreddit', 'Text',]).to_csv('reddit_comments.csv', index=False)

# Twitter search
def twitter(username):
    for i, post in enumerate(sntwitter.TwitterSearchScraper('from:'+username).get_items()):
        if i>number_of_posts_to_investigate:
            break
        print(type(post))
        twitter_posts.append([post.date, post.sourceLabel, post.likeCount, post.rawContent, post.media, post.links, post.replyCount, 
        post.retweetCount, post.quoteCount, post.retweetedTweet, post.quotedTweet, post.mentionedUsers])
    pd.DataFrame(twitter_posts, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks', 
    'Replies', 'Retweets', 'Quotes', 'Retweeted', 'Quoted', 'Tagged']).to_csv('twitter_posts.csv', index=False)   


# User inputs
username_reddit = input('Reddit username (Leave blank for not searching reddit): ')
username_twitter = input('Twitter username (Leave blank for not searching twitter): ')
number_of_posts_to_investigate = int(input('Number of posts you wish to investigate:'))

# Function calls
if username_reddit:
    reddit(username_reddit)
if username_twitter:
    twitter(username_twitter)