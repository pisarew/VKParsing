import requests
import sqlite3 as sq

token = 'a6d0701fa6d0701fa6d0701fe0a6aa21cfaa6d0a6d0701fc77957373e0265f6e83e255d'
version = 5.131
count = 100

with open('domains.txt') as f: 
    domains = []
    for domain in f:
        if domain[ 0 : (len(domain) - 2)] != '':
            domains.append(domain[ 0 : (len(domain) - 1)])


def loadJson(token, version, domain, count):
    r = requests.get('https://api.vk.com/method/wall.get', params = { 
        'access_token': token,
        'v': version,
        'domain': domain,
        'count': count
    })
    return r.json()
k = 0
with sq.connect("ParsingData.db") as con:
        cur = sq.Cursor(con)

        cur.execute("""CREATE TABLE IF NOT EXISTS posts (
            PostText TEXT,
            date TEXT,
            organization TEXT
        )""")
        
        con.commit()
        for domain in domains:
            posts = loadJson(token, version, domain, count)
            for post in posts['response']['items']:
                text = post['text']
                date = post['date']
                organization = domain

                cur.execute(f"SELECT * FROM posts WHERE date = '{date}' ")
                if cur.fetchone() is None:
                    cur.execute(f"INSERT INTO posts VALUES (?, ?, ?)", (text, date, organization))
                    con.commit()
                    k += 1
                    print(k, ' complite!')
                    
                    
                        