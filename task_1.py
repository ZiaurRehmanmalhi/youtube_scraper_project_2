from selenium import webdriver
from bs4 import BeautifulSoup
from utils import scroll_to_page_end, extract_comment_data
import pandas as pd


driver = webdriver.Chrome()
url = "https://www.youtube.com/watch?v=zghBofrKv7s&ab_channel=EhmadZubair"
driver.get(url)
scroll_to_page_end(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
data = extract_comment_data(soup)

dataframe = pd.DataFrame(data)
video_title = soup.title.string
file_name = f"{video_title}.csv"
dataframe.to_csv(file_name, index=False)
print("Data saved to csv file")
