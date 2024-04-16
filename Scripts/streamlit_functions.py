# IMPORT NECESSARY LIBRARIES
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px

# IMPORT LOCAL MODULES
import Scripts.sql_script as sql
import Scripts.channelfunctions as ch
import Scripts.functions as f


# SETTING PAGE CONFIGURATIONS
def set_page_config():
    icon = Image.open("assets/ytLogo.png")

    st.set_page_config(
        page_title="Youtube Data Harvesting",
        page_icon=icon,
        layout="wide",
        menu_items={"About": """# This app is created by *Nilankar Deb!*"""},
    )
    set_header("YOUTUBE DATA WAREHOUSE")


# SET HEADER
def set_header(header):
    st.markdown(
        f"<h1 style='text-align: center; color: violet;'>{header}</h1>",
        unsafe_allow_html=True,
    )


# CREATING OPTION MENU
def create_option_menu():

    selected = option_menu(
        menu_title="",
        options=["Home", "Insert", "Analysis", "About"],
        # options =["Home",  "Analysis", "About"],
        icons=["house-door-fill", "tools", "card-text", "file-person"],
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
            },
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "pink",
            },
            "nav-link-selected": {"background-color": "green"},
        },
    )
    return selected


# HOME OPTION
def home(cursor, mydb):
    set_header("ALL CHANNELS")

    # SELECT DATA FROM CHANNEL TABLE
    query = "select channel_name from channel"
    data = sql.execute_select(query, cursor, mydb)

    # CREATE BUTTON TO VIEW MORE DETAILS
    channel = st.selectbox(
        "SELECT A CHANNEL:",
        [d[0] for d in data],
        index=None,
        placeholder="Select channel...",
    )

    # SELECT DATA FROM CHANNEL TABLE
    query = f"SELECT channel_id,channel_name, channel_subscribers, channel_views, channel_videos, channel_description FROM channel WHERE channel_name = '{channel}'"
    data = sql.execute_select(query, cursor, mydb)

    for d in data:
        st.markdown(f"## :blue[Channel ID] : {d[0]}")
        st.markdown(f"## :blue[Channel Name] : {d[1]}")
        st.markdown(f"## :blue[Subscribers] : {d[2]}")
        st.markdown(f"## :blue[Views] : {d[3]}")
        st.markdown(f"## :blue[Total Videos] : {d[4]}")
        st.markdown(f"## :blue[Description] :\n {d[5]}")

    # SELECT DATA FROM VIDEO TABLE
    query = f"SELECT video_name as Title, view_count as Views, like_count as likes, comment_count as Comments FROM video WHERE channel_id =(select channel_id from channel where channel_name = '{channel}')"
    data = sql.execute_select(query, cursor, mydb)

    video_df = pd.DataFrame(data.fetchall(), columns=data.column_names)

    if channel:
        st.dataframe(video_df, use_container_width=True, hide_index=True)


# INSERT OPTION
def insert(cursor, mydb):
    set_header("INSERT DATA")
    channel_id = st.text_input("ENTER CHANNEL ID 👇")

    if st.button("Get channel Details", type="primary"):
        data = ch.get_channel_details(channel_id)

        # INSERTING CHANNEL
        sql.insert_into_channel(
            (
                channel_id,
                data[0]["Channel_name"],
                data[0]["Views"],
                data[0]["Subscribers"],
                data[0]["Total_videos"],
                data[0]["Description"],
            ),
            cursor,
            mydb,
        )

        # INSERTING VIDEOS & PLAYLIST
        videos, playlist_id = ch.get_channel_videos(channel_id)

        # INSERTING PLAYLISTS
        sql.insert_into_playlist((playlist_id, channel_id), cursor, mydb)

        for v in videos:
            vid = ch.get_video_details(v)

            changed_date = f.change_date_format(vid[0]["Published_date"])
            changed_time = f.change_duration_format(vid[0]["Duration"])

            sql.insert_into_videos(
                (
                    v,
                    playlist_id,
                    channel_id,
                    vid[0]["Title"],
                    vid[0]["Description"],
                    f.change_date_format(vid[0]["Published_date"]),
                    vid[0]["Views"],
                    vid[0]["Likes"],
                    vid[0]["Dislikes"],
                    vid[0]["Comments"],
                    f.change_duration_format(vid[0]["Duration"]),
                    vid[0]["Thumbnail"],
                ),
                cursor,
                mydb,
            )

            # INSERTING COMMENTS
            comments = ch.get_comments_details(v)
            if comments:
                for com in comments:
                    sql.insert_into_comments(
                        (
                            com["Comment_id"],
                            v,
                            com["Comment_text"],
                            com["Comment_author"],
                            f.change_date_format(com["Comment_posted_date"]),
                        ),
                        cursor,
                        mydb,
                    )
        st.success("Data inserted successfully!!!")


