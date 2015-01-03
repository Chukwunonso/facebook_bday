import requests
import facebook
import json
import random

"""
Get all my birthday wall posts, 
and like and comment them.
"""

BASE_URL = 'https://graph.facebook.com/v2.2/'
ACCESS_TOKEN = ''
MY_ID = '10203439226367251' 
MESSAGES = [
    'Your wishes warm my heart,',
    'Thank you for your wishes,',
    'You are too kind,',
    'Your wishes are appreciated. Thank you,',
    'I appreciate your birthday wishes,',
    'You have made my day,'
]
    
def stop_condition(post):
    "Callback that will limit posts by date"
    created = post['created_time']
    day = created[: created.find('T')]
    return not(day in ['2015-01-03', '2015-01-02'])

def get_posts():
    "Returns all posts in a list"

    url = '%sme/feed/?access_token=%s' % (BASE_URL, ACCESS_TOKEN)
    all_posts = []
    posts = requests.get(url).json()
    stop = True
    while stop:
        for post in posts['data']:
            # check for the break condition
            # could use 'break' here
            if stop_condition(post):
                stop = False
            else:
                all_posts.append(post)
        # find the next page and extract contents
        posts = requests.get(posts['paging']['next']).json()
    return all_posts

def get_first_name(post):
    "Return the first name of the post author"
    name = post['from']['name'].split(' ')
    return name[0]

def message(post):
    "Returns the name and the message as a tuple"
    msg = random.choice(MESSAGES)
    name = get_first_name(post)
    # todo: use a dictionary to map nicknames
    data = '%s %s' % (msg, name) 
    return data, name
    
def run():
    graph = facebook.GraphAPI(ACCESS_TOKEN)
    posts = get_posts()
    for post in posts:
        msg, name = message(post)
        if name.lower() != 'justina':
            graph.put_like(post['id'])
            #graph.put_comment(post['id'], msg)


if __name__ == '__main__':
    run()
