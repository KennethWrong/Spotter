import numpy as np
import pandas as pd
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import neattext.functions as nfx
import nltk

import os

cwd = os.path.dirname(__file__)

# nltk.download('wordnet')


def word_lemmatization(sentence):
    lemmatizer = WordNetLemmatizer()
    sentence = sentence.split()
    sentence = [lemmatizer.lemmatize(word) for word in sentence]
    sentence = " ".join(sentence)
    return sentence

def clean_text(df, text_col_name):
    df['Clean_Text'] = df[text_col_name].apply(nfx.remove_stopwords)
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
    return df
    

def clean_data(file_path, text_col, emotion_col, change_emotion=None):
    df = pd.read_csv(file_path)
    df = clean_text(df, text_col)
    df = df[['Clean_Text', emotion_col]]

    if change_emotion:
        for k,v in change_emotion.items():
            df.replace(to_replace=k, value=v, inplace=True)
    
    return df
    
def export_csv(df, change_emotion=None):
    
    if change_emotion:
        for k,v in change_emotion.items():
            df.replace(to_replace=k, value=v, inplace=True)
    
    emotions = df['Emotion'].unique()
    print(emotions)
    emotion_mapping = {emotion:idx for idx, emotion in enumerate(emotions)}
    
    df['emotion_encoded'] = df['Emotion'].map(emotion_mapping)

    text_labels = df[['emotion_encoded', 'Emotion']]
    text_labels.to_csv(os.path.join(cwd, "labels.csv"), index=False)
    train_data = df['Clean_Text']
    train_data.to_csv(os.path.join(cwd, "data.csv"), index=False)
    
if __name__ == "__main__":
    df1 = clean_data(os.path.join(cwd, "emotion_dataset.csv"), "Text", "Emotion")

    change_emotion = {
        'empty':'shame',
        'joy': "surprise",
        'fun': "joy",
        'hate': "anger",
        'relief': 'neutral',
        'love': 'joy',
        'worry': 'fear',
        'boredom': 'neutral',
        'happiness': 'joy',
        'enthusiasm': 'joy',
    }
    
    
    change_emotion2 = {
        # 'fear': 'bad',
        # 'surprise': 'good',
        # 'anger': 'bad',
        'shame': 'anger',
        # 'neutral': 'good',
        'disgust': 'anger',
        # 'joy': 'good',
        # 'sadness': 'bad'
    }

    combine = False
     
    if combine:
        df2 = clean_data(os.path.join(cwd, "tweet_emotions.csv"), "content", "sentiment", change_emotion)
        
        # Rename columns
        new_cols = {x: y for x, y in zip(df2.columns, df1.columns)}
        df2 = df2.rename(columns=new_cols)
        combined_df = pd.concat([df1, df2], ignore_index=True)
        combined_df.drop_duplicates(subset=['Clean_Text'])
    
        export_csv(combined_df, change_emotion=change_emotion2)
    else:
        export_csv(df1, change_emotion=None)
    