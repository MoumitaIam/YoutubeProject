# Imports
from googleapiclient.discovery import build
import Scripts.constants as c

youtube = build(c.api_service_name,c.api_version,developerKey=c.api_key)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# FUNCTION TO GET CHANNEL DETAILS
def get_channel_details(channel_id):
    ch_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics", id=channel_id
    )
    response = request.execute()

    data = dict(
        Channel_id=channel_id,
        Channel_name=response["items"][0]["snippet"]["title"],
        Playlist_id=response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ],
        Subscribers=response["items"][0]["statistics"]["subscriberCount"],
        Views=response["items"][0]["statistics"]["viewCount"],
        Total_videos=response["items"][0]["statistics"]["videoCount"],
        Description=response["items"][0]["snippet"]["description"],
        Country=response["items"][0]["snippet"].get('country')
    )
    ch_data.append(data)
    return ch_data


# -----------------------------------------------------------------------------------------------------------------------------------------------------#


# FUNCTION TO GET VIDEOS
def get_channel_videos(channel_id):

    video_ids = []

    # Finding the uploads playlist id
    response = youtube.channels().list(part="contentDetails", id=channel_id).execute()

    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    next_page_token = None

    while True:
        res = (
            youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return video_ids,playlist_id


# -----------------------------------------------------------------------------------------------------------------------------------------------------#


# FUNCTION TO GET VIDEO DETAILS
def get_video_details(v_id):

    video_stats = []

    for i in range(0, len(v_id), 50):
        response = (
            youtube.videos()
            .list(part="snippet,contentDetails,statistics", id=v_id)
            .execute()
        )

        video = response["items"][0]
        video_details = dict(
            Channel_name=video["snippet"]["channelTitle"],
            Channel_id=video["snippet"]["channelId"],
            Video_id=video["id"],
            Title=video["snippet"]["title"],
            Tags=video["snippet"].get("tags"),
            Thumbnail=video["snippet"]["thumbnails"]["default"]["url"],
            Description=video["snippet"]["description"],
            Published_date=video["snippet"]["publishedAt"],
            Duration=video["contentDetails"]["duration"],
            Views=video["statistics"]["viewCount"],
            Likes=video["statistics"].get("likeCount"),
            Dislikes=video["statistics"].get("dislikecount"),
            Comments=video["statistics"].get("commentCount"),
            Favorite_count=video["statistics"]["favoriteCount"],
            Definition=video["contentDetails"]["definition"],
            Caption_status=video["contentDetails"]["caption"],
        )
        video_stats.append(video_details)
    return video_stats


# -----------------------------------------------------------------------------------------------------------------------------------------------------#


# FUNCTION TO GET COMMENT DETAILS
def get_comments_details(v_id):

    comment_data = []

    try:
        next_page_token = None
        while True:
            response = (
                youtube.commentThreads()
                .list(
                    part="snippet,replies",
                    videoId=v_id,
                    maxResults=100,
                    pageToken=next_page_token,
                )
                .execute()
            )

            # pprint(response)

            for cmt in response["items"]:
                data = dict(
                    Comment_id=cmt["id"],
                    Video_id=cmt["snippet"]["videoId"],
                    Comment_text=cmt["snippet"]["topLevelComment"]["snippet"][
                        "textDisplay"
                    ],
                    Comment_author=cmt["snippet"]["topLevelComment"]["snippet"][
                        "authorDisplayName"
                    ],
                    Comment_posted_date=cmt["snippet"]["topLevelComment"]["snippet"][
                        "publishedAt"
                    ],
                    Like_count=cmt["snippet"]["topLevelComment"]["snippet"][
                        "likeCount"
                    ],
                    Reply_count=cmt["snippet"]["totalReplyCount"],
                    Replies=cmt["replies"]["comments"][0]["snippet"]["textDisplay"],
                )
                comment_data.append(data)
            next_page_token = response.get("nextPageToken")
            if next_page_token is None:
                break
    except:
        pass

    return comment_data
