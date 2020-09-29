from instagram_private_api import Client, ClientCompatPatch
from login import login
from arguser import get_args
import json
import time

arguser = get_args()

user_name = arguser.user
password = arguser.password


def save_object( file_name  , saved_object , writing_mode , seprator):

    saved_object = json.dumps(saved_object, indent=3 , ensure_ascii= False)
    with open(file_name, writing_mode) as handler:
        handler.writelines(saved_object + seprator)

def get_your_user_id_and_api( user_name , password) : 

    api = login(user_name, password)
    user_info = api.username_info(user_name)
    your_user_id = user_info['user']['pk']

    return your_user_id , api


def gain_your_followers_and_following():

    results_followers = []
    results_followings = []

    your_user_id , api = get_your_user_id_and_api( user_name , password)

    rank_token = api.generate_uuid()

    user_info = api.username_info(user_name)
    follower_count = user_info['user']['follower_count']
    following_count = user_info['user']['following_count']
    
    followers = api.user_followers(your_user_id, rank_token=rank_token )
    following = api.user_following(your_user_id, rank_token=rank_token )

    results_followers.extend(followers.get('users', []))
    save_object('your_followers.json' , results_followers , 'w' , '')

    results_followings.extend(following.get('users', []))
    save_object('your_following.json' , results_followings , 'w' , '')

    if follower_count > 200 or follower_count > 200 :

        next_max_id_follower = followers.get('next_max_id')
        next_max_id_following = following.get('next_max_id')

        while len(results_followers) < follower_count :
            #time.sleep(3)
            followers = api.user_followers(your_user_id, rank_token=rank_token , max_id = next_max_id_follower)
            results_followers.extend(followers['users'])
            next_max_id_follower = followers['next_max_id']
            save_object('your_followers.json' , results_followers , 'w' , '')

        while len(results_followings) < following_count :
            #time.sleep(3)
            following = api.user_following(your_user_id, rank_token=rank_token , max_id = next_max_id_following)
            results_followings.extend(following['users'])
            next_max_id_following = following['next_max_id']
            save_object('your_following.json' , results_followings , 'w' , '')

                    
def users_must_unfollow(your_followers_file_name , your_following_file_name): 

    follower_list = []
    following_list = []
    users_must_unfollow = []

    with open(your_followers_file_name) as follower_file , open(your_following_file_name) as following_file:

        follower_json_loaded = json.load(follower_file)
        following_json_loaded = json.load(following_file)

        for follower in follower_json_loaded:
            follower_list.append(follower['pk'])
        for following in following_json_loaded:
            following_list.append(following['pk'])

    for user in following_list:
        if user not in follower_list:
            users_must_unfollow.append(user)

    print('There is {} number of account doesnt follow you back!'.format(len(users_must_unfollow)))
    return users_must_unfollow


def user_unfollow(list_of_user_must_unfollow):

    counter = 1
    your_user_id , api = get_your_user_id_and_api( user_name , password)

    for user in list_of_user_must_unfollow:  

        if counter < 50 :
            time.sleep(15)
            status = api.friendships_destroy(user)
            print('Username number {} with user id {} is now deleted from your following'.format(counter , user))
            log_dict = {
                'your_user_id': your_user_id,
                'info': 'Username number {} with user id {} is now deleted from your following'.format(counter , user),
                'status': status
            }

            save_object('unfollow_log.json' , log_dict , 'a' , ',')
            counter += 1


if __name__ == "__main__":

    gain_your_followers_and_following()
    users_must_unfollow = users_must_unfollow('your_followers.json' , 'your_following.json')
    user_unfollow(users_must_unfollow)