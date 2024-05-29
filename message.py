#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
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

# from selenium import webdriver
# from linebot.models import *
# from flex_msg import *
# from config import *
# import time
# import random
# import string

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
        recipes = soup.select('.browse-recipe-card')
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


#TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
def finding():
    ingredient = find()
    message = TextSendMessage(
        text = get_result(search(ingredient),ingredient)
    )
    return message
    
#關於LINEBOT聊天內容範例
