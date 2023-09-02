import sys
import os
import json
import pickle

from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from fake_useragent import UserAgent

import sentry_sdk

sys.path.append("..")
from app.config import ProdSettings  # noqa


class Parser:
    def __init__(self, keywords_count: int = 30):
        self._settings = ProdSettings()
        self._cookies_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cookies")

        self._keywords_count = keywords_count

        options = webdriver.ChromeOptions()
        user_agent = UserAgent().googlechrome
        print(user_agent)
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=options)
        # self._driver.set_window_size(1000, 600)
        self._driver.maximize_window()

    def _check_cookies(self) -> bool:
        """
        Проверка наличия сохраненное сессии
        """
        return os.path.exists(self._cookies_path)

    def _inject_cookies(self) -> None:
        """
        Инъекция cookie для авторизации
        """
        for cookie in pickle.load(open(self._cookies_path, "rb")):
            self._driver.add_cookie(cookie)

    def _authorize(self, save_cookies: bool = False) -> None:
        """
        Авторизация на сайте с сохранением cookie в файл
        """
        self._driver.get("https://mpstats.io/login")
        email_input = self._driver.find_element(By.ID, "email")
        passwd_input = self._driver.find_element(By.NAME, "password")

        email_input.clear()
        email_input.send_keys(self._settings.MPSTATS_LOGIN)
        passwd_input.clear()
        passwd_input.send_keys(self._settings.MPSTATS_PASS)
        passwd_input.send_keys(Keys.ENTER)

        if save_cookies:
            pickle.dump(self._driver.get_cookies(), open("cookies", "wb"))
            print("Cookies saved")

    def _auth_pipeline(self):
        """
        Авторизации или инъекции cookie по условиям
        """
        if self._check_cookies():
            self._driver.get("https://mpstats.io/login")
            self._inject_cookies()
            self._driver.refresh()
            print("Cookies injected")

            if self._driver.current_url == "https://mpstats.io/doubleSession":
                print("Double Session")
                self._authorize()

        else:
            print("Getting cookies")
            self._authorize(save_cookies=True)

    def _top_similar_item(self, wb_sku: int) -> int:
        """
        Переход к ТОП-1 похожему товару
        """
        self._driver.get(f"https://mpstats.io/wb/item/{wb_sku}")
        elements = self._driver.find_elements(
            By.XPATH, "//a[@href and @title='Открыть в Wildberries' and " "@target='_blank']"
        )
        return int([i.text for i in elements][0])

    def _get_keywords(self, sku: int) -> Dict[str, int]:
        """
        Парсинг ключевых слов со страницы https://mpstats.io/wb/item/{sku}
        """
        self._driver.get(f"https://mpstats.io/wb/item/{sku}")
        self._driver.execute_script("document.body.style.zoom = '30%'")

        kw_json = {}
        while len(kw_json) <= self._keywords_count:
            scroll_table = WebDriverWait(self._driver, 10).until(
                ec.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="mp-stats-app"]/div[2]/div/section/div[5]'
                        '/div[2]/div[1]/div/div/div/div[2]/div[2]/div[3]',
                    )
                )
            )
            keywords = self._driver.find_elements(By.XPATH, '//a[@title="Информация по ключевому слову"]/span')
            count = self._driver.find_elements(By.XPATH, '//div[@col-id="wb_count"]')
            keywords = [i.text for i in keywords]
            count = [i.text for i in count][3:]

            for keyword, kw_count in zip(keywords, count):
                kw_json[keyword] = int(kw_count.replace(" ", ""))

            self._driver.execute_script("arguments[0].scrollTop += 100;", scroll_table)

        json.dump(kw_json, open("keywords.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("Json dumped")

        return kw_json

    def parse_mpstats(self, wb_sku: int) -> Dict[str, int] | None:
        """
        Вызов бизнес логики
        """
        try:
            self._auth_pipeline()
            top_item_sku = self._top_similar_item(wb_sku=wb_sku)
            return self._get_keywords(top_item_sku)

        except Exception as ex:
            sentry_sdk.capture_exception(ex)
            return None

        finally:
            self._driver.close()
            self._driver.quit()

    def get_wb_item_params(self):
        """
        WIP
        """
        self._driver.get("https://www.wildberries.ru/catalog/74643153/detail.aspx")

        button = WebDriverWait(self._driver, 10).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    "// button[text() = 'Развернуть характеристики']"
                )
            )
        )
        self._driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()

        product_params_decor = self._driver.find_elements(
                    By.CLASS_NAME,
                    "product-params__cell-decor"
                )

        product_params_info = self._driver.find_elements(
            By.CLASS_NAME,
            "product-params__cell"
        )

        product_params_decor = [i.text for i in product_params_decor if i.text != '']
        product_params_info = [i.text for i in product_params_info if i.text not in product_params_decor and i.text != '']

        # print(len(product_params_decor), len(product_params_info))
        result = {decor: info for decor, info in zip(product_params_decor, product_params_info)}
        json.dump(result, open("result.json", "w"), ensure_ascii=False, indent=1)
