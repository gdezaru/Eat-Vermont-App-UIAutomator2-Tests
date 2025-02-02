import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture
def driver():
    # Appium desired capabilities
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'b0ba3ece',  # Your actual device ID
        'appPackage': 'com.eatvermont',
        'appActivity': '.MainActivity',
        'noReset': True
    }
    
    # Create driver options
    options = UiAutomator2Options().load_capabilities(capabilities)
    
    # Initialize the driver
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    
    yield driver
    
    # Quit the driver after test
    driver.quit()
