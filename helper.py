#from urlextract  import URLExtract
#extract = URLExtract()
import matplotlib as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats(selected_user , df):


    if selected_user !='Overall':
        df = df[df['user']==selected_user]

    num_messages = df.shape[0]
    words =[]
    for i in df['message']:
        words.extend(i.split())

    num_media_messages = df[df["message"]=='<Media omitted>\n'].shape[0]
   ## links =[]
    #for message in df["message"]:
       # links.extend(extract.find_urls(message))

    return num_messages , len(words) , num_media_messages  

def most_active_users(df):
    x = df["user"].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0]*100 , 2).reset_index().rename(columns ={'index':'name' ,'count':'percent'})

    return x ,df

def create_word_cloud(selected_user ,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    wc = WordCloud(width=500, height=500 ,min_font_size=10 , background_color='white')
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def senti(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    x = sum(df["positive"])
    y = sum(df["negative"])
    z = sum(df["neutral"])

    t = x + y + z

    a = round((x/t)*100 ,2)
    b = round((y/t)*100 ,2)
    c = round((z/t)*100 ,2)


    return  a , b , c




