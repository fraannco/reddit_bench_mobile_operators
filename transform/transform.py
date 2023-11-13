import nltk
nltk.download('omw')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unidecode
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

class Transform:
  def __init__(self,p_stopwords_language,p_operadoras):
    # Stop words
    self.stop_words = set(stopwords.words(p_stopwords_language))  

    # Operadoras
    self.operadoras = p_operadoras

    # Palabras positivas
    self.positive_keywords = [
      'bueno', 'excelente', 'mejor', 'buena', 'eficiente', 'rápido', 'satisfecho',
      'estable','mejor','bueno','fibra óptica','funciona',
'bueno',
'recomendaria',
'bien',
'calidad',
'precio-calidad',
'recomendaría',
'personalmente',
'upvote',
'mejor',
'opciones',
'velocidad',
'ancho de banda',
'promoción',
'extra',
'funciona bien',
'aprovecho toda la velocidad',
'aguanta',
'promoción',
'mejor',
'simetrica',
'buena',
'verdad',
'nunca he tenido problemas',
'bueno',
'calidad de internet',
'servicio es bueno',
'buenas',
'satisfactorio',
'bueno',
'excelente',
'recomendaría',
'satisfecho',
'contento',
'óptimo',
'maravilloso',
'sin problemas',
'bueno',
'recomendaría',
'óptimo',
'mejor',
'ganado premios',
'excelente',
'rápido',
'buena señal','lo es todo',
'cobertura','top',
'satisfecho','genial','recomiendo que si','barato','suficiente','sin pensarlo','ganador','no lo pienses','no hay mas'
    ]
    self.negative_keywords = [
      'malo', 'terrible', 'peor', 'mala', 'ineficiente', 'lento', 'insatisfecho','caído','estafa','kk','problemas',
'mala','amenos','no se que paso'
'problemas',
'lenta','reclamo',
'pesima',
'no lo vale','cambiate a','spam',
'peor',
'siglo antepasado',
'no parece mucha',
'no aprovecho toda la velocidad',
'cortaba por segundos',
'asquerosa',
'problemas',
'ridiculeces',
'no vale la pena',
'problemas',
'descontento',
'mala experiencia',
'quejas',
'no recomendaría',
'insatisfacción',
'malo',
'error',
'pobre',
'lento'
    ]
    self.neutral_keywords = ['depende', 'variable', 'medio', 'promedio', 'regular','hasta ahora',
'probablemente',
'diferencia',
'menor latencia',
'streaming',
'jugando',
'mobile',
'chateo',
'instagram',
'similar',
'competencia',
'dura',
'basico',
'ultima vez',
'distrito',
'region',
'rankea',
'informe',
'hizo',
'internet',
'región',
'cusco',
'hogar',
'móvil',
'movistar',
'claro',
'conexión',
'fija',
'tomaba',
'diferencia',
'nota',
'operadoras',
'ofrece',
'suscribes',
'plan de celular',
'contratar',
'actualmente',
'cableado',
'renovar',
'switches',
'routers',
'cables',
'tarjetas madres',
'adaptadores',
'pc',
'fibra óptica',
'migrar',
'servicio',
'hogar',
'problemas',
'central',
'ofrecido',
'zona',
'surco',
'alguien',
'cuenta',
'internet',
'televisión',
'teléfono fijo',
'respuesta',
'preguntas',
'recomienden',
'operador',
'cobertura',
'tal',
'aparte',
'edit',
'por favor',
'necesita',
'zona',
'hogar',
'personas',
'consumo mensual',
'amigo',
'familia',
'netflix',
'jugando en línea',
'llegan a los 2tb',
'familiar',
'busca instalar',
'adulto mayor',
'videollamadas',
'messenger',
'información',
'pregunta',
'datos',
'necesito ayuda',
'consulta',
'detalles',
'experiencia',
'comentario',
'opinión',
'sugerencia',
'información',
'pregunta',
'datos',
'consulta',
'detalles',
'experiencia',
'comentario',
'opinión',
'sugerencia',
'enrutamiento']

  def __load_lexicon__(self, lexicon_name):
    synsets = wn.synsets(lexicon_name, lang='spa')
    lexicon = set()
    for synset in synsets:
        for lemma in synset.lemma_names('spa'):
            lexicon.add(lemma.lower())
    return lexicon

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
  
  def analyze_sentiment(self, comment, operator):
    # Verificar si el operador está presente en el comentario
    if operator.lower() in comment.lower():
      # Tokenizar el comentario y eliminar palabras de parada
      tokens = [word for word in word_tokenize(comment.lower()) if word.isalpha() and word not in self.stop_words]

      # Verificar la cercanía de las palabras clave al operador
      def is_near_operator(keyword):
          return any(keyword in tokens[i:i + 3] for i in range(len(tokens)))

      # Asignar el sentimiento basado en la presencia de palabras clave y operadora
      if any(is_near_operator(word) for word in self.positive_keywords):
          return 'positivo'
      elif any(is_near_operator(word) for word in self.negative_keywords):
          return 'negativo'
      elif any(is_near_operator(word) for word in self.neutral_keywords):
          return 'neutro'
      else:
          return 'no_definido'
    else:
        # Realizar el análisis de sentimiento en base a todo el comentario
        overall_sentiment = self.analyze_sentiment_for_text(comment)
        return overall_sentiment

  def analyze_sentiment_for_text(self, text):
    if any(keyword in text.lower() for keyword in self.positive_keywords):
        return 'positivo'
    elif any(keyword in text.lower() for keyword in self.negative_keywords):
        return 'negativo'
    elif any(keyword in text.lower() for keyword in self.neutral_keywords):
        return 'neutro'
    else:
        return 'no_definido'
    
