from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


from time import sleep
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import random
#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('W1iFrhuHEPdo8z9ewYqvRKCyFjHWlrlqHkoaJ98nO7diOjgiBPlIrPJqmGJhjj4mOVKNxhSLbW0AYvDc0WsAJZ7IymPR1rvvlP8jyXLwo6aZUyAtnkIhD5t15U5kLVX/qW94ubH5WSyhpPnhLvxzywdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d5cd857c17c8ff9466f3f7817a5980b8')
line_bot_api.push_message('U6a9e45ef42f84e15883c1dd23c20badd',TextSendMessage(text='連接成功'))

#############
        


driver = webdriver.Chrome()

def search(ingredient):
    url = "https://icook.tw/"
    driver.get(url)
    sleep(2)
    search_box = driver.find_element(By.CLASS_NAME, "search-input")
    search_box.clear()
    search_box.send_keys(ingredient)
    search_box.send_keys(Keys.RETURN)
    sleep(2)
    original_html = driver.page_source
    return original_html

def progress_bar(percentage, length):  # 進度條
    # 确保百分比在 0 到 100 之间
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100
    # 计算填充部分的长度
    filled_length = int(length * percentage // 100)
    bar = "■" * filled_length + "□" * (length - filled_length)
    # 輸出進度條
    return f"|{bar}|"

def get_result(original_html,search_ingredient):
    soup = BeautifulSoup(original_html, "html.parser")
    recipe_list = []
    while True:
        recipe = soup.select('.browse-recipe-card')
        recipe_items = soup.find_all("li", class_="browse-recipe-item")
        for recipe in recipe_items:
            link_tag = recipe.find("a", class_="browse-recipe-link")
            if link_tag and link_tag.has_attr("href"):
                link = link_tag["href"]
                title = recipe.find('h2').get_text(strip=True)
                ingredients = recipe.find('p').get_text(strip=True)
                likes_elem = recipe.select_one('li.browse-recipe-meta-item[data-title*="讚"]')
                time_elem = recipe.select_one('li.browse-recipe-meta-item[data-title*="烹飪時間"]')
                like_count = 0
                cook_time = "未知"
                if likes_elem:
                    likes_text = likes_elem.get_text(strip=True).replace('讚', '').strip()
                    if likes_text.isdigit():
                        like_count = int(likes_text)
                if time_elem:
                    cook_time = time_elem.get_text(strip=True).replace('烹飪時間', '').strip()
                recipe_list.append({
                    "title": title,
                    "ingredients": list(ingredients.split("、")),
                    "likes": like_count,
                    "cook_time": cook_time,
                    "link": f"https://icook.tw{link}"
                })
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.pagination-tab.page--next a.pagination-tab-link')
            next_button.click()
            sleep(2)
            original_html = driver.page_source
            soup = BeautifulSoup(original_html, "html.parser")
        except Exception as e:
            #print("已到最後一頁或找不到下一頁按鈕", e)
            break
    recipe_list.sort(key=lambda x: x["likes"], reverse=True)
    top_recipes = recipe_list[:10]
    search_ingredient = list(search_ingredient.strip().split(" "))
    results = []
    for idx, recipe in enumerate(top_recipes, 1):
        complete_percent = int(
            round(len(search_ingredient) / len(recipe["ingredients"]), 2) * 100
        )
        left = len(recipe["ingredients"]) - len(search_ingredient)
        
        result = (f"""{idx}. {recipe['title']}
    {recipe['likes']} 次讚 - 烹飪時間: {recipe['cook_time']}
    材料完成度： {complete_percent} % Complete - 差{left}樣 
    {progress_bar(complete_percent, length = 10)}
    {'、'.join(recipe["ingredients"])}
""")
        results.append(result)
    
    return top_recipes, results
        
        

#############
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

    
def finding(ingredient):
    message = TextSendMessage(get_result(search(ingredient),ingredient))
    return message
    


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ingredient = event.message.text
    message = finding(ingredient)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


        
# # 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text
#     if '找食譜' in msg:
#         message = find_recipes()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '吃甚麼' in msg:
        
#     elif '最新活動訊息' in msg:
#         message = buttons_message()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '註冊會員' in msg:
#         message = Confirm_Template()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '旋轉木馬' in msg:
#         message = Carousel_Template()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '圖片畫廊' in msg:
#         message = test()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '功能列表' in msg:
#         message = function_list()
#         line_bot_api.reply_message(event.reply_token, message)
#     else:
#         message = TextSendMessage(text=msg)
#         line_bot_api.reply_message(event.reply_token, message)

# @handler.add(PostbackEvent)
# def handle_message(event):
#     print(event.postback.data)


# @handler.add(MemberJoinedEvent)
# def welcome(event):
#     uid = event.joined.members[0].user_id
#     gid = event.source.group_id
#     profile = line_bot_api.get_group_member_profile(gid, uid)
#     name = profile.display_name
#     message = TextSendMessage(text=f'{name}歡迎加入')
#     line_bot_api.reply_message(event.reply_token, message)
        
        
