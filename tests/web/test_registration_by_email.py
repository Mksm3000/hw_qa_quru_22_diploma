import allure
import pytest

from pages.main_page import main_page
from tests import conftest
from user.nonexistent import non_existent_user
from user.random import random_user


@allure.severity('critical')
@allure.label('UI')
@allure.label("owner", "Zosimov")
@allure.feature('Registration')
@allure.story('Registration new user by email')
@allure.title('Test registration by email with successful')
@conftest.web
@pytest.mark.web
def test_registration_by_email_with_successful():
    main_page.open()

    main_page.login_button_click()
    main_page.email_button_click()
    main_page.email_input(random_user.email)
    main_page.password_input(random_user.password)
    main_page.name_input(random_user.first_name)

    main_page.address_input('Mainski put')


@allure.severity('critical')
@allure.label('UI')
@allure.label("owner", "Zosimov")
@allure.feature('Registration')
@allure.story('Registration new user by email')
@allure.title('Test registration by email with invalid email format')
@conftest.web
@pytest.mark.web
def test_registration_by_email_with_invalid_email():
    main_page.open()

    main_page.login_button_click()
    main_page.email_button_click()

    main_page.email_input(non_existent_user.email)
    main_page.is_email_format_invalid()
