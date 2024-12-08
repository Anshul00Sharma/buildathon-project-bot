import sqlite3
def save_posts(posts):
    conn = sqlite3.connect('posts.db')

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS post (
            id INTEGER PRIMARY KEY,
            uri TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    for post in posts:
        print(f"Post: {post.post.record.text}")
        print(f"Uri: {post.post.uri}")
        add_posts(post.post.uri, post.post.record.text, conn)
        
        # print(f"Comments: {len(comments)}")
def add_posts(uri, text, conn):
    cursor = conn.cursor()
    
    # Check if the URI already exists
    cursor.execute("SELECT * FROM post WHERE uri = ?", (uri,))
    if cursor.fetchone() is not None:
        print(f'URI exists, not adding: {uri}')
        return
    
    # Insert the new post
    cursor.execute("INSERT INTO post (uri, text) VALUES (?, ?)", (uri, text))
    conn.commit()
def list_posts():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    for row in cursor.fetchall():
        print(row)

def save_comments_to_db(comments_arr):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            uri TEXT NOT NULL,
            text TEXT NOT NULL,
            parentUri TEXT NOT NULL,
            parentText TEXT NOT NULL,
            commented BOOLEAN NOT NULL DEFAULT 0,
            owner TEXT NOT NULL,
            cid TEXT NOT NULL,
            parentCid TEXT NOT NULL
        )
    ''')
    for comment in comments_arr:
        cursor.execute("SELECT uri FROM comments WHERE uri = ?", (comment['uri'],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO comments (parentUri, parentText, uri, text, owner, cid, parentCid) VALUES (?, ?, ?, ?, ?, ?, ?)", (comment['parent']['uri'], comment['parent']['text'], comment['uri'], comment['text'], comment['owner'], comment['cid'], comment['parent']['cid']))
        else:
            print(f'Comment already exists: {comment["uri"]}')
    conn.commit()
    conn.close()

def list_comments_from_db():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments")
    comments = []
    for row in cursor.fetchall():
        obj = {
            "id":row[0],
            "uri":row[1],
            "text":row[2],
            "parentUri":row[3],
            "parentText":row[4],
            "commented":row[5],
            "owner":row[6],
            "cid":row[7],
            "parentCid":row[8]
        }
        comments.append(obj)
    return comments

def commented(uri):
    with sqlite3.connect('posts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE comments SET commented = ? WHERE uri = ?", (True, uri))
        conn.commit()