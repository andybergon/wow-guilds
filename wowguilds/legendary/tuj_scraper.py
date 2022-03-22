# Needed to use Selenium as API is "crypted" and `HTMLSession().get(url).html.render()` of 'requests-html' was not working
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from wowguilds.legendary.items import SPECTRAL_FLASK_OF_POWER


def get_house_id(server_name):
    # can get from https://theunderminejournal.com/api/realms.php
    return 227


def get_from_api(server_name):
    house_id = get_house_id(server_name)
    # item_url = f'https://theunderminejournal.com/api/item.php?house={house_id}&item={item_id}&e=1'


def get_price(server_name, item_id):
    item_url = f'https://theunderminejournal.com/#eu/{server_name}/item/{item_id}'

    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    driver.get(item_url)
    el = driver.find_element(by=By.XPATH, value='//*[@class="current-price"]')  # TODO
    # print(el)
    driver.close()


if __name__ == '__main__':
    get_price('nemesis', SPECTRAL_FLASK_OF_POWER.id)
