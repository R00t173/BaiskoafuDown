import requests
import string
import random
import json
import config
import baiskoafu_download_manager



login_url   = "https://admin.baiskoafu.com/api/v1.92/user/login/"
search_url  = "https://admin.baiskoafu.com/api/v1.92/search/"
prmm_url    = "https://admin.baiskoafu.com/api/v1.92/user/change-primary-device/"
VIDEO_CDN   = "https://dffhiy8lbgb51.cloudfront.net/"
AUDIO_CDN   = "https://d1g98ytv3fry8t.cloudfront.net/"


KEY_LEN = 32

def chars():
    return (string.ascii_letters+string.digits)  

def gen():
    keylist = [random.choice(chars()) for i in range(KEY_LEN)]
    return ("".join(keylist))

def login(username, password, query=""):
    AUTH = {
        "device_token": f"{gen()}",
        "device_type": "android",
        "email": f"{username}",
        "password": f"{password}",
        "unique_device_id": f"{gen()}"
        }

    resp = requests.session()
    resp.post(login_url, data=AUTH)
    r = resp.post(login_url, data=AUTH)

    userinfo    = json.loads(r.text)
    
    if "The password you entered is incorrect." in str(userinfo['message']):
        print("The password you entered is incorrect.")
        baiskoafu_download_manager.wait(3)
        exit()
    
    if "Login Successful" in userinfo['message']:

        FIRST_NAME  = userinfo['user']['first_name']
        LAST_NAME   = userinfo['user']['last_name']
        TOKEN	    = userinfo['user']['access_token']
        DEVICE_ID	= userinfo['user']['device_id']
        PRIMARY	    = userinfo['user']['subscription']
        ID_AUTH     = {"Authorization": f"JWT {TOKEN}"}

        print(f"Hi, {FIRST_NAME} {LAST_NAME}")

        if config.IS_PRIMARY_DEVICE and  str(PRIMARY) == "Premium":

            primary = resp.patch(prmm_url, data={"device_id" : f"{DEVICE_ID}"}, headers=ID_AUTH)

        def search_engine():

            if query == "":
                search_query = input("Search for songs, movies, series to download\nSEARCH :  ")
            else: search_query = query
            baiskoafu_download_manager.clear()
            if search_query.lower() == "return 0":
                exit()
            if search_query == "" or None:
                search_engine()
            
            SEARCH_DATA = {
            "category_name": "All",
            "device_id": f"{DEVICE_ID}",
            "search_keyword": f"{search_query}"
            }

            ids = resp.post(search_url, data=SEARCH_DATA, headers=ID_AUTH)
            dummy = json.loads(ids.text)
            
            I = ['ID', 'TYPE', 'FILE NAME']
            print(f'{I[0]:<5} | {I[1]:<6} | {I[2]:<5}')
            print('_' * 50)
            search_result = 0

            for i in dummy['data']:

                try:
                    for i in i['items']:

                        ITEM_ID         = i['item_id']
                        ITEM_TITLE      = i['item_title'][0:30]
                        CONTENT_TYPE    = i['content_type']
                        ITEM_CONTENT_M	= i['item_content_url']
                        ITEM_TITLE = ITEM_TITLE if len(ITEM_TITLE) < 30 else ITEM_TITLE + "..."
                        print(f'{ITEM_ID :<5} | {CONTENT_TYPE :<6} | {ITEM_TITLE : <5}')
                        search_result += 1

                except IndexError: pass
                except KeyError: pass

            if search_result == 0:

                print("\nNo results :(\nSearching for series? try with episode name.\n")
                search_engine()
        
            def user_choice():

                choice_list = []
                print('_' * 50)
                try:
                    choice = int(input("Enter ID number to download : "))
                    baiskoafu_download_manager.clear()
                    if choice == 0:
                        exit()
                    if choice == 1:
                        search_engine()
                except ValueError:
                    print("INVALID ID NUMBER! TRY AGAIN")
                    user_choice()

                for i in dummy['data']:

                    try:
                        for i in i['items']:
                            ITEM_ID         = i['item_id']
                            ITEM_TITLE      = i['item_title']
                            CONTENT_TYPE    = i['content_type']
                            ITEM_CONTENT_M	= i['item_content_url']

                            if choice == int(ITEM_ID):

                                if CONTENT_TYPE == "audio":
                                    choice_list.append(str(ITEM_TITLE)+'.mp3')
                                else: choice_list.append(str(ITEM_TITLE)+'.mp4')    # index 0 -- > Title
                                choice_list.append(CONTENT_TYPE)
                                choice_list.append(ITEM_CONTENT_M)
  

                    except IndexError: pass
                    except KeyError: pass
                
                if len(choice_list) == 3:

                    if choice_list[2] == "": # empty links
                        print("URL not found!")
                        baiskoafu_download_manager.wait(5)
                        search_engine() # TODO go to main

                    filename = choice_list[0]
                    if choice_list[1] == 'audio':
                        cdn_url = f"{AUDIO_CDN}{choice_list[2]}"
                    else:
                        cdn_url = f"{VIDEO_CDN}{choice_list[2]}"
                    
                    resp_cdn = requests.get(cdn_url)
                    resp_cdn_data = resp_cdn.text.split('\n')
                    high_med_low = []
                    base_url = cdn_url.split('/')
                    base_url.pop(-1)
                    base_url = "/".join(base_url) + "/"
                    
                    for m3 in resp_cdn_data:
                        if m3.endswith('m3u8'):
                            high_med_low.append(m3)

                    if config.media_quality() == 'low':
                        base_url += high_med_low[2]         #  -- > low 
                    if config.media_quality() == 'medium':
                        base_url += high_med_low[1]         #  -- > medium
                    if config.media_quality() == 'high':
                        base_url += high_med_low[0]         #  -- > high

                    baiskoafu_download_manager.get_ts_files(base_url)
                    baiskoafu_download_manager.download()
                    baiskoafu_download_manager.combine(filename)

            user_choice()

        search_engine()
