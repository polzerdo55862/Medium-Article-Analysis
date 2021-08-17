import sys

sys.path.append('.')
import medium_scraper
from unicodedata import name
from scraper.models import *
import requests
from bs4 import BeautifulSoup
from scraper.models import Archives
from datetime import datetime, timedelta, timezone
import re
import os
from os import listdir
from os.path import isfile, join
import json
from datetime import datetime
import pytz

def how_many_users_clapped():
    '''
    Collects the number of users clapped for each article
    '''

    # get all entries in table articles where field voter_count is empty
    all_articles = Articles.objects.all()
    articles = Articles.objects.filter(voter_scraped_date__isnull=True)

    for article in articles:
        post_id = re.search(r'[a-zA-Z0-9]*$', article.url).group(0)

        json = {
            "operationName": "PostVotersDialogQuery",
            "variables": {
                "postId": "3a971a1ce78d",
                "pagingOptions": {
                    "limit": 10
                }
            },
            "query": "query PostVotersDialogQuery($postId: ID!, $pagingOptions: PagingOptions) {\n  post(id: $postId) {\n    id\n    title\n    clapCount\n    voterCount\n    voters(paging: $pagingOptions) {\n      items {\n        user {\n          id\n          ...UserFollowButton_user\n          ...Voter_user\n          __typename\n        }\n        clapCount\n        __typename\n      }\n      pagingInfo {\n        next {\n          page\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ...UserFollowButton_post\n    __typename\n  }\n}\n\nfragment Voter_user on User {\n  id\n  username\n  bio\n  name\n  ...userUrl_user\n  ...UserAvatar_user\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment UserFollowButton_user on User {\n  ...UserFollowButtonSignedIn_user\n  ...UserFollowButtonSignedOut_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedIn_user on User {\n  id\n  __typename\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowButton_post on Post {\n  collection {\n    id\n    __typename\n  }\n  ...UserFollowButtonSignedOut_post\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedOut_post on Post {\n  ...SusiClickable_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n"
        }

        #replace postID with postId of specified article
        json["variables"]["postId"] = post_id

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "apollographql-client-name": "lite",
            "apollographql-client-version": "main-20210716-213924-fe75fd1a3c",
            "content-type": "application/json",
            "graphql-operation": "PostVotersDialogQuery",
            "medium-frontend-app": "lite/main-20210716-213924-fe75fd1a3c",
            "medium-frontend-path": "/what-to-study-before-a-data-science-interview-3a971a1ce78d",
            "medium-frontend-route": "post",
            "ot-tracer-sampled": "true",
            "ot-tracer-spanid": "4c8343535be62fbe",
            "ot-tracer-traceid": "2c9d6abafdcdff63",
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        request = requests.post(url="https://towardsdatascience.com/_/graphql", json=json, headers=headers)
        print(request)

        try:
            # find number of voters
            voter_count = re.search(r'"voterCount":[0-9]*', str(request._content)).group(0)
            voter_count_int = int(voter_count.replace('"voterCount":',""))

            # find number of clapps
            clap_count = re.search(r'"clapCount":[0-9]*', str(request._content)).group(0)
            clap_count_int = int(clap_count.replace('"clapCount":', ""))

            # save in database
            article.voter_count = voter_count_int
            article.clap_count = clap_count_int

            # save timestamp
            article.voter_scraped_date = datetime.now(tz=pytz.UTC)

            article.save()

            print("Votes: " + str(article.voter_count))
            print("Claps: " + str(article.clap_count))
            print("No Voter found for " + str(len(articles)) + " articles")
            print("Number of articles in total: " + str(len(all_articles)) + " articles")
            print("Timestamp: " + str(datetime.now(tz=pytz.UTC)))
        except:
            print("Couldnt find or save voter_count and clap_count for: " + str(request._content))

def save_articles_to_html():
    '''
    Saves html to all articles in the folder .articles
    '''

    counter = 1

    # read filenames in articles folder
    dir = os.getcwd()
    folder = dir + "\\articles\\"

    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    file_ids = [f.replace(".html", "") for f in onlyfiles]
    print(str(len(file_ids)) + " articles already saved")

    #for article in Articles.objects.filter(published__year=2021).values():
    for article in Articles.objects.values():
        article_url = article["url"]
        article_id = article["id"]

        if str(article_id) in file_ids:
            print("--- Article " + str(article_id) + " was already saved")
        else:
            r = requests.get(article_url)
            soup_article = BeautifulSoup(r.text, 'html.parser')
            html = soup_article.prettify("utf-8")

            filename = folder + str(article_id) + ".html"

            with open(filename, "wb") as file:
                file.write(html)

            print("Saved article with ID: " + str(article_id))

        counter = counter + 1


if __name__ == '__main__':
    # how_many_users_clapped()
    save_articles_to_html()