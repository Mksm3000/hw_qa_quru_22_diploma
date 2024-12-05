import os
import allure
import allure_commons
import pytest

from selene import browser, support
from appium import webdriver
from utils import attach
from dotenv import load_dotenv


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


def pytest_configure(config):
    context = config.getoption("--context")
    env_file_path = f".env.{context}"

    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        print(f"Warning: Configuration file '{env_file_path}' not found.")


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def android_mobile_management(context):

    print(f'\nMobile context: {context}\n')

    from config import config
    options = config.to_driver_options(context=context)

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(
            options.get_capability('remote_url'),
            options=options
        )

    browser.config.timeout = 30.0

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    attach.png_attachment(browser)
    attach.xml_attachment(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session with id' + session_id):
        browser.quit()

    if context == 'bstack':
        attach.video_attachment(session_id)
