import mysql.connector as sql


def connect_database():
    conn = sql.connect(
        host="localhost", user="root", password="India@123", db="youtube"
    )
    cur = conn.cursor()
    return cur, conn


# SELECT STATEMENT
def execute_select(query, cur, mydb):
    cur.execute(query)
    return cur

# INSERT VALUES INTO CHANNEL TABLE
def insert_into_channel(val, cur, mydb):
    query = (
        "INSERT INTO channel"
        "(channel_id,"
        "channel_name,"
        "channel_views,"
        "channel_subscribers,"
        "channel_videos,"
        "channel_description) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    cur.execute(query, val)
    mydb.commit()


# INSERT INTO VIDEO TABLE
def insert_into_videos(val, cur, mydb):
    query = (
        "INSERT INTO video"
        "(video_id,"
        "playlist_id,"
        "channel_id,"
        "video_name,"
        "video_description,"
        "published_date,"
        "view_count,"
        "like_count,"
        "dislike_count,"
        "comment_count,"
        "duration,"
        "thumbnail)"
        "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
    )
    cur.execute(query, val)
    mydb.commit()


# INSERT INTO PLAYLIST TABLE
def insert_into_playlist(val, cur, mydb):
    query = "INSERT INTO playlist " "(playlist_id, channel_id) " "VALUES (%s, %s)"
    cur.execute(query, val)
    mydb.commit()


# INSERT INTO COMMENTS TABLE
def insert_into_comments(val, cur, mydb):
    query = (
        "INSERT INTO comment"
        "(comment_id,"
        "video_id,"
        "comment_text,"
        "comment_author,"
        "comment_published_date) "
        "VALUES (%s, %s, %s, %s, %s)"
    )

    cur.execute(query, val)
    mydb.commit()
