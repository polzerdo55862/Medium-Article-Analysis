import re
import sys
import requests
sys.path.append('.')
from medium_scraper import __init__
from datetime import date, datetime, timedelta, timezone, tzinfo
from scraper.models import * 
from bs4 import BeautifulSoup
import json


def collect_user_info(url):

    res = requests.get(url="https://dmnkplzr.medium.com/followers")

    bs = BeautifulSoup(res.text, "html.parser")

    # nach reihenfolge - nicht sehr zuverlässig, vll mit regex suchen
    x = bs.findAll("script")[5].string

    a = re.search("(?<=window.__APOLLO_STATE__ = ).*",x).group(0)

    a_json = json.loads(a)

    a_json = list(a_json.items())

    root_query = a_json[0]

    # user
    main_user =  a_json[1][1]
    main_user_id = main_user["id"]
    main_info = main_user["bio"]
    main_full_name = main_user["name"]
    main_user_name = main_user["username"]
    main_image_id = main_user["imageId"]
    main_follower_count = main_user["socialStats"]["followerCount"]
    main_following_count = main_user["socialStats"]["followingCount"]
    main_url = "mediu.com/"+main_user_name
    main_user_obj = Users.objects.update_or_create(user_name = main_user_name, defaults={"medium_id":main_user_id, "user_name":main_user_name, "full_name":main_full_name, "info":main_info , "follower_count":main_follower_count , "following_count":main_following_count , "url":main_url , "image_id":main_image_id, "last_updated":datetime.now(timezone(timedelta(hours=0)))})[0]
    print(main_user_name)
    # followers
    for i in range(2, len(a_json)-2):
        user =  a_json[i][1]
        if user.get("__typename") == "User":
            user_id = user["id"]
            info = user.get("bio")
            full_name = user["name"]
            user_name = user["username"]
            image_id = user.get("imageId")
            url = "https://medium.com/@"+user_name
            user_obj = Users.objects.update_or_create(user_name = user_name, defaults={"medium_id":user_id, "user_name":user_name, "full_name":full_name, "info":info , "url":url , "image_id":image_id, "last_updated":datetime.now(timezone(timedelta(hours=0)))})[0]
            Follower_Relations.objects.update_or_create(user1=main_user_obj, user2=user_obj, date=datetime.now(timezone(timedelta(hours=0))))
            print(user_name)

    next_user = a_json[len(a_json)-3][1]["id"]

    fp_query = open("medium_scraper/data/data0.json", "r")
    fp_headers = open("medium_scraper/data/headers.json", "r")
    query = json.load(fp_query)
    headers = json.load(fp_headers)
    query["variables"]["paging"]["from"] = next_user
    query["variables"]["paging"]["limit"] = 25
    query["variables"]["username"] = "@"+main_user_name


    while True:

        req = requests.post("https://medium.com/_/graphql", json=query, headers=headers)
        
        content = json.loads(req.content)

        follower_user_connection = content["data"]["userResult"]["followersUserConnection"]
        users = follower_user_connection["users"]
        paging_info = follower_user_connection["pagingInfo"]
        
        for user in users:
            user_id = user["id"]
            info = user["bio"]
            full_name = user["name"]
            user_name = user["username"]
            image_id = user["imageId"]
            url = "https://medium.com/@"+user_name

            user_obj = Users.objects.update_or_create(user_name = user_name, defaults={"medium_id":user_id, "user_name":user_name, "full_name":full_name, "info":info , "url":url , "image_id":image_id, "last_updated":datetime.now(timezone(timedelta(hours=0)))})[0]
            Follower_Relations.objects.update_or_create(user1=main_user_obj, user2=user_obj, date=datetime.now(timezone(timedelta(hours=0))))
        
            print(user_name)
            
        if paging_info["next"] == None:
            break
        elif next_user == paging_info["next"]["from"]:
            break
        next_user = paging_info["next"]["from"]
        query["variables"]["paging"]["from"] = next_user
    
    
        
