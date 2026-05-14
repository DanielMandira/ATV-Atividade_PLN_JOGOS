import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import spacy
import re
import os

from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Carregando o modelo do Spacy para Português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Baixando modelo spacy pt_core_news_sm...")
    ret = os.system("python -m spacy download pt_core_news_sm")
    if ret != 0:
        print("Aviso: Falha no download do Spacy. Usando WordNetLemmatizer como fallback.")
        nlp = None
    else:
        nlp = spacy.load("pt_core_news_sm")

def preprocess(text):
    raw_text = str(text)
    # Converter para string e minúsculas
    text = raw_text.lower()
    
    # Remoção de pontuação e caracteres especiais
    text = re.sub(r'[^\w\s]', '', text)
    
    # 1. Tokenização
    tokens = word_tokenize(text, language='portuguese')
    
    # 2. Remoção de Stopwords
    stop_words = set(stopwords.words('portuguese'))
    tokens_no_stop = [word for word in tokens if word not in stop_words]
    
    # 3. Radicalização (Stemming)
    stemmer = SnowballStemmer('portuguese')
    stemmed_tokens = [stemmer.stem(word) for word in tokens_no_stop]
    
    # 4. Lematização (usando o Spacy a partir das palavras sem stopwords, ou WordNet se falhar)
    if nlp is not None:
        text_no_stop = " ".join(tokens_no_stop)
        doc = nlp(text_no_stop)
        lemmatized_tokens = [token.lemma_ for token in doc]
    else:
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens_no_stop]
    
    return {
        'original_raw': raw_text,
        'original': text,
        'tokens': tokens,
        'tokens_no_stop': tokens_no_stop,
        'stemmed': stemmed_tokens,
        'lemmatized': lemmatized_tokens
    }

def main():
    print("Iniciando pré-processamento...")
    df = pd.read_csv("metacritic_reviews.csv")
    
    resultados = []
    for comment in df['Comment']:
        resultados.append(preprocess(comment))
        
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv("comentarios_processados.csv", index=False, encoding='utf-8')
    
    print("\n--- Processamento concluído! ---")
    print("Resultados salvos em 'comentarios_processados.csv'.")
    print("\n--- Processamento dos 4 Primeiros Comentários ---")
    for i in range(4):
        print(f"\n[Comentário {i+1}]")
        print("Original:", df_resultados['original_raw'].iloc[i])
        print("Tokens:", df_resultados['tokens'].iloc[i])
        print("Sem Stopwords:", df_resultados['tokens_no_stop'].iloc[i])
        print("Stemming:", df_resultados['stemmed'].iloc[i])
        print("Lematização:", df_resultados['lemmatized'].iloc[i])

if __name__ == "__main__":
    main()
