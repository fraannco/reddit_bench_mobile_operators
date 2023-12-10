
import pandas as pd
import unidecode
import datetime 
import json 

from database.postgres import PostgreSQL
from transform.transform import Transform

def main():
  try:
    
    fecha_inicio = datetime.datetime.now()

    operadoras = ["claro", "bitel", "entel", "movistar","wow","win"]

    # Cargando el archivo de configuraciones
    with open('config.json', 'r') as archivo:
      # Carga el contenido del archivo JSON en una variable
      proyect_data = json.load(archivo)

    QUERY_EXPORT = '''
      SELECT
        a.post_id,
        a.author post_author,
        b.comment_id,
        b.author comment_author,
        REPLACE(a.title, E'\\n', ' ') title,
        a.created_utc post_created_utc,
        a.link_flair_text,
        REPLACE(a.selftext, E'\\n', ' ') selftext,
        a.subreddit,
        a.upvote_ratio,
        REPLACE(b.body, E'\\n', ' ') comment,
        b.score comment_score,
        b.createc_utc comment_created_utc,
        CASE
          WHEN
            a.operadora IN ('claro','entel','movistar','win','wow','bitel')
          THEN a.operadora
          ELSE 'no_identificado'
        END operadora_busqueda
      FROM reddit_bmo_sq_posts a
      INNER JOIN reddit_bmo_sq_comments b
        ON a.post_id = b.post_id
      WHERE a.post_id  NOT IN (
        SELECT DISTINCT ep.post_id
        FROM reddit_mbo_sq_excluded_posts ep
      )
    '''
    # Instanciando la clase de base de datos
    database = PostgreSQL(
      proyect_data["postgres"]["database"],
      proyect_data["postgres"]["user"],
      proyect_data["postgres"]["password"],
      proyect_data["postgres"]["host"],
      proyect_data["postgres"]["port"]
    )

    transform = Transform('spanish',operadoras)

    v_data = database.get_query_results(QUERY_EXPORT)
    v_df = pd.DataFrame(
      v_data,
      columns = [
        "post_id", "post_author", "comment_id", "comment_author",
        "post_title", "post_created_utc", "link_flair_text", "selftext",
        "subreddit", "upvote_ratio", "comment", "comment_score",
        "comment_created_utc","operadora_busqueda",
      ]
    )

    print(v_df.head())

    # Aplicar la limpieza a las columnas 'post_title', 'selftext' y 'comment'
    v_df['post_title'] = v_df['post_title'].apply(transform.preprocess_text)
    v_df['selftext'] = v_df['selftext'].apply(transform.preprocess_text)
    v_df['link_flair_text'] = v_df['link_flair_text'].apply(transform.preprocess_text)
    print(v_df.head())

    # Aplicar la normalización a las columnas 'post_title', 'selftext' y 'comment'
    v_df['post_title'] = v_df['post_title'].apply(transform.normalize_text)
    v_df['selftext'] = v_df['selftext'].apply(transform.normalize_text)
    v_df['comment'] = v_df['comment'].apply(transform.normalize_text)
    v_df['link_flair_text'] = v_df['link_flair_text'].apply(transform.normalize_text)

    print(v_df.head())

    # Aplicar la función a cada fila
    v_df["menciones_operadoras"] = v_df.apply(lambda row: transform.contar_mencion_operadora(row["post_title"] + " " + row["selftext"] + " " + row["comment"],), axis=1)
    print(v_df["menciones_operadoras"])
    # Puedes convertir la lista de menciones en una cadena separada por comas si lo deseas

    v_df["menciones_operadoras"] = v_df["menciones_operadoras"].apply(lambda menciones: ', '.join(menciones) if menciones else None)
    
    v_df["menciones_operadoras"].fillna(v_df["operadora_busqueda"], inplace=True)

    # Dividiendo las filas por menciones de operadora
    expanded_df = v_df.assign(menciones_operadoras=v_df['menciones_operadoras'].str.split(', ')).explode('menciones_operadoras')
    expanded_df = expanded_df.drop(columns=["operadora_busqueda"])
    expanded_df = expanded_df.rename(columns={"menciones_operadoras": "operadora"})
    expanded_df['operadora'] = expanded_df['operadora'].replace('telefonica', 'movistar')
    
    expanded_df['mobile_operator_sentiment'] = expanded_df.apply(lambda row: transform.analyze_sentiment(row['comment'], row['operadora']), axis=1)

    expanded_df.to_csv('files/reddit_mobile_operators_peru_opinions9.csv', index=False)
    
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