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
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def collect_archive_urls(url, publication):
    """
    Parameters
    ----------
    url: str
    publication: QuerySet[scraper.models.Publication]
    """

    anchor_list = get_soup(url).select("div.timebucket > a")

    if (len(anchor_list) == 0):
        print(url)
        match = re.search("[\d/]+$", url)
        group = match.group(0).strip("/")
        arr = group.split("/")
        dt = None
        if len(arr[0]) > 0:
            if len(arr) == 3:
                dt = datetime(int(arr[0]), int(arr[1]), int(arr[2]))
            elif len(arr) == 2:
                dt = datetime(int(arr[0]), int(arr[1]), 1)
            elif len(arr) == 1:
                dt = datetime(int(arr[0]), 1, 1)

        Archives.objects.update_or_create(url=url.strip(), publication=publication, last_seen=None, date=dt)

    else:

        url_list = []

        for anchor in anchor_list:
            url_1 = anchor.get("href")
            if url_1 == url:
                print(url)
                match = re.search("[\d/]+$", url)
                group = match.group(0).strip("/")
                arr = group.split("/")
                dt = None
                if len(arr) > 1:
                    if len(arr) == 3:
                        dt = datetime(int(arr[0]), int(arr[1]), int(arr[2]))
                    elif len(arr) == 2:
                        dt = datetime(int(arr[0]), int(arr[1]), 1)
                    elif len(arr) == 1:
                        dt = datetime(int(arr[0]), 1, 1)

                Archives.objects.update_or_create(url=url.strip(), publication=publication, last_seen=None, date=dt)
                return
            url_list.append(url_1)

        for url in url_list:
            collect_archive_urls(url, publication)


