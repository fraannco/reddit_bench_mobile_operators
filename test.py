import praw
import json

# Abre el archivo JSON
with open('config.json', 'r') as archivo:
  # Carga el contenido del archivo JSON en una variable
  proyect_data = json.load(archivo)

reddit = praw.Reddit(
  client_id=proyect_data["reddit_api"]["client_id"],
  client_secret=proyect_data["reddit_api"]["client_secret"],
  user_agent=proyect_data["reddit_api"]["user_agent"],
  username=proyect_data["reddit_api"]["username"],
  password=proyect_data["reddit_api"]["password"]
)

# Enable read-only mode
reddit.read_only = True


#subreddit = reddit.subreddit("PERU").hot()
subreddit=reddit.subreddit("PERU").search("bitel")

for collection in subreddit:
    print(collection.title)