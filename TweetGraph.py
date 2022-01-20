import requests
import tweepy
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
from skimage import io

class User(object):
    def __init__(self, username, userID, userimgURL):
        self.username = username
        self.userID = userID
        self.userimgURL = userimgURL


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAG1IXQEAAAAAUd1GAqrl4tKWAUyqcUWJ7oB5hE8%3DwxHZaWNPhe8JaQew1nDLRgqUHdA14GKbA9Z0OWoWRtt5rEnpOj'
bearer_token = os.environ.get("BEARER_TOKEN")

consumerKey = "z0zWSSgYygacLBHnpoewDpgbh"
consumerSecret = "lFDGsXMZkh8LLES1JLXvoxGwh86x1cY61nk76bbxhFXCLoBBk1"
accessToken = "1473779807800332288-7jgp19ZOh7OyccOS34wIQJHwSvtTA2"
accessTokenSecret = "8cfSwjASHSaHvKH8iN9owkIdsWsvd6vm1VOXYA2uH9gQ7"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

counter = 0 #counts the number of follow pulls (should not exceed 15 per 15 min)

# CONNECTING TO TWITTER API
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


## ACTIONS
def get_user_id(username):
    user = api.get_user(screen_name = username)
    return(user.id)

def get_connected_users(start_user):
    following_users = get_following_users(start_user)
    connected_users = []
    for following_user in following_users: # Get Following list of each following user
        following_username = following_user.username # gets username of following user
        following_user_list = get_following_users(following_user) # Creates a list of following for following user
        for following_following_user in following_user_list: #  Checks if following list contains start user
            if int(following_following_user.userID) == int(start_user.userID):
                print("CONNECTION MADE with " + str(following_username))
                connected_users.append(following_user)
                
    if len(connected_users) != 0:
        return connected_users
    else:
        print("User has no connections")
        return []

def get_profile_image(user_ID: int): # RETURNS IMAGE URL OF INPUTTED USER ID
    url = "https://api.twitter.com/2/users/{}".format(user_ID)
    params = {"user.fields": "profile_image_url"}
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)
    image = data_list['data']['profile_image_url']
    return image

    
def get_following_list_profile_images(user: User):
    url = "https://api.twitter.com/2/users/{}/following".format(user.userID)
    params = {"user.fields": "profile_image_url"}
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)


def get_following_users(user: User):
    global counter
    if counter == 15:
        counter = 0
        time.sleep(901)
    counter+=1
    print(counter)
    print("getting following list of: " + str(user.username))
    url = "https://api.twitter.com/2/users/{}/following".format(user.userID)

    params = {"user.fields": "created_at,profile_image_url"}
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)
    username_list = []
    if len(data_list) > 1:
        for i in range(len(data_list['data'])):
            username = data_list['data'][i]['username']
            id = data_list['data'][i]['id']
            image = data_list['data'][i]['profile_image_url']
            following_user = User(username, id, image)
            username_list.append(following_user)
    return(username_list)

def add_nodes(G, connected_users, username, profile_images): # ADDING USER NODES TO GRAPH
    if len(connected_users) > 0:
        for user in connected_users:
            following_username = user.username
            img = io.imread(user.userimgURL)
            G.add_node(following_username, image = img)
            G.add_edge(username,following_username)
            # profile_images.append(img)
    

def test_exception_rate(start_user):
    i = 0
    while i != 182:
        get_following_users(start_user)
        i += 1
        print(i)



# EXECUTE CODE HERE ---------------------------------------------------------------------------------
def main():
    profile_images = []
    username = "VincentBaNguyen"
    user_id = get_user_id(username)
    imgURL = get_profile_image(user_id)
    start_user = User(username, user_id, imgURL)
    profile_images.append(io.imread(imgURL))
    user_profile_img = io.imread(imgURL)
    connected_users = get_connected_users(start_user)

    G = nx.Graph()
    add_nodes(G, connected_users, username, profile_images)
    G.add_node(username, image = user_profile_img)

    pos=nx.circular_layout(G)

    fig=plt.figure(figsize=(5,5))
    ax=plt.subplot(111)
    ax.set_aspect('equal')
    nx.draw_networkx_edges(G,pos,ax=ax)

    plt.xlim(-1.5,1.5)
    plt.ylim(-1.5,1.5)

    trans=ax.transData.transform
    trans2=fig.transFigure.inverted().transform

    piesize=0.1 # this is the image size
    p2=piesize/2.0
    for n in G:
        xx,yy=trans(pos[n]) # figure coordinates
        xa,ya=trans2((xx,yy)) # axes coordinates
        a = plt.axes([xa-p2,ya-p2, piesize, piesize])
        a.set_aspect('equal')
        a.imshow(G.nodes[n]['image'])
        a.axis('off')
    ax.axis('off')
    plt.show()

    #test_exception_rate(start_user)        # To test exception rate error

if __name__ == "__main__":
    main()

