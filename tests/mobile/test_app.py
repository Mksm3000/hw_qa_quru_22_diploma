import allure
import pytest

from pages.app_page import app_page
from tests import conftest
from tests.marks import microservice, layer, owner, tm4j, jira_issues

pytestmark = [
    layer("mobile"),
    owner("zosimov"),
    allure.feature("Mobile registration")
]

OWNER = "allure-framework"
REPO = "allure2"


@tm4j("ZM-T11")
@jira_issues("ZM-2")
@microservice("auth-service")
@allure.severity('critical')
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
