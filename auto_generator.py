import argparse
import configparser
import os.path
import requests
from operator import itemgetter
import random
import string
import json

with open('predefined_emails.json') as f:
    predefined_emails = json.load(f)

API_ROOT_URL = "http://localhost:8000/"
CREATED_USERS = []
CREATED_POSTS = []
USER_POST_LIKES = []
USER_LIKING_ORDER = []
ELIGIBLE_USERS_TO_BE_LIKED = []
POSTS_LIKE_AMMOUNT = {}
USER_TOKEN_MAP = {}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", dest="filename",
                    help="path to config file", metavar="FILE")
args = parser.parse_args()

assert os.path.isfile(args.filename), "config file could not be found"

config = configparser.ConfigParser()
config.sections()
config.read(args.filename)
number_of_users = int(config.get('CONFIG', 'number_of_users'))
max_posts_per_user = int(config.get('CONFIG', 'max_posts_per_user'))
max_likes_per_user = int(config.get('CONFIG', 'max_likes_per_user'))
print(number_of_users, max_likes_per_user, max_posts_per_user)



def create_user():
    sub_data = {}
    sub_data["username"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    sub_data["password"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    if config.getboolean('CONFIG', 'use_predefined_emails') is True:
        email = random.choice(predefined_emails['email_list'])
        sub_data["email"] = email
        predefined_emails['email_list'].remove(email)
    else:
        sub_data["email"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "@gmail.com"
    data = {"user": sub_data}
    url = API_ROOT_URL + "users/"
    response = requests.post(url, json=data)
    if response.json().get("message", "") == "Email is not valid":
        return response
    if response.status_code == 400:
        print("Error occured while creating user with email %s:, %s"%(email, response.json()["errors"]))
        return response
    CREATED_USERS.append(response.json())
    USER_TOKEN_MAP[response.json()['id']] = response.json()['token']
    return response


def create_post(user_id):
    hed = {'Authorization': 'Bearer ' + USER_TOKEN_MAP[user_id]}
    data = {
        "post_text": "This is a test post!"
    }
    url = API_ROOT_URL + "users/" + str(user_id) + "/posts/"
    response = requests.post(url, data=data, headers=hed)
    CREATED_POSTS.append(response.json())
    return response


def check_if_user_likeable(user_id):
    x = POSTS_LIKE_AMMOUNT.get(user_id, (1, 1))
    sorted(x, key=itemgetter(1))
    if x[0][1] == 0:
        return True
    return False


def get_user_id_to_like(user_id):
    temp_array = ELIGIBLE_USERS_TO_BE_LIKED
    if user_id in temp_array: temp_array.remove(user_id)
    if len(ELIGIBLE_USERS_TO_BE_LIKED) == 0:
        return False
    if len(temp_array) == 0:
        return False
    user_id_to_be_liked = random.choice(temp_array)
    if check_if_user_likeable(user_id_to_be_liked):
        return user_id_to_be_liked
    else:
        ELIGIBLE_USERS_TO_BE_LIKED.remove(user_id_to_be_liked)
        return get_user_id_to_like(user_id)


def user_like_post(user_id):
    hed = {'Authorization': 'Bearer ' + USER_TOKEN_MAP[user_id]}
    user_id_to_be_liked = get_user_id_to_like(user_id)
    if user_id_to_be_liked is False:
        return False
    posts_of_user = POSTS_LIKE_AMMOUNT.get(user_id_to_be_liked)

    post_id_to_be_liked = random.choice(posts_of_user)[0]
    data = {}
    response = requests.post(API_ROOT_URL + "users/" + str(user_id) + "/posts/" + str(post_id_to_be_liked) + "/like/",
                             data=data, headers=hed)
    USER_POST_LIKES.append(response.json())
    return response


def eligible_posts_for_likes(user_id):
    counter = 0
    for post in CREATED_POSTS:
        if post['user'] == user_id:
            pass
        else:
            counter += 1
    return counter


print("----Creating " + str(number_of_users) + " users----------")
for _ in range(number_of_users):
    create_user()

for user in CREATED_USERS:
    post_likes_tuple = []
    i = random.randint(0, max_posts_per_user)
    print("----Creating " + str(i) + " posts for user with id " + user['id'] + "----------")
    USER_LIKING_ORDER.append((user['id'], i))
    if i > 0:
        ELIGIBLE_USERS_TO_BE_LIKED.append(user['id'])
    for _ in range(i):
        resp = create_post(user_id=user['id'])
        post_likes_tuple.append((resp.json()['id'], 0))
    POSTS_LIKE_AMMOUNT[user['id']] = post_likes_tuple

x = len(USER_LIKING_ORDER)
sorted(USER_LIKING_ORDER, key=itemgetter(1))
for _ in range(x):
    user_id_max_post_tuple = USER_LIKING_ORDER.pop()
    print("----Liking " + str(user_id_max_post_tuple[1]) + " posts as user with id " + user_id_max_post_tuple[
        0] + " ----------")
    for _ in range(user_id_max_post_tuple[1]):
        resp = user_like_post(user_id_max_post_tuple[0])
        if resp is False:
            break

print("-----------CREATED USERS---------------")
for user in CREATED_USERS:
    print("Email: %s, Password: %s, First Name: %s, Last Name: %s" % (user.get("email", ""), user.get("password", ""),
                                                                      user.get("first_name", ""),
                                                                      user.get("last_name", "")))
print("-----------CREATED POSTS---------------")
for post in CREATED_POSTS:
    print("Post text: %s, Poster ID: %s" % (post.get("post_text", ""), post.get("user", "")))
print("-----------USER POST LIKES---------------")
for post_like in USER_POST_LIKES:
    print("Post with id: %s, was liked by User with id: %s" % (post_like.get("post", ""), post_like.get("user", "")))
