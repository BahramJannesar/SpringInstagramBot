from instagram_private_api import Client, ClientCompatPatch
from login import login
from arguser import get_args
import json
import time
import os

arguser = get_args()

user_name = arguser.user
password = arguser.password
target_username = arguser.username_target
counts_of_commenters = int(arguser.counts_of_commenters)

api = login(user_name, password)

def save_object( file_name  , saved_object , writing_method , seprator):

    saved_object = json.dumps(saved_object, indent=3 , ensure_ascii= False)
    with open(file_name, writing_method) as handler:
        handler.writelines(saved_object + seprator)

def get_target_user_id_and_api( user_name , password ,  target_username ) : 

    
    user_info = api.username_info(target_username)
    target_user_id = user_info['user']['pk']

    return target_user_id


def gain_user_feed():

    feed_result = []
    target_user_id  = get_target_user_id_and_api( user_name , password ,  target_username )
    user_info = api.user_info(target_user_id)

    user_feed = api.user_feed(target_user_id)
    feed_result.extend(user_feed['items'])
    save_object('user_feed.json' , feed_result , 'w' , '')

    next_max_id = user_feed.get('next_max_id')

    while user_feed['num_results'] < user_info['user']['media_count']:
        user_feed = api.user_feed(target_user_id , max_id = next_max_id)
        feed_result.extend(user_feed['items'])
        if not user_feed['more_available']:
            save_object('user_feed.json' , feed_result , 'w' , '')
            break
        next_max_id = user_feed.get('next_max_id')
        save_object('user_feed.json' , feed_result , 'w' , '')


def gain_media_ids():

    media_ids = []
    with open('user_feed.json' , 'r') as file:
        json_loaded = json.load(file)
        for each in json_loaded:
            media_ids.append(each['id'])
    os.remove('user_feed.json')
    return media_ids

def gain_commenters():

    list_commenters = []
    dict_of_commenters = {}
    for each_id in list_media_ids:  
        comments = api.media_comments(each_id)
        for each_comment in comments['comments']:
            if len(list_commenters) <= counts_of_commenters:
                list_commenters.append(each_comment['user']['pk'])
            else:
                break

    list_commenters = list(set(list_commenters))
    dict_of_commenters = {
            'target_user_name': target_username,
            'target_followers' : list_commenters
    }

    save_object('commenters.json' , dict_of_commenters , 'w' , '')



if __name__ == "__main__":
    

    gain_user_feed()
    list_media_ids = gain_media_ids()
    gain_commenters()