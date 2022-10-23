import snscrape.modules.twitter as sntwitter
import pandas as pd


class TwitterBot:
    def __init__(self, keyword, data_number):
        # search_keywords=['Head of learning ','director of learning','Head employee experience','director of employee experience','Head of people',' director of people','chief HR officer','chief learning officer']
        self.search_keyword = keyword
        self.data_number = data_number

    def run(self):
        # Creating list to append tweet data to
        tweets_list2 = []
        k = 0
        j = 0
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(self.search_keyword).get_items()):
            if i > self.data_number:
                break
            j = j+1
            tweets_list2.append([tweet.id, tweet.content])

        # Creating a dataframe from the tweets list above
        tweets_df2 = pd.DataFrame(tweets_list2, columns=[
                                  'Tweet Id', 'comment'])
        return tweets_df2
