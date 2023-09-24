from reddit_praw import Reddit
import json
import sys
import datetime

def main():
  
  # Guardando nombre de la operadora
  mobile_operator=sys.argv[1]

  # Cargando el archivo de configuraciones
  with open('config.json', 'r') as archivo:
    # Carga el contenido del archivo JSON en una variable
    proyect_data = json.load(archivo)
    
  search_keyworks = next((item for item in proyect_data["search_keywords"] if item.get("operator") == mobile_operator), None)["keywords"]
  # Instanciando la clase de Reddit
  v_reddit = Reddit(
    proyect_data["reddit_api"]["client_id"],
    proyect_data["reddit_api"]["client_secret"],
    proyect_data["reddit_api"]["user_agent"],
    proyect_data["reddit_api"]["username"],
    proyect_data["reddit_api"]["password"]
  )

  # Probando la extraccion de data del operadora
  v_posts = v_reddit.get_all_post_by_mobile_operator(search_keyworks)

if __name__ == "__main__":
  main()