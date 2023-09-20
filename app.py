from reddit import Reddit
import json
import sys

def main():
  
  # Guardando nombre de la operadora
  mobile_operator=sys.argv[1]


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

  # Probando la extraccion de data del operadora
  v_reddit.get_post_by_mobile_operator(mobile_operator)

if __name__ == "__main__":
  main()