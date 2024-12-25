from selene import browser, have, be, by, command
import allure


class MainPage:

    def open(self):
        with allure.step('Открываем главную страницу'):
            browser.open('')
            try:
                # закрываем всплывающий баннер
                browser.element('.banner-close-button').should(be.visible).click()
            finally:
                pass

    def login_button_click(self):
        with allure.step("Нажимаем кнопку 'Login'"):
            login_button = browser.element(
                '[class="unified-header-desktop__right"]>[data-test-id="login-button"]')
            login_button.should(be.visible)
            login_button.click()

    def email_button_click(self):
        with allure.step("Нажимаем кнопку 'Email'"):
            try:
                # ожидаем появление модального окна
                browser.element('#base-modal').should(be.visible)
            except:
                pass
            finally:
                email_button = browser.element('[data-test-id="email-button"]')
                email_button.should(be.visible)
                email_button.click()

    def continue_button_click(self):
        continue_button = browser.element('[data-test-id="submit-button"]')
        continue_button.click()

    def email_input(self, email):
        with allure.step('Вводим email: ' + email):
            email_field = (browser.element('[data-test-id="email-input"]').
                           element('[data-testid="input"]'))
            email_field.send_keys(email)
            self.continue_button_click()

    def password_input(self, password):
        with allure.step('Вводим password: ' + password):
            password_field = browser.element('input[data-testid="input"][type="password"]')
            password_field.send_keys(password)
            self.continue_button_click()

    def name_input(self, name):
        with allure.step('Вводим name: ' + name):
            name_field = browser.element('input[data-testid="input"][type="text"]')
            name_field.send_keys(name)
            self.continue_button_click()

    def address_input(self, address):
        with allure.step('Вводим address: ' + address):
            browser.element('[data-test-id="location-form-title"]').should(
                have.text('Add a delivery address'))
            address_field = browser.element('[data-testid="input"]')
            address_field.type(address)
            cards = browser.all('.address-details-card.autocomplete-suggestions__entry')
            cards.should(have.size_greater_than_or_equal(2))
            cards.first.with_(timeout=5).click()

    def is_email_format_invalid(self):
        browser.element('[class="helio-input__error"]').should(
            have.exact_text('Please use a valid email address format.'))


main_page = MainPage()
