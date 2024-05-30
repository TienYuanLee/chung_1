#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# from app import *
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup

# driver = webdriver.Chrome()

# def search(ingredient):
#     # out = '、'.join(ingredient.strip().split(" "))
#     # print(f'幫你搜尋有關{out}的食譜喔 !')
#     url = "https://icook.tw/"
#     driver.get(url)
#     sleep(2)
#     search_box = driver.find_element(By.CLASS_NAME, "search-input")
#     search_box.clear()
#     search_box.send_keys(ingredient)
#     search_box.send_keys(Keys.RETURN)
#     sleep(2)
#     original_html = driver.page_source
#     return original_html

# def progress_bar(percentage, length):  # 進度條
#     # 确保百分比在 0 到 100 之间
#     if percentage < 0:
#         percentage = 0
#     elif percentage > 100:
#         percentage = 100
#     # 计算填充部分的长度
#     filled_length = int(length * percentage // 100)
#     bar = "■" * filled_length + "□" * (length - filled_length)
#     # 輸出進度條
#     return f"|{bar}|"

# def get_result(original_html,search_ingredient):
#     soup = BeautifulSoup(original_html, "html.parser")
#     recipe_list = []
#     for i in range(2): #可以改變翻頁次數，每頁有18道菜
#         recipes = soup.select('.browse-recipe-card')
#         recipe_items = soup.find_all("li", class_="browse-recipe-item")
#         for recipe in recipe_items:
#             link_tag = recipe.find("a", class_="browse-recipe-link")
#             if link_tag and link_tag.has_attr("href"):
#                 link = link_tag["href"]
#                 title = recipe.find('h2').get_text(strip=True)
#                 ingredients = recipe.find('p').get_text(strip=True)
#                 likes_elem = recipe.select_one('li.browse-recipe-meta-item[data-title*="讚"]')
#                 time_elem = recipe.select_one('li.browse-recipe-meta-item[data-title*="烹飪時間"]')
#                 like_count = 0
#                 cook_time = "未知"
#                 if likes_elem:
#                     likes_text = likes_elem.get_text(strip=True).replace('讚', '').strip()
#                     if likes_text.isdigit():
#                         like_count = int(likes_text)
#                 if time_elem:
#                     cook_time = time_elem.get_text(strip=True).replace('烹飪時間', '').strip()
#                 recipe_list.append({
#                     "title": title,
#                     "ingredients": list(ingredients.split("、")),
#                     "likes": like_count,
#                     "cook_time": cook_time,
#                     "link": f"https://icook.tw{link}"
#                 })
#         try:
#             next_button = driver.find_element(By.CSS_SELECTOR, 'li.pagination-tab.page--next a.pagination-tab-link')
#             next_button.click()
#             sleep(2)
#             original_html = driver.page_source
#             soup = BeautifulSoup(original_html, "html.parser")
#         except Exception as e:
#             #print("已到最後一頁或找不到下一頁按鈕", e)
#             break
#     recipe_list.sort(key=lambda x: x["likes"], reverse=True)
#     top_recipes = recipe_list[:10]
#     search_ingredient = list(search_ingredient.strip().split(" "))
#     results = []
#     for idx, recipe in enumerate(top_recipes, 1):
#         complete_percent = int(
#             round(len(search_ingredient) / len(recipe["ingredients"]), 2) * 100
#         )
#         left = len(recipe["ingredients"]) - len(search_ingredient)
#         ############這裡改result########
#         result = TextSendMessage (text  = (f"""{idx}. {recipe['title']}
#     {recipe['likes']} 次讚 - 烹飪時間: {recipe['cook_time']}
#     材料完成度： {complete_percent} % Complete - 差{left}樣 
#     {progress_bar(complete_percent, length = 10)}
#     {'、'.join(recipe["ingredients"])}
# """))
#         results.append(result)
    
#     return top_recipes, results


# def selection(num, top_recipes):
#     selected_recipe = top_recipes[num - 1]
#     recipe_link = selected_recipe['link']
#     driver.get(recipe_link)
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
#     page_source = driver.page_source
#     soup = BeautifulSoup(page_source, "html.parser")
#     recipe_title = soup.find('h1').get_text(strip=True)
#     ingredients_section = soup.find('div', class_='recipe-details-ingredients')
#     ingredients = []
#     if ingredients_section:
#         ingredient_items = ingredients_section.find_all('li', class_='ingredient')
#         for item in ingredient_items:
#             name = item.find('div', class_='ingredient-name').get_text(strip=True)
#             quantity = item.find('div', class_='ingredient-unit').get_text(strip=True)
#             ingredients.append(f"{name} {quantity}")
#     steps_section = soup.find('ul', class_='recipe-details-steps')
#     steps = []
#     if steps_section:
#         step_items = steps_section.find_all('li', class_='recipe-details-step-item')
#         for index, item in enumerate(step_items, start=1):
#             step_description = item.find('p', class_='recipe-step-description-content').get_text(strip=True)
#             steps.append(f"Step {index}: {step_description}")
    
#     result = {
#         "title": recipe_title,
#         "cook_time": selected_recipe['cook_time'],
#         "ingredients": ingredients,
#         "steps": steps
#     }
    
#     return result

# n = input()
# top_recipes, results = get_result(search(n),n)
# for result in results:
#     print(result)


# #TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
# def finding():
#     ingredient = find()
#     message = TextSendMessage(
#         text = get_result(search(ingredient),ingredient)
#     )
#     return message
    
#關於LINEBOT聊天內容範例
