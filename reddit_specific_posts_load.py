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

    # Cargando el archivo de configuraciones
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
      WHERE operadora = 'claro'
    '''

    # Realizando la extraccion de posts asociados a la operadora
    v_posts = v_reddit.get_posts_by_array(
      [
        '13wx55j','oh0gqc','10fhpwp','w49w4x','16bxxzf','17mcamt','10gh5sh','z9yxv6','15041z0','15b61u0',
        '16gakgu','iq8hs0','15ya1x2','16hvcw3','titnc5','x3aw2x','14hahmp','15fajdt','112purm','v1tmgv',
        '148te1o','sqxb7c','w7nh9t','u2uswx','rjesp8','w0mgpd','svyxpl','q1jvti','15rx31r','z259el',
        'zv0gae','zxfvc5','140ujfk'
      ]
      ,'claro'
    )
    print(v_posts)
    if len(v_posts) > 0:
      # Eliminando tabla de paso
      database.execute_query(QUERY_DELETE)

      # Insertando informacion a la base de datos
      database.insert_array(v_posts,QUERY_INSERT,10)

      # Ejecutando SP de carga de tabla fuente
      database.execute_store_procedure("sp_reddit_mo_bench_load_posts",['claro'])

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
