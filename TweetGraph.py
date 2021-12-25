import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAG1IXQEAAAAAUd1GAqrl4tKWAUyqcUWJ7oB5hE8%3DwxHZaWNPhe8JaQew1nDLRgqUHdA14GKbA9Z0OWoWRtt5rEnpOj'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    user_id = 2244994945
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


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    data_print = json.dumps(json_response, indent=4, sort_keys=True)

    print(data_print)
    return data_print
    
def get_usernames(data_print):
    data_list = json.loads(data_print)
    #print(data_list['data'][0]['username']) 
        #^ this was to test which part of the dictionary and list i needed to iterate through 
    username_list = []
    for i in range(len(data_list['data'])):
        username = data_list['data'][i]['username']
        user_ID = data_list['data'][i]['id']
        username_list.append({user_ID:username})
    print(username_list)
    return(username_list)


if __name__ == "__main__":
    main()