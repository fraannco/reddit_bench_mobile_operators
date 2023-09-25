from extract.reddit_praw import Reddit
import json
import sys
import datetime

from database.postgres import PostgreSQL

def main():
  try:
    # Fecha inicio
    fecha_inicio = datetime.datetime.now()

    # Guardando nombre de la operadora
    mobile_operator=sys.argv[1]
    granularity=sys.argv[2]

    # Cargando el archivo de configuraciones
    with open('config.json', 'r') as archivo:
      # Carga el contenido del archivo JSON en una variable
      proyect_data = json.load(archivo)
    
    # Buscando la cadena de busqueda en el proyecto
    search_keyworks = next((item for item in proyect_data["search_keywords"] if item.get("operator") == mobile_operator), None)["keywords"]

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

    QUERY_INSERT = '''
      INSERT INTO TP_REDDIT_PERU_POST_MOBILE_OPERATORS(
        operadora,
        post_id,
        author,
        title,
        created_utc,
        distinguished,
        edited,
        is_original_content,
        is_self,
        link_flair_text,
        locked,
        name,
        num_comments,
        over_18,
        permalink,
        saved,
        score,
        selftext,
        spoiler,
        stickied,
        subreddit,
        upvote_ratio,
        url
      ) VALUES(
        %s,
        %s,
        %s,
        %s,
        TO_TIMESTAMP(%s,'YYYY-MM-DD HH24:MI:SS'),
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
      )
    '''
    QUERY_DELETE = f'''
      DELETE FROM TP_REDDIT_PERU_POST_MOBILE_OPERATORS
      WHERE operadora = '{mobile_operator}'
    '''

    # Realizando la extraccion de posts asociados a la operadora
    v_posts = v_reddit.get_all_post_by_mobile_operator(search_keyworks,mobile_operator,granularity)
    if len(v_posts) > 0:
      # Eliminando tabla de paso
      database.execute_query(QUERY_DELETE)

      # Insertando informacion a la base de datos
      database.insert_array(v_posts,QUERY_INSERT)

      # Ejecutando SP de carga de tabla fuente
      database.execute_store_procedure("sp_reddit_mo_bench_load_posts",[mobile_operator])

      # Finalizando la conexion a postgres
      database.connection.close()

      # Fecha fin
      fecha_fin = datetime.datetime.now()

      print(f'Se finalizo la carga de posts correctamente | [Fecha inicio]: {fecha_inicio} | [Fecha fin]: {fecha_fin}')
    else:
      # Fecha fin
      fecha_fin = datetime.datetime.now()
      print(f'No se encontraron datos | [Fecha inicio]: {fecha_inicio} | [Fecha fin]: {fecha_fin}')
  except Exception as e:
    # Fecha fin
    fecha_fin = datetime.datetime.now()

    print(f'Problemas en Benchmarking Mobile Operators {e}')
    print(f'[Fecha inicio]: {fecha_inicio} | [Fecha fin]: {fecha_fin}')

if __name__ == "__main__":
  main()
