import praw
import pandas as pd

LEFT_SUBREDDITS = ['ShitLiberalsSay', 'LateStageGenderBinary', 'RadicalQueers', 'GenderQueer', 'LateStageCapitalism', 'LateStageColonialism']

reddit_authorized = praw.Reddit(client_id="--",
                                client_secret="--",
                                user_agent="--",
                                username="--",
                                password="--")

i = 0

# code commented out for author collection

authors = set()
for sub in LEFT_SUBREDDITS:
    sr_obj = reddit_authorized.subreddit(sub)

    # posts_dict = {"Title": [], "Post Text": [],
    #           "ID": [], "Score": [],
    #           "Total Comments": [], "Post URL": [],
    #           "Post Comments": []
    #           }
    print(sub)
    # tot_comments = 0
    # tot_posts = 0
    for post in sr_obj.hot(limit=500): # change limit from 1k to 500
        # tot_posts += 1
        # # Title of each post
        # posts_dict["Title"].append(post.title)
        # # Text inside a post
        # posts_dict["Post Text"].append(post.selftext)
        # # Unique ID of each post
        # posts_dict["ID"].append(post.id)
        # # The score of a post
        # posts_dict["Score"].append(post.score)
        # # Total number of comments inside the post
        # posts_dict["Total Comments"].append(post.num_comments)
        # tot_comments += post.num_comments
        # # URL of each post
        # posts_dict["Post URL"].append(post.url)
        # comments_vec = []
        # post.comments.replace_more(limit=20)
        authors.add(post.author)
        for comment in post.comments:
            if str(type(comment)) == 'MoreComments':
                continue
            # comments_vec.append(comment.body)
            try:
                authors.add(comment.author)
            except:
                continue
        # print(len(comments_vec))
        # posts_dict["Post Comments"].append(comments_vec)
    # Saving the data in a pandas dataframe
    # top_posts = pd.DataFrame(posts_dict)
    # print(tot_posts)
    # print(tot_comments)
    # name = sub + '.csv'
    # top_posts.to_csv(name, index=True)
    i+=1

all_authors = pd.DataFrame(authors)
all_authors.to_csv('leftwing_users.csv', index=True)



