from instagram_private_api import Client, ClientCompatPatch
from login import login
from arguser import get_args
import json
import time

arguser = get_args()

user_name = arguser.user
password = arguser.password
target_username = arguser.username_target
counts_of_follower = int(arguser.counts_of_follower)


def save_object( file_name  , saved_object , writing_method , seprator):

    saved_object = json.dumps(saved_object, indent=3 , ensure_ascii= False)
    with open(file_name, writing_method) as handler:
        handler.writelines(saved_object + seprator)

def get_target_user_id_and_api( user_name , password ,  target_username ) : 

    api = login(user_name, password)
    user_info = api.username_info(target_username)
    target_user_id = user_info['user']['pk']

    return target_user_id , api

def gain_followers():

    results = []

    target_user_id , api = get_target_user_id_and_api( user_name , password ,  target_username )

    rank_token = api.generate_uuid()
    
    followers = api.user_followers(target_user_id, rank_token=rank_token )

    results.extend(followers.get('users', []))
    
    next_max_id = followers.get('next_max_id')

    while len(results) < counts_of_follower :
        time.sleep(3)
        followers = api.user_followers(target_user_id, rank_token=rank_token , max_id = next_max_id)
        results.extend(followers['users'])
        next_max_id = followers['next_max_id']
        save_object('target_followers.json' , results , 'w' , '')

    user_id_cleaner('target_followers.json' , target_user_id)


def user_id_cleaner(target_followers_file_name , target_user_id):

    target_follower_list = []

    with open(target_followers_file_name , 'r+' ) as file :
        loaded_json = json.load(file)
        for user_id in loaded_json:
            target_follower_list.append(user_id['pk'])

        target_follower_dict = {
            'target_user_id':target_user_id,
            'target_followers': target_follower_list[0:counts_of_follower]
        }

        save_object(target_followers_file_name , target_follower_dict , 'w' , '')


if __name__ == "__main__":

    gain_followers()
    