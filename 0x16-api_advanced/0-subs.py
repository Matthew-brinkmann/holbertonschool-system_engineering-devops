#!/usr/bin/python3
"""first task for advanced API"""
import requests


def number_of_subscribers(subreddit):
    """Returns the number of subscribers
    to a subreddit or 0(zero) if not a
    valid subreddit"""

    if subreddit is None or not type(str):
        return (0)

    apiUrlToCall = "http://www.reddit.com/r/{}/about.json".format(subreddit)
    headersToCall = {"User-Agent":
                     "Python3:School_Project:v1.0 (by /u/theHilariousMrcbtdx)"}
    apiRequest = requests.get(apiUrlToCall,
                              headers=headersToCall,
                              verify=False).json()
    totalSubs = apiRequest.get("data", {}).get("subscribers", 0)

    return (totalSubs)
