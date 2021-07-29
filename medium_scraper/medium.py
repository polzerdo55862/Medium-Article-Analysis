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
from os import listdir
from os.path import isfile, join
import json


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


if __name__ == '__main__':
    ### Initial collecting of user info from users that didn't got updated yet
    user_urls = Users.objects.filter(last_updated__isnull=True, collect_user_info=True).values()
    collect_user_info(user_urls)