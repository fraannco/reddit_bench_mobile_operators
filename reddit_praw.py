import praw
import datetime

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

    #claro operadora experiencia opinion
    v_query = ' '.join(p_search_keyworks)
    cont=1
    v_subreddit=self.reddit.subreddit("PERU").search(query=v_query, limit=None,time_filter="week",sort="relevance")
    
    for collection in v_subreddit:
      print(
        '[',cont,'] -> author:', #collection.author,' | ',
        #'comments:', collection.comments,' | ',
        'title:', collection.title,' | '#,
        #'created_utc:', collection.created_utc,' | ',
        #'distinguished:', collection.distinguished,' | ',
        #'edited:', collection.edited,' | ',
        #'id:', collection.id,' | ',
        #'is_original_content:', collection.is_original_content,' | ',
        #'is_self:', collection.is_self,' | ',
        #'link_flair_template_id:', collection.link_flair_template_id,' | ',
        #'link_flair_text:', collection.link_flair_text,' | ',
        #'locked:', collection.locked,' | ',
        #'name:', collection.name,' | ',
        'num_comments:', collection.num_comments,' | ',
        #'over_18:', collection.over_18,' | ',
        #'permalink:', collection.permalink,' | ',
        ##'poll_data:', collection.poll_data,' | ',
        #'saved:', collection.saved,' | ',
        #'score:', collection.score,' | ',
        #'selftext:', collection.selftext,' | ',
        #'spoiler:', collection.spoiler,' | ',
        #'stickied:', collection.stickied,' | ',
        #'subreddit:', collection.subreddit,' | ',
        #'title:', collection.title,' | ',
        #'upvote_ratio:', collection.upvote_ratio,' | ',
        #'url:', collection.url
      )
      cont=cont+1


























