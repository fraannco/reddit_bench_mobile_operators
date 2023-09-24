import praw
import datetime
import pandas as pd

class Reddit:
  def __init__(self,p_client_id,p_client_secret,p_user_agent,p_username,p_password):
    self.reddit = praw.Reddit(
      client_id=p_client_id,
      client_secret=p_client_secret,
      user_agent=p_user_agent,
      username=p_username,
      password=p_password
    )
    self.reddit.read_only = True

  def get_all_post_by_mobile_operator(self,p_search_keyworks):

    # Definiando cabeceras a extraer:
    headers = [
      'id', 'author', 'comments', 'title', 'created_utc', 'distinguished', 'edited', 'is_original_content',
      'is_self', 'link_flair_template_id', 'link_flair_text', 'locked', 'name', 'num_comments', 'over_18',
      'permalink', 'saved', 'score', 'selftext', 'spoiler', 'stickied', 'subreddit', 'upvote_ratio', 'url'
    ]
    #claro operadora experiencia opinion
    v_query = ' '.join(p_search_keyworks)
    cont=1
    v_subreddit=self.reddit.subreddit("PERU").search(query=v_query, limit=None,time_filter="year",sort="relevance")
    #df = pd.DataFrame([ vars(post) for post in v_subreddit ])
    #df_filter = df.filter(items=headers)
    #print(df_filter.describe())
    v_data = []
    for collection in v_subreddit:
      #if cont == 1 :
      v_data.append(
        [
          collection.id, collection.author, collection.title, collection.created_utc, collection.distinguished, collection.edited,
          collection.is_original_content, collection.is_self, collection.link_flair_template_id,
          collection.link_flair_text, collection.locked, collection.name, collection.num_comments, collection.over_18, collection.permalink,
          collection.saved, collection.score, collection.selftext, collection.spoiler, collection.stickied, collection.subreddit,
          collection.upvote_ratio, collection.url
        ]
      )
    #print(len(v_data))
    return v_data


























