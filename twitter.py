import snscrape.modules.twitter as sntwitter
import pandas as pd

# List to append all data to
data_container = []

# User input
username_to_investigate = input('Enter the username you wish to investigate: ')
number_of_posts_to_investigate = int(input('Enter the number of posts you wish to investigate:'))

# Scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+username_to_investigate).get_items()):
    if i>number_of_posts_to_investigate:
        break
    data_container.append([tweet.date, tweet.sourceLabel, tweet.likeCount, tweet.rawContent, tweet.media, tweet.outlinks, tweet.replyCount, 
    tweet.retweetCount, tweet.quoteCount, tweet.retweetedTweet, tweet.quotedTweet, tweet.mentionedUsers])
    
# Create dataframe from the tweets list and save it to a csv file
tweets_df = pd.DataFrame(data_container, columns=['Date', 'Source', 'Likes', 'Tweet', 'Media', 'Outlinks',
'Replies', 'Retweets', 'Quotes', 'Retweeted', 'Quoted', 'Tagged'])
tweets_df.to_csv('raw_data.csv', index=False)