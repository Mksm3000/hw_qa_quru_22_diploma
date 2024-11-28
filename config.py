import os

from appium.options.android import UiAutomator2Options
from pydantic import BaseModel
from utils.file import abs_path_from_project


class Config(BaseModel):
    context: str
    remote_url: str = os.getenv('REMOTE_URL')
    device_name: str = os.getenv('DEVICE_NAME')
    app_local: str = abs_path_from_project(os.getenv('APP'))
    app_bstack: str = os.getenv('APP')
    platformName: str = os.getenv('PLATFORM_NAME')
    platformVersion: str = os.getenv('PLATFORM_VERSION')
    userName: str = os.getenv('USER_NAME')
    accessKey: str = os.getenv('ACCESS_KEY')

    def to_driver_options(self, context):
        options = UiAutomator2Options()

        if context == 'local_emulator':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('deviceName', self.device_name)
            options.set_capability('app', self.app_local)

        if context == 'bstack':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('deviceName', self.device_name)
            options.set_capability('platformName', self.platformName)
            options.set_capability('platformVersion', self.platformVersion)
            options.set_capability('app', self.app_bstack)
            options.set_capability(
                'bstack:options', {
                    'projectName': 'Glovo Android tests project',
                    'buildName': 'Glovo Android build',
                    'sessionName': 'Glovo Android tests',
                    'userName': self.userName,
                    'accessKey': self.accessKey,
                },
            )

        print(self.device_name)

        return options


config = Config(context="local_emulator")
