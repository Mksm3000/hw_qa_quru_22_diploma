from selene import browser, have, be, by, command
import allure
from selene import browser, be
from selene.support.shared import browser as shared_browser
from typing import Any, Dict

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions


class AppPage:

    def open_start_page_and_click_continue(self):
        with allure.step('Запуск приложения и нажатие кнопок "Continue"'):
            browser.element((AppiumBy.ID, 'com.glovo:id/splash_permissions_secondary_btn')).click()
            browser.element((AppiumBy.ID, 'com.glovo:id/splash_permissions_secondary_btn')).click()
            browser.element((AppiumBy.ID, 'com.glovo:id/tutorial_confirm_button')).click()
            browser.element((AppiumBy.ID, 'com.glovo:id/tutorial_confirm_button')).click()

    def update_window_detect_and_close(self):
        with allure.step('Появление окошка с предложением обновления и его закрытие'):
            browser.element((AppiumBy.ID, 'com.android.vending:id/0_resource_name_obfuscated')).should(be.visible)
            browser.element((AppiumBy.ACCESSIBILITY_ID, 'Dismiss update dialog')).click()

    def welcome_window_and_email_input(self):
        with allure.step('Появление окошка с приветствием, выбор регистрации через '
                         'email, ввод email и нажатие кнопки "Continue"'):
            browser.element((AppiumBy.XPATH, '//android.widget.TextView[@text="Welcome"]')).should(be.visible)

            browser.element((AppiumBy.XPATH, '//android.widget.TextView[@text="Other methods"]')).click()
            browser.element((AppiumBy.XPATH, '//android.widget.TextView[@text="Email"]')).click()

            browser.element((AppiumBy.XPATH, '//android.widget.EditText['
                                             '@resource-id="emailInput"]')).send_keys('my_test@for_you.com')
            browser.element((AppiumBy.XPATH, '//android.widget.TextView[@text="Continue"]')).click()


app_page = AppPage()
