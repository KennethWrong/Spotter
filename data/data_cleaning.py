import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import neattext.functions as nfx

from nltk.stem import WordNetLemmatizer
import os

cwd = os.path.dirname(__file__)


def word_lemmatization(sentence):
    lemmatizer = WordNetLemmatizer()
    sentence = sentence.split()
    sentence = [lemmatizer.lemmatize(word) for word in sentence]
    sentence = " ".join(sentence)
    return sentence

def clean_data(file_path):
    df = pd.read_csv(file_path)
    df['Clean_Text'] = df['Text'].apply(nfx.remove_stopwords)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_userhandles)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_punctuations)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_emojis)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_hashtags)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_special_characters)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_urls)
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_emojis)
    df['Clean_Text'] = df['Clean_Text'].apply(lambda x: word_lemmatization(x))

    df['Clean_Text'].replace('', np.nan, inplace=True)
    df = df.dropna()
    
    df = df[['Clean_Text', 'Emotion']]
    
    print(df['Clean_Text'].head())

    emotions = df['Emotion'].unique()
    emotion_mapping = {emotion:idx for idx, emotion in enumerate(emotions)}

    df['emotion_encoded'] = df['Emotion'].map(emotion_mapping)

    text_labels = df[['emotion_encoded', 'Emotion']]
    text_labels.to_csv(os.path.join(cwd, "labels.csv"), index=False)
    train_data = df['Clean_Text']
    train_data.to_csv(os.path.join(cwd, "data.csv"), index=False)
    
if __name__ == "__main__":
    clean_data(os.path.join(cwd, "emotion_dataset.csv"))
