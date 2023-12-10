# DataFrame
import pandas as pd

# Matplot
import matplotlib.pyplot as plt

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer

# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Embedding, Flatten, Conv1D, MaxPooling1D, LSTM
from keras import utils
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

# nltk
import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer

# Word2vec
import gensim

# Utility
import re
import numpy as np
import os
from collections import Counter
import logging
import time
import pickle
import itertools

# Set log
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


df = pd.read_csv('../files/analyzed_comments_sentiment.csv', header=0)
df = df.dropna(subset=['comment'])

print("Tamaño del dataset:  ", len(df))

# DATASET
TRAIN_SIZE = 0.9

# TEXT CLENAING
TEXT_CLEANING_RE = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

stemmer = SnowballStemmer("spanish")


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            #tokens.append(token)
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                if token == 'tan': tokens.append(token)
    return " ".join(tokens)

df['comments_preprocess'] = df.comment.apply(lambda x: preprocess(x))

df_train, df_test = train_test_split(df, test_size=1-TRAIN_SIZE, random_state=42)
print("TRAIN size:", len(df_train))
print("TEST size:", len(df_test))

# Asigna df_train.txt a 'documentos'
documentos = df_train.comments_preprocess

# Elimina los duplicados
documentos.drop_duplicates(inplace=True)

# Aplica 'split' a cada documento
documentos = [texto.split() for texto in documentos]


## WORD2VEC 
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 100
W2V_MIN_COUNT = 10

import multiprocessing

hhgroups2vec = gensim.models.word2vec.Word2Vec(
    documentos,
    sg=1,
    seed=1,
    workers=multiprocessing.cpu_count(),
    vector_size=W2V_SIZE,
    min_count=W2V_MIN_COUNT,
    window=W2V_WINDOW
)

hhgroups2vec.build_vocab(documentos)

words = list(hhgroups2vec.wv.key_to_index)
vocab_size = len(words)
print("Vocab size", vocab_size)


hhgroups2vec.train(documentos, total_examples=len(documentos), epochs=W2V_EPOCH)

hhgroups2vec.wv.most_similar("bien")

hhgroups2vec.wv.most_similar("basura")

hhgroups2vec.wv.most_similar("bien")

hhgroups2vec.wv.most_similar("movistar")

