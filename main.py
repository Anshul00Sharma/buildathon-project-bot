from atproto import Client, models
import sqlite3
from postFunctions import get_all_posts, get_post_comments,comments_from_posts
from db import save_posts, list_posts,save_comments_to_db,list_comments_from_db,commented
import datetime
import time
from langchain_openai import ChatOpenAI
from agent import generate_Tweet_text, reply
import schedule
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    USERNAME = os.getenv("uname")
    PASSWORD = os.getenv("upass")
    client = Client()
    print(USERNAME)
    print(PASSWORD)
    profile = client.login(USERNAME, PASSWORD)
    llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-4o')
    print('Welcome,', profile.display_name)
    
    schedule.every().hour.do(scheduled_tweets,client,llm)
    schedule.every(10).minutes.do(fetch_posts_data,client,profile)
    schedule.every(11).minutes.do(reply_to_comments,client,llm)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
def fetch_posts_data(client,profile):
    posts = get_all_posts(client, profile.did)
    comments_arr = comments_from_posts(posts,client)
    save_comments_to_db(comments_arr)
    
def scheduled_tweets(client,llm):
    text = generate_Tweet_text(llm)
    text = text.replace('"','')
    print("Tweet:",text)
    post_tweet(client,text)
def reply_to_comments(client,llm):
    
    comments = list_comments_from_db()
    
    for comment in comments:
        print(comment)
        if comment['commented'] == 0 and comment["owner"] != "karl-smith-marx.bsky.social":
            try:
                text = reply(llm,comment['text'],comment['parentText'])
                text = text.replace('"','')
                print("Tweet:",text)
                reply_to_comment_bsky(client,text,comment['uri'],comment['cid'],comment['parentUri'],comment['parentCid'])
            except Exception as e:
                print(e)
            else:
                commented(comment['uri'])
                
def reply_to_comment_bsky(client,comment,uri,cid,parentUri,parentCid):
    reply = models.AppBskyFeedPost.ReplyRef(
        root=models.ComAtprotoRepoStrongRef.Main(
            uri=parentUri,
            cid=parentCid
        ),
        parent=models.ComAtprotoRepoStrongRef.Main(
            uri=uri,
            cid=cid
        )
        )
    response = client.send_post(
        text=comment,
        reply_to=reply)
    print(f"Reply sent successfully. URI: {response.uri}")

    
    
                
        
              
def post_tweet(client,text):
    client.send_post(text=text)
    



if __name__ == '__main__':
    main()