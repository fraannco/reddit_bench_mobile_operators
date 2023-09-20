import praw

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

  def get_post_by_mobile_operator(self,p_mobile_operator):
    v_subreddit=self.reddit.subreddit("PERU").search(p_mobile_operator,limit=100)
    for collection in v_subreddit:
        print(collection.title)