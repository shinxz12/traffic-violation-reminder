from typing import Literal, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from io import BytesIO
import traceback

from phatnguoi.exceptions import WrongCapchaException
from .constants import VehicleType
from .capcha import decode_capcha


class VehicleChecker:
    def __init__(self, number_plate: str, vehicle_type: Literal["CAR", "MOTOBIKE", "ELECTRIC_BIKE"]) -> None:
        self.number_plate = number_plate
        self.vehicle_type = getattr(VehicleType, vehicle_type)
        self.driver = self.init_selenium()

    def init_selenium(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--allow-running-insecure-content")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        return driver

    def _check(self) -> Optional[WebElement]:
        self.driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
        capcha_element = self.driver.find_element(By.ID, "imgCaptcha")
        capcha_img = BytesIO(capcha_element.screenshot_as_png)
        capcha_text = decode_capcha(capcha_img)
        number_plate = self.driver.find_element(By.NAME, "BienKiemSoat")
        self.driver.find_element(
            By.XPATH, f"//select[@name='LoaiXe']/option[@value='{self.vehicle_type}']"
        ).click()
        number_plate.send_keys(self.number_plate)
        self.driver.find_element(By.NAME, "txt_captcha").send_keys(capcha_text)
        self.driver.find_element(By.CLASS_NAME, "btnTraCuu").click()
        errors = bool(
            self.driver.find_elements(By.XPATH, "//span[text()='Chưa xử phạt']")
        )
        if errors:
            body = self.driver.find_element(By.ID, "bodyPrint123")
            height = self.driver.execute_script(
                "return document.documentElement.scrollHeight"
            )
            width = self.driver.execute_script(
                "return document.documentElement.scrollWidth"
            )
            self.driver.set_window_size(width, height)
            return body

        is_wrong_capcha = bool(
            self.driver.find_elements(By.XPATH, "//div[text()='Mã xác nhận sai!']")
        )
        if is_wrong_capcha:
            raise WrongCapchaException()

    def check(self) -> Optional[WebElement]:
        retries = 0
        result = None
        while retries < 10:
            try:
                result = self._check()
                break
            except WrongCapchaException:
                print("Capcha is wrong!")
            except:
                traceback.print_exc()
            retries += 1
        return result
