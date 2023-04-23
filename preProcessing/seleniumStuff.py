from selenium import webdriver
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

chromedriver_path = "../selenium/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Sina\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
prefs = {"profile.managed_default_content_settings.images": 2}
options.page_load_strategy = 'normal'
page = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)


class Sel:

    @staticmethod
    def start(uni, program, keywords: list):
        random.seed(datetime.now().microsecond)
        page.get("https://app.copy.ai/projects/25347383?tool=Freestyle&tab=results&sidebar=tools")
        Sel.enter_topic("Application for MSC Admission")
        Sel.enter_keywords([uni,program,keywords])
        while 1:
            pass

    @staticmethod
    def enter_topic(str):
        wait = WebDriverWait(page, 10)
        topic_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#what-are-you-looking-to-create")))
        topic_input.clear()
        Sel.enter_keys_slowly(topic_input, str)

    @staticmethod
    def enter_keywords(string_list):
        wait = WebDriverWait(page, 10)
        elem = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#what-are-the-main-points-you-want-to-cover > div")))
        elem.clear()
        # Create a new <p> tag for each string in the list
        for string in string_list:
            Sel.enter_keys_slowly(elem, string)
            Sel.enter_keys_slowly(elem, Keys.ENTER)

    @staticmethod
    def generate_text():
        elem = page.find_element(By.XPATH,
                                 "//*[@id=\"__next\"]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/div[1]/div[2]/div[1]/form/div[3]/div/button")
        page.execute_script("arguments[0].click();", elem)
        elem.click()

    @staticmethod
    def enter_keys_slowly(input_elem, string):
        speed_wpm = random.randint(80, 120)
        time_to_sleep = (60 / (speed_wpm * 5))
        for char in string:
            input_elem.send_keys(char)
            sleep(abs(time_to_sleep + random.uniform(-0.1, 0.1)))
