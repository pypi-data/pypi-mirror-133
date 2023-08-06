import os
from time import sleep

from linkedin_scraper import actions
from selenium import webdriver

from clean_html import get_headline
from excel_db import create_sheet
from prompt import location, password, position, username

# Initialize chrome driver
PATH = './chromedriver'

if os.path.exists(PATH) is None:
    raise Exception(
        "Error Chromedriver not found please download the latest from https://sites.google.com/chromium.org/driver/")

if os.path.exists(".env") is None:
    raise Exception(
        "Please add the environment variables for the following items see: .env.example")

driver = webdriver.Chrome(PATH)

WEBSITE = "https://www.linkedin.com/"

actions.login(driver, username, password)


def pull_linkedin():
    main_url = f"https://duckduckgo.com/?q=site%3Alinkedin.com%2Fin%2F+AND+%22{position}%22+AND+%22{location}%22&atb=v295-2__&ia=web"
    driver.get(
        main_url
    )

    linkedin_urls = driver.find_elements_by_class_name('result__url')
    linkedin_urls = [url.text for url in linkedin_urls]

    sleep(4)
    for i, value in enumerate(linkedin_urls):
        url = value.replace('› in ›', '/in/').replace(' ', '')
        driver.get(url)
        j = i
        sleep(6)
        check_profile_null = get_headline(driver.page_source)

        if check_profile_null is not None:
            append_sheet2 = create_sheet(j, driver.page_source)
            print("Success Person---- added", append_sheet2)


if __name__ == '__main__':
    pull_linkedin()
