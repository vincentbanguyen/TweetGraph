import requests
import tweepy
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import time

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
    print(response.status_code)
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

def get_connected_users(username_list, user_id):
    connected_users = [] 
    following_id_list = []
    for following_user in username_list: # Get Following list of each following user
        following_id_list = list(following_user.keys())[0]

        for following_user in following_id_list: #  Checks if following list contains start user
            if following_user == user_id:
                print("CONNECTION MADE!")
                connected_users.append(following_user)

    if len(connected_users) != 0:
        return connected_users
    else:
        return "NO CONNECTIONS"
    
#def get_following_users2(username):
  #  username_list = []
  #  for user in tweepy.Cursor(api.get_friends, screen_name=username).items():
  #      username_list.append({get_user_id(user.screen_name):user.screen_name})
  #  return(username_list)

def get_following_users(user_id):
    time.sleep(0.05)
    url = create_url(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)
    #print(data_list['data'][0]['username']) 
        #^ this was to test which part of the dictionary and list i needed to iterate through 
    username_list = []

    for i in range(len(data_list['data'])):
        user = User()
        user.username = data_list['data'][i]['username']
        user.id = data_list['data'][i]['id']
        username_list.append(user)

      #  username = data_list['data'][i]['username']
      #  user_id = data_list['data'][i]['id']
      #  username_list.append({user_id:username}) # THIS IS AN ARRAY OF DICTIONARIES
   
    return(username_list)

def add_nodes(G, following_users):
    following_usernames = []
    for user in following_users:
        username = list(user.values())[0]
        following_usernames.append(username)
    print(following_usernames)
    G.add_nodes_from(following_usernames)



def main():
    username = "tweetgraphdev"
    user_id = get_user_id(username)
    following_users = get_following_users(user_id)
    print(get_connected_users(following_users, user_id))

    G = nx.Graph()
    add_nodes(G, following_users)
    nx.draw(G, with_labels = True)
    plt.show()
    

if __name__ == "__main__":
    main()

class User:
    def __init__(self, username, id):
        self.username = username
        self.id = id