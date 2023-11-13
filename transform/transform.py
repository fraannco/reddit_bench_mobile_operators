import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unidecode

class Transform:
  def __init__(self,p_stopwords_language,p_operadoras):
    self.stop_words = set(stopwords.words(p_stopwords_language))  
    self.operadoras = p_operadoras

  # Crear una función para realizar la limpieza de texto
  def preprocess_text(self,text):
    try:
      # Convertir a minúsculas
      if text is None:
          text = ''
      text = text.lower()
      
      # Tokenización
      tokens = word_tokenize(text)
      
      # Eliminar stopwords y caracteres especiales
      filtered_tokens = [word for word in tokens if word not in self.stop_words and word.isalpha()]
      
      # Unir las palabras procesadas de nuevo en texto
      cleaned_text = ' '.join(filtered_tokens)
      
      return cleaned_text
    except Exception as e:
      raise Exception (f'Transform.preprocess_text: {e}')

  # Crear una función para la normalización de texto
  def normalize_text(self,text):
    # Convierte el texto a minúsculas
    if text is None:
        text = ''
    text = text.lower()
    # Elimina acentos y caracteres especiales
    text = unidecode.unidecode(text)
    # Puedes agregar más pasos de normalización si es necesario, como eliminar símbolos

    return text
  
  def contar_mencion_operadora(self,p_texto):
    menciones = [operadora for operadora in self.operadoras if operadora.lower() in p_texto.lower()]
    return menciones

  def etiquetado_de_palabras(self, text):
      # Tokenización
      tokens = word_tokenize(text)
      
      # Etiquetar palabras que son menciones de operadoras
      etiquetas = []
      for word in tokens:
          if word.lower() in [operadora.lower() for operadora in self.operadoras]:
              etiquetas.append(f"Mención de Operadora: {word}")
          else:
              etiquetas.append(word)

      # Unir las palabras procesadas de nuevo en texto
      etiquetado_text = ' '.join(etiquetas)

      return etiquetado_text