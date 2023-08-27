import json
import os
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import pickle


class MpsParser:
    def __init__(self, wb_sku: int):
        self.wb_sku = wb_sku
        self._cookies_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cookies")

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().googlechrome}")

        self._driver = webdriver.Chrome(options=options)
        self._driver.set_window_size(1000, 600)

    def authorize(self, save_cookies: bool = False) -> None:
        self._driver.get("https://mpstats.io/login")
        email_input = self._driver.find_element(By.ID, "email")
        passwd_input = self._driver.find_element(By.NAME, "password")

        email_input.clear()
        email_input.send_keys("timfcsm@yandex.ru")
        time.sleep(1.5)
        passwd_input.clear()
        passwd_input.send_keys("MPstats2023")
        time.sleep(0.3)
        passwd_input.send_keys(Keys.ENTER)

        if save_cookies:
            pickle.dump(self._driver.get_cookies(), open("cookies", "wb"))
            print("Cookies saved")

    def check_cookies(self) -> bool:
        return os.path.exists(self._cookies_path)

    def inject_cookies(self) -> None:
        for cookie in pickle.load(open(self._cookies_path, "rb")):
            self._driver.add_cookie(cookie)
        print("Cookies injected")

    def top_similar_item(self) -> int:
        self._driver.get(f"https://mpstats.io/wb/item/{self.wb_sku}")
        elements = self._driver.find_elements(By.XPATH, "//a[@href and @title='Открыть в Wildberries' and "
                                                        "@target='_blank']")
        return int([i.text for i in elements][0])

    def get_keywords(self, sku: int):
        self._driver.get(f"https://mpstats.io/wb/item/{sku}")
        span_elements = self._driver.find_elements(By.XPATH, "//a[@href and @target='_blank']/span")
        json.dump(
            [i.text for i in span_elements], open("keywords.json", "w", encoding="utf8"), ensure_ascii=False, indent=1
        )

    def service(self):
        try:
            if self.check_cookies():
                print("Cookies found")

                self._driver.get("https://mpstats.io")
                self.inject_cookies()
                self._driver.refresh()
                if self._driver.current_url == "https://mpstats.io/doubleSession":
                    print("Double Session")
                    self.authorize()
                time.sleep(2)
            else:
                print("Getting cookies")
                self.authorize(save_cookies=True)
                print(self._driver.current_url)

            top_item_sku = self.top_similar_item()
            self.get_keywords(top_item_sku)
            time.sleep(20)

        except Exception as ex:
            print(ex)

        finally:
            self._driver.close()
            self._driver.quit()


MpsParser(wb_sku=100076915).service()
