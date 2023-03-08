import praw
import pandas as pd

LEFT_SUBREDDITS = ['ShitLiberalsSay', 'LateStageGenderBinary', 'RadicalQueers', 'GenderQueer', 'LateStageCapitalism', 'LateStageColonialism']

reddit_authorized = praw.Reddit(client_id="nJb1PxPT5tJCDDNlQ4BBcg",
                                client_secret="dCU5OB0iCJRfMynkkG-5HE3CFcUqyQ",
                                user_agent="Green-Mud1928",
                                username="Green-Mud1928",
                                password="pooploop123")

i = 0

for sub in LEFT_SUBREDDITS:
    sr_obj = reddit_authorized.subreddit(sub)

    posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": [],
              "Post Comments": []
              }
    print(sub)
    tot_comments = 0
    tot_posts = 0
    for post in sr_obj.hot(limit=1000):
        tot_posts += 1
        # Title of each post
        posts_dict["Title"].append(post.title)
        # Text inside a post
        posts_dict["Post Text"].append(post.selftext)
        # Unique ID of each post
        posts_dict["ID"].append(post.id)
        # The score of a post
        posts_dict["Score"].append(post.score)
        # Total number of comments inside the post
        posts_dict["Total Comments"].append(post.num_comments)
        tot_comments += post.num_comments
        # URL of each post
        posts_dict["Post URL"].append(post.url)
        comments_vec = []
        post.comments.replace_more(limit=20)
        for comment in post.comments:
            if type(comment) == 'MoreComments':
                continue
            comments_vec.append(comment.body)
        # print(len(comments_vec))
        posts_dict["Post Comments"].append(comments_vec)
    # Saving the data in a pandas dataframe
    top_posts = pd.DataFrame(posts_dict)
    print(tot_posts)
    print(tot_comments)
    name = sub + '.csv'
    top_posts.to_csv(name, index=True)

    i+=1


