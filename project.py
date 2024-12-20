import os
from typing import Literal

from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from selenium.webdriver.chrome.options import Options

from utils.file import abs_path_from_project

BASE_DIR = os.path.dirname(__file__)


class Config(BaseSettings):
    SELENOID_LOGIN: str = ''
    SELENOID_PASSWORD: str = ''
    SELENOID_URL: str = ''

    base_url: str = 'https://glovoapp.com/'
    browser_version: Literal['100.0', '120.0', '123.0', '126.0'] = '126.0'
    context: Literal['local_emulator', 'bstack', 'web', 'api'] = 'web'

    DRIVER_REMOTE_URL: str = ''
    BSTACK_USERNAME: str = ''
    BSTACK_ACCESSKEY: str = ''
    timeout: float = 10.0

    APP: str = ''
    APP_WAIT_ACTIVITY: str = ''
    APPWAITPACKAGE: str = ''
    APPPACKAGE: str = ''

    PLATFORM_VERSION: Literal['10.0', '12.0', '13.0', '15.0'] = '13.0'
    PLATFORM_NAME: str = 'Android'
    DEVICE_NAME: Literal[
        'Google Pixel 7 Pro',
        'Google Pixel 7',
        'Google Pixel 3',
        'Android Emulator'
    ] = 'Google Pixel 7'
    AVD: str = ''
    UDID: str = ''

    @property
    def bstack_credentials(self):
        load_dotenv(abs_path_from_project('.env.bstack'))
        self.BSTACK_USERNAME = os.getenv('BSTACK_USERNAME')
        self.BSTACK_ACCESSKEY = os.getenv('BSTACK_ACCESSKEY')
        return {
            'userName': self.BSTACK_USERNAME,
            'accessKey': self.BSTACK_ACCESSKEY
        }

    def get_selenoid_link(self):
        load_dotenv(abs_path_from_project('.env.web'))
        self.SELENOID_LOGIN = os.getenv('SELENOID_LOGIN')
        self.SELENOID_PASSWORD = os.getenv('SELENOID_PASSWORD')
        self.SELENOID_URL = os.getenv('SELENOID_URL')
        return f'https://{self.SELENOID_LOGIN}:{self.SELENOID_PASSWORD}@{self.SELENOID_URL}'

    def is_bstack_run(self):
        return self.APP.startswith('bs://')

    def driver_options(self, platform_name):
        if platform_name == 'android':
            options = UiAutomator2Options().load_capabilities(
                {
                    'platformName': self.PLATFORM_NAME,
                    'platformVersion': self.PLATFORM_VERSION,
                    'deviceName': self.DEVICE_NAME,
                    'app': self.APP if self.APP.startswith(
                        './') or self.is_bstack_run() else abs_path_from_project(
                        self.APP),
                    'appWaitActivity': self.APP_WAIT_ACTIVITY,
                }
            )

            if self.context == 'local_emulator':
                options.set_capability('udid', self.UDID)
                options.set_capability('avd', self.AVD)

            if self.context == 'bstack':
                options.set_capability(
                    'bstack:options', {
                        'projectName': 'Glovo Android tests project',
                        'buildName': 'Glovo Android build',
                        'sessionName': 'Glovo Android tests',
                        **self.bstack_credentials
                    })

        elif platform_name == 'web':
            options = Options()
            selenoid_capabilities = {
                'browserName': 'chrome',
                'browserVersion': self.browser_version,
                'selenoid:options': {
                    'enableVNC': True,
                    'enableVideo': True
                }
            }
            options.capabilities.update(selenoid_capabilities)

        return options
