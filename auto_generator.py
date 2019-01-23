import argparse
import configparser
import os.path
import requests
from operator import itemgetter
import random
import string

API_ROOT_URL = "http://localhost:8000/"
CREATED_USERS = []
CREATED_POSTS = []
USER_POST_LIKES = []
USER_LIKING_ORDER = []
ELIGIBLE_USERS_TO_BE_LIKED = []
POSTS_LIKE_AMMOUNT = {}

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
    data = {"user": {
        "first_name": "David",
        "last_name": "Testing",
        "username": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "password": "Overlord12",
        "email": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))+"@gmail.com"
    }}
    url = API_ROOT_URL + "users/"
    response = requests.post(url, json=data)
    CREATED_USERS.append(response.json())
    return response


def create_post(user_id):
    data = {
        "post_text": "This is a test post!"
    }
    url = API_ROOT_URL + "users/" + str(user_id) + "/posts/"
    response = requests.post(url, data=data)
    CREATED_POSTS.extend(response.json())
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
    user_id_to_be_liked = get_user_id_to_like(user_id)
    if user_id_to_be_liked is False:
        return False
    posts_of_user = POSTS_LIKE_AMMOUNT.get(user_id_to_be_liked)
    print("@@@@@#")
    print(posts_of_user)
    print(user_id)
    print(user_id_to_be_liked)
    post_id_to_be_liked = random.choice(posts_of_user)[0]
    data = {}
    response = requests.post(API_ROOT_URL + "users/" + str(user_id) + "/posts/" + str(post_id_to_be_liked) + "/like/", data=data)
    USER_POST_LIKES.extend(response.json())
    return response


def eligible_posts_for_likes(user_id):
    counter = 0
    for post in CREATED_POSTS:
        if post['user'] == user_id:
            pass
        else:
            counter += 1
    return counter


for _ in range(number_of_users):
    create_user()

for user in CREATED_USERS:
    post_likes_tuple = []
    i = random.randint(0, max_posts_per_user)
    # print(user)
    # print(i)
    USER_LIKING_ORDER.append((user['id'], i))
    if i > 0:
        ELIGIBLE_USERS_TO_BE_LIKED.append(user['id'])
    for _ in range(i):
        resp = create_post(user_id=user['id'])
        post_likes_tuple.append((resp.json()['id'], 0))
    POSTS_LIKE_AMMOUNT[user['id']] = post_likes_tuple

# for user in CREATED_USERS:
x = len(USER_LIKING_ORDER)
sorted(USER_LIKING_ORDER, key=itemgetter(1))
for _ in range(x):
    user_id_max_post_tuple = USER_LIKING_ORDER.pop()
    # max_eligible_posts = eligible_posts_for_likes(user_id=user_id_max_post_tuple[0])
    # if max_eligible_posts < max_likes_per_user:
    #     i = random.randint(0, max_eligible_posts)
    # else:
    #     i = random.randint(0, max_likes_per_user)
    for _ in range(user_id_max_post_tuple[1]):
        resp = user_like_post(user_id_max_post_tuple[0])
        if resp is False:
            break

print("-----------CREATED USERS---------------")
print(CREATED_USERS)
print("-----------CREATED POSTS---------------")
print(CREATED_POSTS)
print("-----------USER POST LIKES---------------")
print(USER_POST_LIKES)
