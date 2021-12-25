import requests
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAG1IXQEAAAAAUd1GAqrl4tKWAUyqcUWJ7oB5hE8%3DwxHZaWNPhe8JaQew1nDLRgqUHdA14GKbA9Z0OWoWRtt5rEnpOj'
bearer_token = os.environ.get("BEARER_TOKEN")

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
    


def get_following_users(user_id):
    url = create_url(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    following_data = json.dumps(json_response, indent=4, sort_keys=True)
    
    data_list = json.loads(following_data)
    #print(data_list['data'][0]['username']) 
        #^ this was to test which part of the dictionary and list i needed to iterate through 
    username_list = []

    for i in range(len(data_list['data'])):
        username = data_list['data'][i]['username']
        user_id = data_list['data'][i]['id']
        username_list.append({user_id:username}) # THIS IS AN ARRAY OF DICTIONARIES
   
    return(username_list)

#def add_nodes(username_list):

   # print(list(username_list[0].values()))
   # following_user_list = list(username_list[0].values())
    #G.add_nodes_from(following_user_list)



def main():
    user_id = 2244994945
    following_users = get_following_users(user_id)
   # print(get_connected_users(following_users, user_id))

    # G = nx.Graph()
    #add_nodes(following_users)
    # nx.draw(G, with_labels = True)
    # plt.show()
    

if __name__ == "__main__":
    main()