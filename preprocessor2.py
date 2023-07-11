
from googletrans import Translator
translator = Translator()
from io import StringIO
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
@st.cache_resource(hash_funcs={StringIO: StringIO.getvalue})
def preprocess(df2):

    sentiments = SentimentIntensityAnalyzer()

    ct = 0
    pos = []
    neg = []
    neu = []

    for i in df2["message"]:
       # print(i)
        text = translator.translate(i).text
        print(text)
        pos.append(sentiments.polarity_scores(text)["pos"])
        neg.append(sentiments.polarity_scores(text)["neg"])
        neu.append(sentiments.polarity_scores(text)["neu"])
        ct = ct + 1

    df2["positive"] = pos
    df2["negative"] = neg
    df2["neutral"] = neu

    return df2
