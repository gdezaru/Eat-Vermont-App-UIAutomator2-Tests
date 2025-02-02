import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep

@pytest.fixture
def driver():
    # Appium desired capabilities
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'b0ba3ece',  # Your actual device ID
        'appPackage': 'com.eatvermont',
        'appActivity': '.MainActivity',
        'noReset': True,
        'autoLaunch': True,
        'newCommandTimeout': 60,
        'waitForIdleTimeout': 0,  # Don't wait for idle
        'systemPort': 8201  # Dedicated system port
    }
    
    # Create driver options
    options = UiAutomator2Options().load_capabilities(capabilities)
    
    # Initialize the driver
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    
    # Force stop and restart the app
    driver.terminate_app('com.eatvermont')
    sleep(1)  # Reduced from 2 seconds
    
    # Launch the app
    driver.activate_app('com.eatvermont')
    sleep(3)  # Reduced from 5 seconds
    
    yield driver
    
    # Quit the driver after test
    driver.quit()
