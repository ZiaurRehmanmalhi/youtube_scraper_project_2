from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def create_csv(channel_link):
    channel_username = channel_link.split("com/")[-1].replace('@', '')
    if not os.path.exists(channel_username):
        os.makedirs(channel_username)
    driver = webdriver.Chrome()
    driver.get(channel_link)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_content = soup.find_all('ytd-rich-grid-media')

    for video_data in all_content:
        video_title = video_data.find('a', {'id': 'video-title-link'}).text.strip()
        video_link = 'https://www.youtube.com' + video_data.find('a', {'id': 'video-title-link'}).get('href')

        driver.get(video_link)
        time.sleep(4)

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
            time.sleep(4)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_content = soup.find_all('ytd-comment-thread-renderer')

        data = []
        for comment_data in all_content:
            user_info = comment_data.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
            user_name = user_info.text.strip()
            comment_time = comment_data.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text
            comment_text = comment_data.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer'}).text
            thumbnail_URL = comment_data.find('img', {'class': 'style-scope yt-img-shadow'}).get('src')
            number_of_likes = comment_data.find('span', {
                'class': 'style-scope ytd-comment-action-buttons-renderer'}).text.strip()

            all_data = [user_name, comment_time, comment_text, thumbnail_URL, number_of_likes]
            data.append(all_data)

        df = pd.DataFrame(data,
                          columns=['Username', 'Comment Time', 'Comment Text', 'Thumbnail URL', 'Number of Likes'])
        df.to_csv(os.path.join(channel_username, video_title.replace('/', '|') + '.csv'), index=False)

    driver.quit()
