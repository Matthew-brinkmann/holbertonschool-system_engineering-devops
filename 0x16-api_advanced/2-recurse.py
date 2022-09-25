#!/usr/bin/python3
"""third task for advanced API"""
import requests


def recurse(subreddit, hot_list=[], count=0, after=None):
    """Returns a list containing tites of ALL
    hot articles in a subreddit. Done recursively.
    None if not a valid subreddit"""
    if subreddit is None or not type(str):
        return (None)

    apiUrlToCall = "http://www.reddit.com/r/{}/hot.json".format(subreddit)
    headersToCall = {"User-Agent":
                     "Python3:School_Project:v1.0 (by /u/theHilariousMrcbtdx)"}
    requestOptions = {"count": count,
                      "after": after}
    apiRequest = requests.get(apiUrlToCall,
                              headers=headersToCall,
                              verify=False,
                              params=requestOptions).json()
    allPosts = apiRequest.get("data", {}).get("children", 0)
    after = apiRequest.get('data', {}).get('after', None)
    if allPosts is None or apiRequest.get("error") == 404:
        if len(hot_list) == 0:
            return (None)
        return (hot_list)
    else:
        for singlePost in allPosts:
            hot_list.append(singlePost.
                            get('data', {}).
                            get('title'))
    if after is None:
        if len(hot_list) == 0:
            return None
        return (hot_list)
    else:
        count = len(hot_list)
        return recurse(subreddit, hot_list, count, after)
