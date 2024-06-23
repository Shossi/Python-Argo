import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def open_headless_firefox_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://0.0.0.0/")
    return driver


def login():
    username = "asd"
    password = "asd"
    driver = open_headless_firefox_driver()
    driver.find_element(By.ID, "Username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    button.click()
    return driver


firefox = login()


def get_location(driver, location):
    driver.find_element(By.NAME, "location").send_keys(location)
    driver.find_element(by=By.NAME, value="weather").click()
    return driver


positive = "Bonji"
negative = "2"


def test_positive():
    assert get_location(firefox, positive).find_element(By.ID, "country")


def test_negative():
    assert get_location(firefox, negative).find_element(By.ID, "not_valid")
    firefox.quit()
