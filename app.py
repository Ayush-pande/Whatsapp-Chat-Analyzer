import googletrans
from io import StringIO
import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocessor
from googletrans import Translator
translator = Translator()
import preprocessor2
import base64
import seaborn as sns


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('/Users/ayushpandey612/Downloads/whatsappdark.webp')


st.header("Whatsapp Chat Analyser")
st.sidebar.title("Upload Your file here")
st.markdown("""
<style>
    [data-testid=stSidebar] {
    textColor: #25D366;
        background-color: #014D4E;
        background-image: url(‘https://i.pinimg.com/564x/8c/98/99/8c98994518b575bfd8c949e91d20548b.jpg);
    }
</style>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Select a file")

if uploaded_file is not None:
    bytes_data =uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    data1=bytes_data.decode("utf-8")
   # st.text(data)
    df = preprocessor.preprocess(data)
    df2 = preprocessor.preprocess(data)



    df = preprocessor2.preprocess(df)
    st.dataframe(df)
    st.dataframe(df2)




    user_list = df['user'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0 , "Overall")

    #df = preprocessor2.preprocess(df)
    #st.dataframe(df2)
    #st.dataframe(df)
    service = ["Overall Analysis" , "Translate"]
    option = st.sidebar.selectbox("Select the service" ,service)
    if option=="Overall Analysis":



        selected_user = st.sidebar.selectbox("Show Analysis", user_list)
        if st.sidebar.button("Show Analysis"):

            num_messages, words , num_media_file ,links = helper.fetch_stats(selected_user, df)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.title("Total Messages")
                st.title(num_messages)
            with col2:
                st.title("Total Words")
                st.title(words)
            with col3:
                st.title("Media Files")
                st.title(num_media_file)
            with col4:
                st.title("Links")
                st.title(links)

            col1, col2 = st.columns(2)

            with col1:
                st.title("Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'], color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.title("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)







            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


            if selected_user=="Overall":
                st.title("Most_Active_Users")
                x , new_df = helper.most_active_users(df)
                fig , ax = plt.subplots()

                col1 , col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values , color="red")
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            col1, col2 = st.columns(2)
            with col1:
                st.title("Weekly Activity Map")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

            with col2:
                st.title("wordCloud")
                df_wc = helper.create_word_cloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Most common words')
            st.pyplot(fig)




            st.header("Sentimental Analysis")
            a , b , c = helper.senti(selected_user ,df)
            list =["Positive" , "Negative" , "Neutral"]
            score = [a , b , c]
            fig, ax = plt.subplots()

            ax.pie( score ,labels=list ,autopct='%.2f%%')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            #st.title(a)
            #st.title(b)
            #st.title(c)













    if option=="Translate":
        user_input = st.text_input("Enter the Language you want to translate in")
        if not user_input:
            st.warning('Please input language')
            st.stop()
        if user_input is None:
            pass
        else:
            r = df.shape[0]
            user = []
            message = []
            for i in df["user"]:
                user.append(i)
            for i in df["message"]:
                message.append(i)

            for i in range(len(user)):
                u = user[i]
                text = translator.translate(message[i], dest=user_input).text
                total = u + ":" + text
                st.text(total)

























