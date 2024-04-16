# YouTube Data Harvesting and Warehousing using SQL and Streamlit

## Problem Statement 
The task is to build a Streamlit app that permits users to analyze data from multiple YouTube channels. 
Users can input a YouTube channel ID to access data like channel information, video details, and user engagement. 
The app should facilitate storing the data in a MongoDB database and allow users to collect data from up to 10 different channels. 
The app should enable searching and retrieval of data from the SQL database, 
including advanced options like joining tables for comprehensive channel information.

## Technology Stack Used
1. Python
2. MySQL
4. Google Client Library
5. Plotly
6. Pandas

## Approach

1. Start by establishing a connection to the YouTube API V3, which allows me to retrieve channel and video data by utilizing the Google API client library for Python. 

2. Next step is to setup a database connection and make necessary tables to fill in data. In this case i used MySQL.

3. Then by setting up a Streamlit application using the python library "streamlit", it provides an easy-to-use interface for users to enter a YouTube channel ID, view channel details.
Also, using suitable functions and the api the data was retrieved and stored in lists

4. For the next step we have to store the retrieved data from multiple channels namely the channels,videos and comments to a SQL data warehouse, utilizing a SQL database like MySQL

5. Now, with the help of SQL queries to retrieve specific channel data based on user input by joining within the SQL tables For that the SQL table was previously made and should have proper foreign and the primary key. 

6. The retrieved data is displayed within the Streamlit application, leveraging Streamlit's data visualization capabilities to create charts and graphs for users to analyze the data.
