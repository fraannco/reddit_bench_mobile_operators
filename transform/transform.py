import nltk
nltk.download('omw')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unidecode
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from langdetect import detect
import re 

class Transform:
  def __init__(self,p_stopwords_language,p_operadoras):
    # Stop words
    self.stop_words = stop_words = ['a','actualmente','adelante','además','afirmó','agregó','ahora','ahí','al','algo','alguna','algunas','alguno','algunos','algún','alrededor','ambos','ampleamos','ante','anterior','antes','apenas','aproximadamente','aquel','aquellas','aquellos','aqui','aquí','arriba','aseguró','así','atras','aunque','ayer','añadió','aún','bajo','bastante','bien','buen','buena','buenas','bueno','buenos','cada','casi','cerca','cierta','ciertas','cierto','ciertos','cinco','comentó','como','con','conocer','conseguimos','conseguir','considera','consideró','consigo','consigue','consiguen','consigues','contra','cosas','creo','cual','cuales','cualquier','cuando','cuanto','cuatro','cuenta','cómo','da','dado','dan','dar','de','debe','deben','debido','decir','dejó','del','demás','dentro','desde','después','dice','dicen','dicho','dieron','diferente','diferentes','dijeron','dijo','dio','donde','dos','durante','e','ejemplo','el','ella','ellas','ello','ellos','embargo','empleais','emplean','emplear','empleas','empleo','en','encima','encuentra','entonces','entre','era','erais','eramos','eran','eras','eres','es','esa','esas','ese','eso','esos','esta','estaba','estabais','estaban','estabas','estad','estada','estadas','estado','estados','estais','estamos','estan','estando','estar','estaremos','estará','estarán','estarás','estaré','estaréis','estaría','estaríais','estaríamos','estarían','estarías','estas','este','estemos','esto','estos','estoy','estuve','estuviera','estuvierais','estuvieran','estuvieras','estuvieron','estuviese','estuvieseis','estuviesen','estuvieses','estuvimos','estuviste','estuvisteis','estuviéramos','estuviésemos','estuvo','está','estábamos','estáis','están','estás','esté','estéis','estén','estés','ex','existe','existen','explicó','expresó','fin','fue','fuera','fuerais','fueran','fueras','fueron','fuese','fueseis','fuesen','fueses','fui','fuimos','fuiste','fuisteis','fuéramos','fuésemos','gran','grandes','gueno','ha','haber','habida','habidas','habido','habidos','habiendo','habremos','habrá','habrán','habrás','habré','habréis','habría','habríais','habríamos','habrían','habrías','habéis','había','habíais','habíamos','habían','habías','hace','haceis','hacemos','hacen','hacer','hacerlo','haces','hacia','haciendo','hago','han','has','hasta','hay','haya','hayamos','hayan','hayas','hayáis','he','hecho','hemos','hicieron','hizo','hoy','hube','hubiera','hubierais','hubieran','hubieras','hubieron','hubiese','hubieseis','hubiesen','hubieses','hubimos','hubiste','hubisteis','hubiéramos','hubiésemos','hubo','igual','incluso','indicó','informó','intenta','intentais','intentamos','intentan','intentar','intentas','intento','ir','junto','la','lado','largo','las','le','les','llegó','lleva','llevar','lo','los','luego','lugar','manera','manifestó','mayor','me','mediante','mejor','mencionó','menos','mi','mientras','mio','mis','misma','mismas','mismo','mismos','modo','momento','mucha','muchas','mucho','muchos','muy','más','mí','mía','mías','mío','míos','nada','nadie','ni','ninguna','ningunas','ninguno','ningunos','ningún','no','nos','nosotras','nosotros','nuestra','nuestras','nuestro','nuestros','nueva','nuevas','nuevo','nuevos','nunca','o','ocho','os','otra','otras','otro','otros','para','parece','parte','partir','pasada','pasado','pero','pesar','poca','pocas','poco','pocos','podeis','podemos','poder','podria','podriais','podriamos','podrian','podrias','podrá','podrán','podría','podrían','poner','por','por qué','porque','posible','primer','primera','primero','primeros','principalmente','propia','propias','propio','propios','próximo','próximos','pudo','pueda','puede','pueden','puedo','pues','que','quedó','queremos','quien','quienes','quiere','quién','qué','realizado','realizar','realizó','respecto','sabe','sabeis','sabemos','saben','saber','sabes','se','sea','seamos','sean','seas','segunda','segundo','según','seis','ser','seremos','será','serán','serás','seré','seréis','sería','seríais','seríamos','serían','serías','seáis','señaló','si','sido','siempre','siendo','siete','sigue','siguiente','sin','sino','sobre','sois','sola','solamente','solas','solo','solos','somos','son','soy','su','sus','suya','suyas','suyo','suyos','sí','sólo','tal','también','tampoco','tan','tanto','te','tendremos','tendrá','tendrán','tendrás','tendré','tendréis','tendría','tendríais','tendríamos','tendrían','tendrías','tened','teneis','tenemos','tener','tenga','tengamos','tengan','tengas','tengo','tengáis','tenida','tenidas','tenido','tenidos','teniendo','tenéis','tenía','teníais','teníamos','tenían','tenías','tercera','ti','tiempo','tiene','tienen','tienes','toda','todas','todavía','todo','todos','total','trabaja','trabajais','trabajamos','trabajan','trabajar','trabajas','trabajo','tras','trata','través','tres','tu','tus','tuve','tuviera','tuvierais','tuvieran','tuvieras','tuvieron','tuviese','tuvieseis','tuviesen','tuvieses','tuvimos','tuviste','tuvisteis','tuviéramos','tuviésemos','tuvo','tuya','tuyas','tuyo','tuyos','tú','ultimo','un','una','unas','uno','unos','usa','usais','usamos','usan','usar','usas','uso','usted','va','vais','valor','vamos','van','varias','varios','vaya','veces','ver','verdad','verdadera','VERDADERO','vez','vosotras','vosotros','voy','vuestra','vuestras','vuestro','vuestros','y','ya','yo','él','éramos','ésta','éstas','éste','éstos','última','últimas','último','últimos','sintiendo','sentido','sentida','sentidos','sentidas','siente','sentid',]#set(stopwords.words(p_stopwords_language))  

    # Operadoras
    self.operadoras = p_operadoras

    # Palabras positivas
    self.positive_keywords = ['bueno', 'excelente', 'mejor', 'buena', 'eficiente', 'rápido', 'satisfecho','estable','mejor','bueno','fibra óptica','funciona','bueno','recomendaria','bien','calidad','precio-calidad','recomendaría','personalmente','upvote','mejor','opciones','velocidad','ancho de banda','promoción','extra','funciona bien','aprovecho toda la velocidad','aguanta','promoción','mejor','simetrica','buena','verdad','nunca he tenido problemas','bueno','calidad de internet','servicio es bueno','buenas','satisfactorio','bueno','excelente','recomendaría','satisfecho','contento','óptimo','maravilloso','sin problemas','bueno','recomendaría','óptimo','mejor','ganado premios','excelente','rápido','buena señal','lo es todo','cobertura','top','satisfecho','genial','recomiendo que si','barato','suficiente','sin pensarlo','ganador','no lo pienses','no hay mas']
    
    # Palabras Negativas
    self.negative_keywords = ['malo', 'terrible', 'peor', 'mala', 'ineficiente', 'lento', 'insatisfecho','caído','estafa','kk','problemas','mala','amenos','no se que paso''problemas','lenta','reclamo','pesima','no lo vale','cambiate a','spam','peor','siglo antepasado','no parece mucha','no aprovecho toda la velocidad','cortaba por segundos','asquerosa','problemas','ridiculeces','no vale la pena','problemas','descontento','mala experiencia','quejas','no recomendaría','insatisfacción','malo','error','pobre','lento']
    
    # Palabras Neutrales
    self.neutral_keywords = ['depende', 'variable', 'medio', 'promedio', 'regular','hasta ahora','probablemente','diferencia','menor latencia','streaming','jugando','mobile','chateo','instagram','similar','competencia','dura','basico','ultima vez','distrito','region','rankea','informe','hizo','internet','región','cusco','hogar','móvil','movistar','claro','conexión','fija','tomaba','diferencia','nota','operadoras','ofrece','suscribes','plan de celular','contratar','actualmente','cableado','renovar','switches','routers','cables','tarjetas madres','adaptadores','pc','fibra óptica','migrar','servicio','hogar','problemas','central','ofrecido','zona','surco','alguien','cuenta','internet','televisión','teléfono fijo','respuesta','preguntas','recomienden','operador','cobertura','tal','aparte','edit','por favor','necesita','zona','hogar','personas','consumo mensual','amigo','familia','netflix','jugando en línea','llegan a los 2tb','familiar','busca instalar','adulto mayor','videollamadas','messenger','información','pregunta','datos','necesito ayuda','consulta','detalles','experiencia','comentario','opinión','sugerencia','información','pregunta','datos','consulta','detalles','experiencia','comentario','opinión','sugerencia','enrutamiento']

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

  def normalize_text(self,text):
    if text is None:
        text = ''
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
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
    if operator.lower() in comment.lower():
      tokens = [word for word in word_tokenize(comment.lower()) if word.isalpha() and word not in self.stop_words]
      def is_near_operator(keyword):
          return any(keyword in tokens[i:i + 3] for i in range(len(tokens)))
      if any(is_near_operator(word) for word in self.positive_keywords):
          return 'positivo'
      elif any(is_near_operator(word) for word in self.negative_keywords):
          return 'negativo'
      elif any(is_near_operator(word) for word in self.neutral_keywords):
          return 'neutro'
      else:
          return 'no_definido'
    else:
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
    
  def is_english(self,text):
      try:
          return detect(text) == 'en'
      except:
          return False