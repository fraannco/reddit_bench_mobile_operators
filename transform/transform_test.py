import unittest

from transform import Transform

class TestTransformMethods(unittest.TestCase):

    def setUp(self):
        # Common setup for tests
        stop_words_language = 'spanish'
        operadoras = ['movistar', 'claro', 'entel']
        self.transformer = Transform(stop_words_language, operadoras)

    def test_normalize_text_with_special_characters(self):
        input_text = "¡Este es un Texto de PRUEBA con Caracteres Especiales y Ácéntös!"
        expected_output = "este es un texto de prueba con caracteres especiales y acentos"
        self.assertEqual(self.transformer.normalize_text(input_text), expected_output)

    def test_preprocess_text_with_stopwords_and_special_characters(self):
        input_text = "Hola, esto es una prueba de limpieza de texto. Aquí hay algunas stopwords y números 123."
        expected_output = "hola prueba limpieza texto stopwords números"
        self.assertEqual(self.transformer.preprocess_text(input_text), expected_output)

    def test_contar_mencion_operadora_case_insensitive(self):
        input_text = "Me gusta el servicio de MOVISTAR, pero la señal de Claro no es buena."
        expected_output = ['movistar', 'claro']
        self.assertEqual(self.transformer.contar_mencion_operadora(input_text), expected_output)

    def test_etiquetado_de_palabras_with_multiple_occurrences(self):
        input_text = "El servicio de Movistar es bueno, pero Claro tiene problemas. Movistar también es bueno."
        expected_output = "El servicio de Mención de Operadora: Movistar es bueno , pero Mención de Operadora: Claro tiene problemas . Mención de Operadora: Movistar también es bueno ."
        self.assertEqual(self.transformer.etiquetado_de_palabras(input_text), expected_output)

    def test_analyze_sentiment_with_operator_near_positive_keyword(self):
        comment = "Movistar tiene un servicio excelente y rápido."
        operator = "movistar"
        expected_output = 0 
        self.assertEqual(self.transformer.analyze_sentiment(comment, operator), expected_output)

    def test_analyze_sentiment_with_operator_near_negative_keyword(self):
        comment = "Movistar tiene un servicio terrible y lento."
        operator = "movistar"
        expected_output = 1 
        self.assertEqual(self.transformer.analyze_sentiment(comment, operator), expected_output)

    def test_analyze_sentiment_with_operator_near_neutral_keyword(self):
        comment = "Movistar tiene un servicio que depende del área."
        operator = "movistar"
        expected_output = 2
        self.assertEqual(self.transformer.analyze_sentiment(comment, operator), expected_output)

    def test_analyze_sentiment_for_text_with_negative_keyword(self):
        text = "El servicio de Movistar es muy lento y poco confiable."
        expected_output = 1 
        self.assertEqual(self.transformer.analyze_sentiment_for_text(text), expected_output)

    def test_is_english_with_english_text(self):
        english_text = "This is an English sentence."
        self.assertTrue(self.transformer.is_english(english_text))

    def test_is_english_with_spanish_text(self):
        spanish_text = "Esto es una oración en español."
        self.assertFalse(self.transformer.is_english(spanish_text))

if __name__ == '__main__':
    unittest.main()