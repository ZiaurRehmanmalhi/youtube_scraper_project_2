import time


def scroll_to_page_end(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_comment_data(soup):
    all_content = soup.find_all('ytd-comment-thread-renderer')

    data = []
    for comment_data in all_content:
        user_info = comment_data.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
        user_name = user_info.text.strip()
        comment_time = comment_data.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text
        comment_text = comment_data.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer'}).text
        thumbnail_URL = comment_data.find('img', {'class': 'style-scope yt-img-shadow'}).get('src')
        number_of_likes = comment_data.find(
            'span', {'class': 'style-scope ytd-comment-action-buttons-renderer'}
        ).text.strip()
        all_comment_data = {
            "user_name": user_name,
            "comment_time": comment_time,
            "number_of_likes": number_of_likes,
            "comment_text": comment_text,
            "thumbnail_URL": thumbnail_URL
        }
        data.append(all_comment_data)
    return data
