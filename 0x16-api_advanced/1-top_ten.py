#!/usr/bin/python3
"""second task for advanced API"""
import requests


def top_ten(subreddit):
    """Returns the title of the first
    10 hot posts to a subreddit or
    None if not a valid subreddit"""

    if subreddit is None or not type(str):
        print(None)
        return

    apiUrlToCall = "http://www.reddit.com/r/{}/hot.json".format(subreddit)
    headersToCall = {"User-Agent":
                     "Python3:School_Project:v1.0 (by /u/theHilariousMrcbtdx)"}
    requestOptions = {"limit": 10}
    apiRequest = requests.get(apiUrlToCall,
                              headers=headersToCall,
                              verify=False,
                              params=requestOptions).json()
    allPosts = apiRequest.get("data", {}).get("children", 0)
    if allPosts is None:
        print(None)
    else:
        for singlePost in allPosts:
            print(singlePost.get('data', {}).
                  get('title'))
