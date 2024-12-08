
import datetime


def get_all_posts(client, did):
    all_posts = []
    cursor = None
    while True:
        posts = client.app.bsky.feed.get_author_feed({'actor': did, 'cursor': cursor, 'limit': 100})
        all_posts.extend(posts.feed)
        if not posts.cursor:
            break
        cursor = posts.cursor
    return all_posts

def get_post_comments(client, uri):
    thread = client.app.bsky.feed.get_post_thread({'uri': uri, 'depth': 1})
    if not thread.thread.replies:
        return []
    return thread.thread.replies


    
def comments_from_posts(posts,client):
    comments_arr = []
    for post in posts: 
        comments = get_post_comments(client, post.post.uri)
        # print(f"Post: {post.post.record.text}")
        # print(f"Comments: {len(comments)}")
        for comment in comments:
            print(f"- {comment.post.record.text}")
            obj = {
                "parent": {
                    "uri": post.post.uri,
                    "text": post.post.record.text,
                    "cid": post.post.cid
                },
                "uri": comment.post.uri,
                "cid": comment.post.cid,
                "text": comment.post.record.text,
                "owner":comment.post.author.handle
            }
            comments_arr.append(obj)
    

    return comments_arr

