import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_ratings():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    teams = []
    ratings = []

    driver.get(
        "https://projects.fivethirtyeight.com/soccer-predictions/premier-league/")

    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    for name_item in soup.findAll('tr', class_="team-row"):
        title_element = name_item["data-str"]
        teams.append(title_element.strip())

    for rating_item in soup.findAll('td', class_="num rating overall drop-6"):
        rating_element = rating_item["data-val"]
        rating_element = round(float(rating_element), 2)
        ratings.append(rating_element)

    spi_start_values = {teams[i]: ratings[i] for i in range(len(teams))}
    return spi_start_values
