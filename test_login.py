import pytest
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep

def test_sign_in_button(driver):
    """Test to verify the Sign In button is present and clickable"""
    # Wait for app to load
    sleep(2)
    
    # Find and click Sign In button using exact XPath
    sign_in_button = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Sign In"]')
    sign_in_button.click()
    
    # Add verification steps here
    # For example, verify we're on the sign-in screen
    sleep(2)  # Wait for transition
    # Add your assertions here
