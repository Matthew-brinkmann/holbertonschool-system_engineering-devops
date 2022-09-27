#!/usr/bin/python3
"""third task for advanced API"""
from collections import OrderedDict
import requests


def count_words(subreddit, word_list, after=None, print_dict={}):
    """
    recursive function that queries the Reddit API,
    parses the title of all hot articles,
    and prints a sorted count of given keywords.
    If no posts match or the subreddit is invalid,
    print nothing.
    """
    if subreddit is None or not type(str):
        return (None)

    apiUrlToCall = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headersToCall = {"User-Agent":
                     "Python3:School_Project:v1.0 (by /u/theHilariousMrcbtdx)"}
    requestOptions = {"after": after}
    apiRequest = requests.get(apiUrlToCall,
                              headers=headersToCall,
                              params=requestOptions).json()
    allPosts = apiRequest.get("data", {}).get("children", 0)
    after = apiRequest.get('data', {}).get('after', None)
    if allPosts is None or apiRequest.get("error") == 404:
        if len(print_dict) == 0:
            return
        return (print_dictionary(print_dict))
    else:
        for singlePost in allPosts:
            title = singlePost.get('data', {}).get('title')
            print_dict = search_title_for_words(title,
                                                word_list,
                                                print_dict)
    if after is None:
        if len(print_dict) == 0:
            return
        return (print_dictionary(print_dict))
    else:
        return count_words(subreddit, word_list, after, print_dict)


def print_dictionary(print_dict):
    """
    prints out final word list or prints Nothing.
    """
    if len(print_dict) == 0:
        return
    sorted_dict = OrderedDict(sorted(print_dict.items(), key=lambda x: x[1]))
    sorted_dict = OrderedDict(reversed(list(sorted_dict.items())))
    for k, v in sorted_dict.items():
        print("{}: {}".format(k, v))
    return


def search_title_for_words(title, word_list, print_dict):
    """
    searches through a title to find words in
    the word_list
    """
    titleAsWordArray = title.split()
    for word in word_list:
        for titleWord in titleAsWordArray:
            if word.lower() == titleWord.lower():
                if word.lower() in print_dict.keys():
                    print_dict[word.lower()] += 1
                else:
                    print_dict[word.lower()] = 1
    return (print_dict)
