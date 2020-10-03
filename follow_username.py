from instagram_private_api import Client, ClientCompatPatch
from login import login
from arguser import get_args
import json
import time

arguser = get_args()

user_name = arguser.user
password = arguser.password
target_username = arguser.username_target
option = arguser.option


def save_object( file_name  , saved_object , writing_method , seprator):

    saved_object = json.dumps(saved_object, indent=3 , ensure_ascii= False)
    with open(file_name, writing_method) as handler:
        handler.writelines(saved_object + seprator)


def get_target_user_id_and_api( user_name , password ,  target_username ) : 

    api = login(user_name, password)
    user_info = api.username_info(target_username)
    target_user_id = user_info['user']['pk']

    return target_user_id , api

def follow_target_user_ids(option):

    if option == 'followers':
        file_name = 'target_followers.json'
    elif option == 'likers':
        file_name = 'likers.json'
    elif option == 'commenters':
        file_name = 'commenters.json'

    target_user_id , api = get_target_user_id_and_api( user_name , password ,  target_username )
    counter = 1
    with open(file_name , 'r') as file :
        loaded_json = json.load(file)
        must_follow_today = loaded_json['target_followers'][0:49]
        must_to_write = loaded_json['target_followers'][50:-1]
        
        target_follower_dict = {
            'target_user_id':target_user_id,
            'target_followers': must_to_write
        }

        save_object(file_name , target_follower_dict , 'w' , '')

    for user in must_follow_today:
        time.sleep(20)
        status = api.friendships_create(user)

        print('Username number {} with user id {} is now your following'.format(counter , user))
        log_dict = {
            'info': 'Username number {} with user id {} is now your following'.format(counter , user),
            'status': status
        }
        save_object('log.json' , log_dict , 'a' , ',')

        counter += 1


if __name__ == "__main__":

    follow_target_user_ids(option)
    