# ANALYSIS OPTION
def analysis(cursor, mydb):
    set_header("ANALYSIS")

    question = st.selectbox(
        "Select question to analyze:",
        get_questions(),
        index=None,
        placeholder="Select a question...",
    )

    if question:
        # changing question to just number to make if condition easier
        if get_questions().index(question) > 8:
            question = question[:2]
        else:
            question = question[:1]
        get_answer(question, cursor, mydb)


# ABOUT OPTION
def about():
    set_header("**MADE BY MOUMITA ROY**")
    st.markdown(
        "## :blue[Technologies used] : Python, Youtube Data API, SQL, Streamlit"
    )
    st.markdown(
        "## :blue[Overview] : Retrieving the Youtube channels data from the Google API, storing it in a SQL then querying the data and displaying it in the Streamlit app."
    )


# QUESTION LIST
def get_questions():
    questions = [
        "1. What are the names of all the videos and their corresponding channels?",
        "2. Which channels have the most number of videos, and how many videos do they have?",
        "3. What are the top 10 most viewed videos and their respective channels?",
        "4. How many comments were made on each video, and what are their corresponding video names?",
        "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
        "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        "7. What is the total number of views for each channel, and what are their corresponding channel names?",
        "8. What are the names of all the channels that have published videos in the year 2022?",
        "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        "10. Which videos have the highest number of comments, and what are their corresponding channel names?",
    ]
    return questions


# QUERY SQL AND GET ANSWER
def get_answer(question, cursor, mydb):
    data = sql.execute_select(get_query(question), cursor, mydb)
    answer_df = pd.DataFrame(data.fetchall(), columns=data.column_names)
    st.dataframe(answer_df, use_container_width=True, hide_index=True)
    make_chart(question, data, answer_df)


# GET THE CORRESPONDING SQL QUERY
def get_query(question):
    question_dict = {
        "1": "SELECT v.video_name as Video, c.channel_name as Channel FROM video v JOIN channel c ON v.channel_id = c.channel_id;",
        "2": "SELECT c.channel_name as Channel, COUNT(v.video_id) as Video_Count FROM channel c INNER JOIN video v ON c.channel_id = v.channel_id GROUP BY c.channel_id, Channel ORDER BY Video_Count DESC",
        "3": "SELECT v.video_name as Video, c.channel_name as Channel, v.view_count as Views FROM video v INNER JOIN channel c ON v.channel_id = c.channel_id ORDER BY v.view_count DESC limit 10",
        "4": "SELECT v.video_name Title, COUNT(c.comment_id) AS Comments FROM video v LEFT JOIN comment c ON v.video_id = c.video_id GROUP BY v.video_name ORDER BY Comments DESC",
        "5": "SELECT v.video_name as Video, ch.channel_name as Channel, v.like_count as Likes FROM video v JOIN channel ch ON v.channel_id = ch.channel_id ORDER BY Likes DESC LIMIT 10;",
        "6": "SELECT v.video_name as Video, SUM(v.like_count) AS Likes, SUM(v.dislike_count) AS Dislikes FROM video v GROUP BY v.video_name;",
        "7": "select channel_name as Channel,channel_views as Views from channel",
        "8": "SELECT DISTINCT c.channel_name as Channel FROM channel c JOIN video v ON c.channel_id = v.channel_id WHERE YEAR(v.published_date) = 2022;",
        "9": "SELECT c.channel_name as Channel, CONCAT(FLOOR(AVG(v.duration) / 60), ' m ', ROUND(MOD(AVG(v.duration), 60)), ' s') AS Average_Duration FROM channel c JOIN video v ON c.channel_id = v.channel_id GROUP BY c.channel_name;",
        "10": "SELECT v.video_name as Video, c.channel_name as Channel, COUNT(co.comment_id) AS Comments FROM video v JOIN channel c ON v.channel_id = c.channel_id JOIN comment co ON v.video_id = co.video_id GROUP BY v.video_name, c.channel_name ORDER BY Comments DESC;",
    }
    return question_dict[question]


# MAKE CHARTED VIEW
def make_chart(question, cursor, df):
    if question in ["2", "7"]:
        fig = px.bar(
            df,
            x=cursor.column_names[0],
            y=cursor.column_names[1],
            orientation="v",
            color=cursor.column_names[0],
        )
        st.plotly_chart(fig, use_container_width=True)
    elif question in ["3", "5"]:
        fig = px.bar(
            df,
            x=cursor.column_names[2],
            y=cursor.column_names[1],
            orientation="h",
            color=cursor.column_names[0],
        )