def collect_articles_from_archive(users):
    """
    Parameters
    ----------
    url: QuerySet[scraper.models.Users]
    """

    for user in users:

        url = user["url"]

        def get_regx_group_0(ptrn, str):

            match = re.search(ptrn, str)

            if match != None:
                return match.group(0)

            return None

        def int_from_k_m_string(str):

            match = re.search("[\d\.]+", str)

            if match != None:
                match = match.group(0)

            else:
                return None

            if "K" in str:
                return int(float(match) * 1000)

            elif "M" in str:
                return int(float(match) * 1000000)
            else:
                return int(match)

        article_list = get_soup(url).select_one(
            "div > div.container.u-maxWidth1040.u-marginTop30 > div.col.u-xs-size12of12.u-size8of12.u-padding0 > div.u-marginTop25.js-postStream")

        for article in article_list.contents:

            title = article.select_one("div.section-content")

            if title != None:
                title = title.text

            print("title: " + title)
            read_time_string = article.select_one(
                "div > div > div.u-clearfix.u-marginBottom15.u-paddingTop5 > div > div > div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > span.readingTime")[
                'title']
            read_time = get_regx_group_0('\d+', read_time_string)
            published_string = article.select_one(
                "div > div > div.u-clearfix.u-marginBottom15.u-paddingTop5 > div > div > div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > div > a > time")[
                'datetime']
            published = datetime.strptime(published_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            last_seen = datetime.now(timezone(timedelta(hours=0)))
            user_url = article.select_one("div > div > div:nth-child(2) > a")['href']
            article_url = article.select_one("div > div > div:nth-child(3) > a")['href']
            article_url = get_regx_group_0(".+.com/[^\?]+", article_url)
            user_url = get_regx_group_0(".+.com/@[^\?]+", user_url)
            print("article url: " + article_url)
            print("user url: " + user_url)
            user_full_name = article.select_one(
                "div > div > div.u-clearfix.u-marginBottom15.u-paddingTop5 > div > div > div.postMetaInline.postMetaInline-authorLockup.ui-captionStrong.u-flex1.u-noWrapWithEllipsis > a.ds-link.ds-link--styleSubtle.link.link--darken.link--accent.u-accentColor--textNormal.u-accentColor--textDarken").string
            user_name = get_regx_group_0("(?<=towardsdatascience\.com/@)[^?]+", user_url)
            user_obj = Users.objects.update_or_create(full_name=user_full_name, user_name=user_name, url=user_url)[0]
            archive_publication_url = get_regx_group_0(".+(?=archive)", url)
            archive_publication_name = get_regx_group_0("((?<=https://).+(?=.com))|((?<=medium.com/).+)",
                                                        archive_publication_url)
            publication_obj = Publications.objects.get_or_create(archive_publication_name, url=archive_publication_url)[
                0]
            archive_obj = Archives.objects.get(url=url)
            response_count_string = article.select_one(
                "div > div > div.u-clearfix.u-paddingTop10 > div.buttonSet.u-floatRight > a")
            if response_count_string != None:
                response_count = int_from_k_m_string(response_count_string.string)
            else:
                response_count = 0
            clap_count_string = article.select_one(
                "div > div > div.u-clearfix.u-paddingTop10 > div.u-floatLeft > div > span > button")
            if clap_count_string != None:
                clap_count = int_from_k_m_string(clap_count_string.string)
            else:
                clap_count = 0
            Articles.objects.update_or_create(title=title, url=article_url, read_time=read_time, published=published,
                                              last_seen=last_seen, publication=publication_obj, archive=archive_obj,
                                              user=user_obj, clap_count=clap_count, response_count=response_count)
            # print(title, read_time, url, user_url, user_name, clap_count, response_count, published, last_seen, "\n")
            Archives.objects.filter(url=url).update(last_seen=last_seen)


def collect_user_info(users):
    """
    Parameters
    ----------
    url: Collection[str]
    """

    for user in users:

        url = user["url"]
        res = requests.get(url=url)

        if res.status_code != 200:
            continue

        bs = BeautifulSoup(res.text, "html.parser")

        # nach reihenfolge - nicht sehr zuverlässig, vll mit regex suchen
        x = bs.findAll("script")[5].string

        a = re.search("(?<=window.__APOLLO_STATE__ = ).*", x).group(0)

        a_json = json.loads(a)

        a_json = list(a_json.items())

        root_query = {}
        main_user = {}

        for a in a_json:
            if a[0] == 'ROOT_QUERY':
                root_query = a[1]
                break

        for a in a_json:
            if 'User:' in a[0]:
                main_user = a[1]
                break

        # user
        main_user_id = main_user.get("id")
        if main_user_id == None:
            main_user_id = main_user.get("user").get("id")

        main_info = main_user["bio"]
        main_full_name = main_user["name"]
        main_user_name = main_user["username"]
        main_image_id = main_user["imageId"]
        main_follower_count = main_user["socialStats"]["followerCount"]
        main_following_count = main_user["socialStats"]["followingCount"]
        main_url = "https://medium.com/@" + main_user_name
        main_user_obj = Users.objects.update_or_create(user_name=main_user_name,
                                                       defaults={"collect_user_info": True, "medium_id": main_user_id,
                                                                 "user_name": main_user_name,
                                                                 "full_name": main_full_name, "info": main_info,
                                                                 "follower_count": main_follower_count,
                                                                 "following_count": main_following_count,
                                                                 "url": main_url, "image_id": main_image_id,
                                                                 "last_updated": datetime.now(
                                                                     timezone(timedelta(hours=0)))})[0]
        print("scraping " + str(main_follower_count) + " followers from " + main_user_name)
        # followers
    #     for i in range(2, len(a_json)-2):
    #         user =  a_json[i][1]
    #         if user.get("__typename") == "User":
    #             user_id = user["id"]
    #             info = user.get("bio")
    #             full_name = user["name"]
    #             user_name = user["username"]
    #             image_id = user.get("imageId")
    #             url = "https://medium.com/@"+user_name
    #             user_obj = Users.objects.get_or_create(user_name = user_name, defaults={"medium_id":user_id, "user_name":user_name, "full_name":full_name, "info":info , "url":url , "image_id":image_id, "last_updated":datetime.now(timezone(timedelta(hours=0))), "collect_user_info":False})[0]
    #             Follower_Relations.objects.update_or_create(user1=main_user_obj, user2=user_obj, date=datetime.now(timezone(timedelta(hours=0))))

    #     next_user = a_json[len(a_json)-3][1]["id"]

    #     fp_query = open("medium_scraper/data/data0.json", "r")
    #     fp_headers = open("medium_scraper/data/headers.json", "r")
    #     query = json.load(fp_query)
    #     headers = json.load(fp_headers)
    #     query["variables"]["paging"]["from"] = next_user
    #     query["variables"]["paging"]["limit"] = 25
    #     query["variables"]["username"] = "@"+main_user_name

    #     while True:

    #         req = requests.post("https://medium.com/_/graphql", json=query, headers=headers)

    #         content = json.loads(req.content)

    #         follower_user_connection = content["data"]["userResult"]["followersUserConnection"]
    #         users = follower_user_connection["users"]
    #         paging_info = follower_user_connection["pagingInfo"]

    #         for user in users:
    #             user_id = user["id"]
    #             info = user["bio"]
    #             full_name = user["name"]
    #             user_name = user["username"]
    #             image_id = user["imageId"]
    #             url = "https://medium.com/@"+user_name
    #             user_obj = Users.objects.get_or_create(user_name = user_name, defaults={"medium_id":user_id, "user_name":user_name, "full_name":full_name, "info":info , "url":url , "image_id":image_id, "last_updated":datetime.now(timezone(timedelta(hours=0))), "collect_user_info":False})[0]
    #             Follower_Relations.objects.update_or_create(user1=main_user_obj, user2=user_obj, date=datetime.now(timezone(timedelta(hours=0))))

    #         if paging_info["next"] == None:
    #             break
    #         elif next_user == paging_info["next"]["from"]:
    #             break
    #         next_user = paging_info["next"]["from"]
    #         query["variables"]["paging"]["from"] = next_user


def save_articles_to_html():
    '''
    Saves html to all articles in the folder .articles
    '''

    counter = 1

    # read filenames in articles folder
    onlyfiles = [f for f in listdir(r'..\\articles\\') if isfile(join(r'..\\articles\\', f))]
    file_ids = [f.replace(".html", "") for f in onlyfiles]

    # for article in Articles.objects.filter(published__year=2021).values():
    for article in Articles.objects.values():
        article_url = article["url"]
        article_id = article["id"]

        file_ids = [f.replace(".html", "") for f in onlyfiles]
        if str(article_id) in file_ids:
            print("--- Article " + str(article_id) + " was already saved")
        else:
            soup_article = get_soup(article_url)
            html = soup_article.prettify("utf-8")

            filename = r'..\\articles\\' + str(article_id) + ".html"

            with open(filename, "wb") as file:
                file.write(html)

            print("Saved article with ID: " + str(article_id))

        counter = counter + 1

        return

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

def extract_image_caption():
    # collect all downloaded .html files
    files_in_articles = listdir(r'./articles')
    file_ids = [f.replace(".html", "") for f in files_in_articles]

    for article in Articles.objects.values():
        article_url = article["url"]
        article_id = article["id"]

        #get all already articles with entries in table figcaptions
        figcaptions = Figcaptions.objects.values()
        figcaptions_articles_ids = [f["article_id"] for f in figcaptions]

        # only start searching for figcaptions if there are no entries in figcaptions table to the article specified
        if article_id not in figcaptions_articles_ids:
            #filename = file.replace(".html","")
            filename = article_id
            file = str(article_id) + ".html"

            # if entries already exist, delete them and continue
            # article = Articles.objects.get(id=filename)
            # Figcaptions.objects.filter(article=article).delete()

            # Fetch the html file
            with open(r"articles/" + file, encoding="utf8") as fp:
                contents = fp.read()
                soup = BeautifulSoup(contents, 'html.parser')

                for figcaption in soup.find_all('figcaption'):
                    #delete HTML element description
                    figcaption = str(figcaption).replace('<figcaption class="jo jp ga fy fz jq jr bf b bg bh dx">', "")
                    figcaption = str(figcaption).replace('<figcaption class="no np ga fy fz nq nr bf b bg bh dx">', "")
                    figcaption = figcaption.replace('</figcaption>', "")

                    #remove newlines
                    figcaption = figcaption.replace("\n", "")

                    #remove spaces
                    figcaption_split = figcaption.split()
                    figcaption_new = " ".join(figcaption_split)

                    try:
                        #create new entries for article
                        figcap = Figcaptions(caption=figcaption_new, article=Articles.objects.get(id=filename))
                        figcap.save()
                        print("************* caption saved")
                    except Exception as e:
                        print("---- Entries could not be saved, something went wrong")
                        print(e)


                print(filename)

        else:
            print("---- figcaptions to article " + str(article_id) + " already saved")

def manually_label_figcaptions():
    '''
    Picks entries in the figcaptions table and asks the user if its a self made image or not
    - Sets the field self_made_manual_label to True
    - Set the field self_made_timestamp to current time
    - Set field self_made = True, if user thinks its a image made by the author
    '''

    figcaptions = Figcaptions.objects.filter(self_made_timestamp__isnull = True)


    for caption in figcaptions:
        print("Is the image with the following figcaption self-made or copied?:")
        print("URL article: " + caption.article.url)
        print("Caption: " + caption.caption)
        print("Was the image created by the author? (y): yes, (n): no:")
        self_made_manually = input()

        if self_made_manually == "y":
            #set self_made_manual_label to True
            caption.self_made_manual_label = True

            # set timestamp
            caption.self_made_timestamp = datetime.now(tz=pytz.UTC)
            caption.save()

            print(caption.caption)
            print("Self-made?: " + str(caption.self_made_manual_label))
            print(caption.self_made_timestamp)
        else:
            #set self_made_manual_label to True
            caption.self_made_manual_label = False

            # set timestamp
            caption.self_made_timestamp = datetime.now(tz=pytz.UTC)
            caption.save()

            print(caption.caption)
            print("Self-made?: " + str(caption.self_made_manual_label))
            print(caption.self_made_timestamp)

# def rule_based_labeling():
#     '''
#     Based on substrings, the function finds images which are most likely made by the author of was copied from another source
#     '''
#     figcaptions = Figcaptions.objects.filter(self_made_timestamp__isnull = True)
#
#     for caption in figcaptions:
#         print(caption.caption)
#         def self_made():
#             #set self_made_manual_label to True
#             caption.self_made_manual_label = True
#
#             # set timestamp
#             caption.self_made_timestamp = datetime.now(tz=pytz.UTC)
#             caption.save()
#
#             print("Image made by author: ")
#             print(caption.caption)
#         def not_self_made():
#             #set self_made_manual_label to True
#             caption.self_made_manual_label = False
#
#             # set timestamp
#             caption.self_made_timestamp = datetime.now(tz=pytz.UTC)
#             caption.save()
#
#             print("Image NOT made by author: ")
#             print(caption.caption)
#
#         if "Image by author" in caption.caption:
#             self_made()
#         if "Unsplash" in caption.caption:
#             not_self_made()

if __name__ == '__main__':
    ## Initial collecting of user info from users that didn't got updated yet
    #user_urls = Users.objects.filter(last_updated__isnull=True, collect_user_info=True).values()
    #collect_user_info(user_urls)

    ## Collect the clap count and voter count for each article
    #how_many_users_clapped()

    ## Save .html for each article
    #save_articles_to_html()

    # Extract image caption from each article
    extract_image_caption()

    # Manually label some captions to create a train data set
    # manually_label_figcaptions()

    # Rule based labeling
    #rule_based_labeling()
