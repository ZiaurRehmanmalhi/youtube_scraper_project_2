from utils_task_2 import create_csv

url = input("Enter Any Youtube Chanel URL: ")
url += "/videos"

create_csv(url)
print("Data successfully saved to csv files.")
