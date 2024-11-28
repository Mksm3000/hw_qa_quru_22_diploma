import os

import pytest
from appium import webdriver
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach

DEFAULT_BROWSER_VERSION = '100.0'


def pytest_addoption(parser):
    parser.addoption(
        '--browser-version',
        default='100.0',
        help='Версия браузера в которой будут запущены тесты'
    )


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser-version')
    browser_version = browser_version if browser_version != '' else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    remote_browser_url = os.getenv('REMOTE_BROWSER_URL')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{remote_browser_url}",
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = 'https://glovoapp.com/'
    browser.config.window_height = 1600
    browser.config.window_width = 900
    browser.config.timeout = 15

    yield browser

    attach.png_attachment(browser)
    attach.log_attachment(browser)
    attach.html_attachment(browser)
    attach.web_video_attachment(browser)

    browser.quit()
