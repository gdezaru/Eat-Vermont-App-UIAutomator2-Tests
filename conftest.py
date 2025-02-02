import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_connection import AppiumConnection
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.common.selenium_manager import SeleniumManager
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.remote_connection import RemoteConnection
from appium.options.common.base import AppiumOptions
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import random

@pytest.fixture
def driver():
    driver = None
    system_port = random.randint(8200, 8299)
    
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'b0ba3ece',
        'appPackage': 'com.eatvermont',
        'appActivity': '.MainActivity',
        'noReset': True,
        'autoLaunch': True,
        # Minimal timeouts
        'newCommandTimeout': 15,
        'uiautomator2ServerLaunchTimeout': 10000,
        'uiautomator2ServerInstallTimeout': 10000,
        'androidInstallTimeout': 15000,
        'adbExecTimeout': 10000,
        'waitForIdleTimeout': 0,
        # Quick startup options
        'systemPort': system_port,
        'skipServerInstallation': True,  # Skip if already installed
        'skipDeviceInitialization': True,  # Skip if device already initialized
        'enforceAppInstall': False,  # Don't reinstall if exists
        'autoGrantPermissions': True,
        'disableWindowAnimation': True,
        'ignoreHiddenApiPolicyError': True,
        'noSign': True,  # Skip signature verification
        'dontStopAppOnReset': True  # Don't stop app between tests
    }

    options = UiAutomator2Options().load_capabilities(capabilities)

    try:
        # Quick ADB restart
        os.system("adb kill-server")
        os.system("adb start-server")
        
        # Clear UiAutomator
        os.system("adb shell pm clear io.appium.uiautomator2.server")
        os.system("adb shell pm clear io.appium.uiautomator2.server.test")
        
        print(f"Starting driver with system port: {system_port}")
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        
        # Quick app restart
        driver.terminate_app('com.eatvermont')
        driver.activate_app('com.eatvermont')
        sleep(1)  # Minimal wait for app to load
        
        yield driver
        
    finally:
        if driver:
            driver.quit()
            os.system("adb shell pm clear io.appium.uiautomator2.server")
            os.system("adb shell pm clear io.appium.uiautomator2.server.test")
