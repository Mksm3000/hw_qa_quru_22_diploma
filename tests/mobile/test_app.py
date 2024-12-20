import allure
import pytest

from pages.app_page import app_page
from tests import conftest


@allure.severity('critical')
@allure.label('UI')
@allure.label("owner", "Zosimov")
@allure.feature('Mobile registration')
@allure.story('Mobile registration new user by email')
@allure.title('Mobile app open and choose registration by email')
@conftest.android
@pytest.mark.android
def test_app_open_and_registration_by_email():
    app_page.open_start_page_and_click_continue()
    try:
        app_page.update_window_detect_and_close()
    except Exception as ex:
        print(f'Oops, we encountered an exception: {ex}')
    finally:
        app_page.welcome_window_and_email_input()
