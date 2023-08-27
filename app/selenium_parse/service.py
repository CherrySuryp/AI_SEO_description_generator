import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import pickle


class MpsParser:
    def __init__(self):
        self._cookies_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cookies")

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().googlechrome}")

        self._driver = webdriver.Chrome(options=options)
        self._driver.maximize_window()

    def check_cookies(self) -> bool:
        return os.path.exists(self._cookies_path)

    def inject_cookies(self) -> None:
        for cookie in pickle.load(open(self._cookies_path, "rb")):
            self._driver.add_cookie(cookie)
        print("Cookies injected")

    def authorize(self) -> None:
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

        pickle.dump(self._driver.get_cookies(), open("cookies", "wb"))
        print("Cookies saved")

    def service(self):
        try:
            if self.check_cookies():
                print("Cookies found")

                self._driver.get("https://mpstats.io")
                self.inject_cookies()
                self._driver.refresh()
                time.sleep(60)
            else:
                print("Getting cookies")
                self.authorize()

        except Exception as ex:
            print(ex)

        finally:
            self._driver.close()
            self._driver.quit()


MpsParser().service()
print("Git!")