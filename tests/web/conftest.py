import os

import pytest
from appium import webdriver
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach
from dotenv import load_dotenv


AVAILABLE_BROWSER_VERSIONS = ('100.0', '113.0', '114.0', '120.0',
                              '121.0', '122.0', '123.0', '124.0',
                              '125.0', '126.0')


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="web",
        help="Specify the test context"
    )
    parser.addoption(
        '--browser-version',
        default=AVAILABLE_BROWSER_VERSIONS[-1],
        help='Версия Chrome browser, в котором будут запущены тесты'
    )


def pytest_configure(config):
    context = config.getoption("--context")
    env_file_path = f".env.{context}"

    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        print(f"Warning: Configuration file '{env_file_path}' not found.")


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser-version')
    browser_version = browser_version if (browser_version in
                                          AVAILABLE_BROWSER_VERSIONS) else (
        AVAILABLE_BROWSER_VERSIONS[-1])

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

    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASS')
    remote_browser_url = os.getenv('SELENOID_URL')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{remote_browser_url}",
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = 'https://glovoapp.com/'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 30

    yield browser

    attach.png_attachment(browser)
    attach.log_attachment(browser)
    attach.html_attachment(browser)
    attach.web_video_attachment(browser)

    browser.quit()
