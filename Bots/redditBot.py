import praw
import pandas as pd


class RedditBot():
    def __init__(self, keyword, data_number):
        self.keyword = keyword
        self.reddit = praw.Reddit(client_id='09VYFMBboiEEHDbMyDOTiQ',
                                  client_secret='6MNE-7Gygp4VWfAlj0Edbu_N1UDdMQ', user_agent='comments_extractor')
        self.data_number = data_number

    def run(self):
        posts = []
        comments = []
# subreddits=['antiwork','accenture','workreform','work','HumanResources','recruiting','remotework','talesfromtheoffice']
        subreddit = self.keyword
        sub = 0
        poste = 0

        ml_subreddit = self.reddit.subreddit(subreddit)
        sub += 1

        for post in ml_subreddit.hot(limit=10):
            posts.append([post.id,  post.url])
            poste += 1
            print("#########  "+str(poste)+"  post  #########")
        x = 0
        for i in posts:
            if x > self.data_number:
                print("Breaked at post Number : ", i)
                break
            submission = self.reddit.submission(id=i[0])
            submission.comments.replace_more(limit=10)
            for comment in submission.comments.list():
                if x < self.data_number:
                    comments.append([i[0], i[1], comment.body])
                    x += 1
                    print("#########  "+str(x)+"  comments  #########")
                else:
                    break
        df = pd.DataFrame(comments, columns=['post_id', 'post_url', 'comment'])
        return df
