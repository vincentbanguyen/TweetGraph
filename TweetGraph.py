import requests
import tweepy
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import time

class User(object):
    def __init__(self, username, userID):
        self.username = username
        self.userID = userID


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

# CONNECTING TO TWITTER API
def create_url(user_id):
    return "https://api.twitter.com/2/users/{}/following".format(user_id)

def get_params():
    return {"user.fields": "created_at"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
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
        print("OH HI MARK")
        return "NO CONNECTIONS"
    
def get_following_users2(username):
    time.sleep(3)
    username_list = []
    for user in tweepy.Cursor(api.get_friends, screen_name=username).items():
       username = user.screen_name
       userID = get_user_id(user.screen_name)
       following_user = User(username, userID)
       username_list.append(following_user)
       
    return(username_list)

def get_following_users(start_user: User):
    time.sleep(3)
    print("getting following list of: " + str(start_user.username))
    url = create_url(start_user.userID)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)
    username_list = []

    for i in range(len(data_list['data'])):
        username = data_list['data'][i]['username']
        id = data_list['data'][i]['id']
        following_user = User(username, id)
        username_list.append(following_user)

      #  username = data_list['data'][i]['username']
      #  user_id = data_list['data'][i]['id']
      #  username_list.append({user_id:username}) # THIS IS AN ARRAY OF DICTIONARIES
   
    return(username_list)

def add_nodes(G, connected_users, username):
    G.add_node(username)
    connected_usernames = []
    for user in connected_users:
        following_username = user.username
        G.add_node(following_username)
        G.add_edge(username, following_username)


# EXECUTE CODE HERE ---------------------------------------------------------------------------------
def main():

    username = "tweetgraphdev"
    user_id = get_user_id(username)
    start_user = User(username, user_id)

    
    connected_users = get_connected_users(start_user)

    G = nx.Graph()
    add_nodes(G, connected_users, username)
    nx.draw(G, with_labels = True)
    plt.show()
    

if __name__ == "__main__":
    main()

