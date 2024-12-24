import allure
import allure_commons
import pytest
from appium import webdriver as appium_webdriver
from selene import browser, support
from selenium import webdriver as selenium_webdriver

import project
from utils import attach
from utils.file import abs_path_from_project


def pytest_addoption(parser):
    parser.addoption("--context",
                     default=project.Config().context,
                     help="Context for the tests")
    parser.addoption("--browser_version",
                     default=project.Config().browser_version,
                     help="Context for the tests")


@pytest.fixture(scope='session', autouse=True)
def project_config(request):
    context_value = request.config.getoption("--context")
    project_config = project.Config(_env_file=abs_path_from_project(f'.env.'
                                                                    f'{context_value}'))
    if context_value == 'web':
        browser_version_value = request.config.getoption("--browser_version")
        project_config = project.Config(
            _env_file=abs_path_from_project(f'.env.{context_value}'),
            browser_version=browser_version_value if
            context_value == 'web' else None)

    return project_config


@pytest.fixture(scope='function', autouse=True)
def driver_management(request, project_config):
    if request.param == 'android':
        with allure.step('init app session'):
            browser.config.driver = appium_webdriver.Remote(
                project_config.DRIVER_REMOTE_URL,
                options=project_config.driver_options(request.param))

        browser.config.timeout = project_config.timeout
        browser.config._wait_decorator = support._logging.wait_with(
            context=allure_commons._allure.StepContext
        )

    elif request.param == 'web':
        browser.config.base_url = project_config.base_url
        browser.config.window_width = 1920
        browser.config.window_height = 1080

        driver = selenium_webdriver.Remote(
            command_executor=project_config.get_selenoid_link(),
            options=project_config.driver_options(request.param)
        )
        browser.config.driver = driver

    elif request.param == 'api':
        with allure.step('Start api test'):
            pass

    yield

    if request.param == 'web':
        attach.html_attachment(browser)
        attach.log_attachment(browser)
        attach.web_video_attachment(browser)
        attach.png_attachment(browser)

    if project_config.context in ['bstack', 'local_emulator']:
        attach.xml_attachment(browser)

    if project_config.context != 'api':
        session_id = browser.driver.session_id
    else:
        session_id = ''

    if project_config.context != 'api':
        with allure.step('tear down app session with id: ' + session_id):
            browser.quit()

    if project_config.context == 'bstack':
        attach.video_attachment(session_id)


android = pytest.mark.parametrize('driver_management', ['android'], indirect=True)
api = pytest.mark.parametrize('driver_management', ['api'], indirect=True)
web = pytest.mark.parametrize('driver_management', ['web'], indirect=True)
