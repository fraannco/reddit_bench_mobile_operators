from extract.reddit_praw import Reddit
import json
import sys
import datetime

from database.postgres import PostgreSQL

def main():
  try:
    # Fecha inicio
    fecha_inicio = datetime.datetime.now()
    
    with open('config.json', 'r') as archivo:
      # Carga el contenido del archivo JSON en una variable
      proyect_data = json.load(archivo)

    # Instanciando la clase de Reddit
    v_reddit = Reddit(
      proyect_data["reddit_api"]["client_id"],
      proyect_data["reddit_api"]["client_secret"],
      proyect_data["reddit_api"]["user_agent"],
      proyect_data["reddit_api"]["username"],
      proyect_data["reddit_api"]["password"]
    )

    # Instanciando la clase de base de datos
    database = PostgreSQL(
      proyect_data["postgres"]["database"],
      proyect_data["postgres"]["user"],
      proyect_data["postgres"]["password"],
      proyect_data["postgres"]["host"],
      proyect_data["postgres"]["port"]
    )

    QUERY_GET_POSTS = '''
      SELECT DISTINCT post_id
      FROM REDDIT_BMO_SQ_POSTS a
      WHERE a.post_id NOT IN (
        SELECT DISTINCT cmmts.post_id
        FROM reddit_bmo_sq_comments cmmts
      )
  '''
    QUERY_INSERT = '''
      INSERT INTO reddit_bmo_sq_comments(
        post_id,
        comment_id,
        author,
        body,
        createc_utc,
        edited,
        score,
        subreddit_id,
        fecha_insercion
      )
      VALUES(
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        NOW()
      )
    '''

    v_posts = database.get_query_results(QUERY_GET_POSTS)

    # Ahora puedes trabajar con los resultados en 'results'
    v_comments = v_reddit.get_all_comments_of_post(v_posts)
    
    database.insert_array(v_comments,QUERY_INSERT,1000)

    # Fecha fin
    fecha_fin = datetime.datetime.now()
    
    print(f'[Fecha inicio]: {fecha_inicio} | [Fecha fin]: {fecha_fin}')
  except Exception as e:
    # Fecha fin
    fecha_fin = datetime.datetime.now()

    print(f'Problemas en Benchmarking Mobile Operators {e}')
    print(f'[Fecha inicio]: {fecha_inicio} | [Fecha fin]: {fecha_fin}')

if __name__ == "__main__":
  main()