import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, have


class AppPage:

    def open_start_page_and_click_continue(self):
        with allure.step(
                'Открытие окна "Explore local stores" и нажатие кнопки "Not now"'):
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/splash_permissions_title')).should(have.text('Explore local stores'))
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/splash_permissions_secondary_btn')).click()

        with allure.step('Открытие окна "Track your order" и нажатие кнопки "Not now"'):
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/splash_permissions_title')).with_(
                timeout=10).should(have.text('Track your order'))
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/splash_permissions_secondary_btn')).click()

        with allure.step(
                'Открытие окна "Order from any store or restaurant in your city" и '
                'нажатие кнопки "Next"'):
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/fragment_welcome_tutorial_text')).should(
                have.text('any store or restaurant'))
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/tutorial_confirm_button')).click()

        with allure.step(
                'Открытие окна "Couriers pick up your order and bring it to you in '
                'minutes" и нажатие кнопки "Continue"'):
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/fragment_welcome_tutorial_text')).should(
                have.text('Couriers pick up your order'))
            browser.element(
                (AppiumBy.ID, 'com.glovo:id/tutorial_confirm_button')).click()

    def update_window_detect_and_close(self):
        with allure.step('Появление окошка с предложением обновления и его закрытие'):
            browser.element((AppiumBy.ID,
                             'com.android.vending:id/0_resource_name_obfuscated')).should(
                be.visible)
            browser.element(
                (AppiumBy.ACCESSIBILITY_ID, 'Dismiss update dialog')).click()

    def welcome_window_and_email_input(self):
        with allure.step('Появление окошка с приветствием, выбор регистрации через '
                         'email, ввод email и нажатие кнопки "Continue"'):
            browser.element(
                (AppiumBy.XPATH, '//android.widget.TextView[@text="Welcome"]')).should(
                be.visible)
            browser.element((AppiumBy.XPATH,
                             '//android.widget.TextView[@text="Other methods"]')).click()
            browser.element(
                (AppiumBy.XPATH, '//android.widget.TextView[@text="Email"]')).click()

            browser.element((AppiumBy.XPATH,
                             '//android.widget.EditText[@resource-id="emailInput"]')).send_keys(
                'my_test@for_you.com')
            browser.element(
                (AppiumBy.XPATH, '//android.widget.TextView[@text="Continue"]')).click()


app_page = AppPage()
