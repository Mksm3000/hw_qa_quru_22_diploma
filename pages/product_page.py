from selene import browser, be, have, by
import allure


class ProductPage:

    def address_input_and_check(self, address):
        with allure.step('Вводим address: ' + address):
            # принимаем политику куки, нажимаем "accept all"
            browser.element('#onetrust-accept-btn-handler').click()

            browser.element('[data-test-id="address-input-container"]').element(
                '[data-test-id="address-input-placeholder"]').click()
            browser.element('#base-modal').should(be.visible)
            address_field = browser.element('[data-testid="input"]')
            address_field.type(address)
            cards = browser.all('.address-details-card.autocomplete-suggestions__entry')
            cards.should(have.size_greater_than_or_equal(2))
            cards.first.with_(timeout=5).click()
            check = browser.element('[data-test-id="address-picker-address"] [data-test-id="address-picker-address"]')
            check.should(have.text(address))

    def cafe_name_input_and_check(self, cafe_name):
        with allure.step('Вводим имя заведения: ' + cafe_name):
            browser.element('[data-test-id="header-search-input-city"] ['
                            'id="search-input"]').send_keys(cafe_name)
            browser.element('[data-test-id="store-card-title"]').should(
                have.exact_text(cafe_name)).click()
            browser.element('[data-test-id="store-info-title"]').should(
                have.exact_text(cafe_name))

    def meal_type(self, item_type):
        with allure.step('Вводим тип блюда: ' + item_type):
            browser.element(f'[data-test-id*="{item_type.lower()}"]').click()

    def meal_name(self, item_name):
        with allure.step('Вводим название блюда: ' + item_name):
            browser.element(by.text(item_name)).click()
            browser.element('[data-test-id="modal-window"]').should(be.visible)

    def add_meal_to_cart_and_check(self, item_name):
        with allure.step('Добавляем в корзину блюдо ' + item_name + ' и проверяем добавление'):
            browser.element('[data-test-id="add-button"]').click()
            browser.element('[data-test-id="cart-products"]').should(
                have.text(item_name))

    def edit_extra_for_meal(self, item_name, extra):
        with allure.step('Исправляем доп. ' + extra + ' для блюда ' +
                         item_name):
            collection = browser.all('[data-test-id="cart-entry-item"]')
            needful = collection.element_by(have.text(item_name))
            needful.element('[data-test-id="edit-button"]').click()
            browser.element('[data-test-id="modal-window"]').with_(timeout=10).should(
                be.visible)
            browser.element(f'[track="{extra}"]').click()
            browser.element('[data-test-id="add-button"]').click()

    def increase_qty_for_meal(self, item_name):
        with allure.step('Увеличиваем количество на +1 для блюда ' + item_name):
            collection = browser.all('[data-test-id="cart-entry-item"]')
            needful = collection.element_by(have.text(item_name))
            needful.element('[data-test-id="plus-button"]').click()

    def reduce_qty_for_meal(self, item_name):
        with allure.step('Уменьшаем количество на -1 для блюда ' + item_name):
            collection = browser.all('[data-test-id="cart-entry-item"]')
            needful = collection.element_by(have.text(item_name))
            needful.element('[data-test-id="minus-button"]').click()


product_page = ProductPage()
