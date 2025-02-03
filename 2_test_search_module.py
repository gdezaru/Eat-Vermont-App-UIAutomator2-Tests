import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from locators import (LoginPageLocators, PermissionDialogLocators, 
                     BottomNavBarLocators, SearchModule)
from utils import take_screenshot, clear_app_state
from config import TEST_USER

def test_search_events(driver):
    """Test searching for events"""
    # Clear app state before starting the test
    clear_app_state(driver)
    
    # Handle notification permission dialog if it appears
    allow_buttons = driver.find_elements(AppiumBy.XPATH, PermissionDialogLocators.ALLOW_BUTTON)
    if allow_buttons:
        allow_buttons[0].click()
        sleep(1)
    
    wait = WebDriverWait(driver, 5)
    
    # Click Sign In button
    sign_in_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH, 
            LoginPageLocators.SIGN_IN_BUTTON
        ))
    )
    sign_in_button.click()
    
    # Enter email
    email_field = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            LoginPageLocators.EMAIL_FIELD
        ))
    )
    email_field.click()
    email_field.clear()
    email_field.send_keys(TEST_USER['email'])
    
    # Enter password
    password_field = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            LoginPageLocators.PASSWORD_FIELD
        ))
    )
    password_field.click()
    password_field.clear()
    password_field.send_keys(TEST_USER['password'])
    
    # Hide keyboard if present
    try:
        driver.hide_keyboard()
    except:
        pass
    
    # Click Log in button
    login_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            LoginPageLocators.LOG_IN_BUTTON
        ))
    )
    login_button.click()
    sleep(3)  # Wait for home screen to load
    
    # Click on Search in bottom navigation bar
    search_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            BottomNavBarLocators.SEARCH_BOTTOM_NAV_BAR
        ))
    )
    search_button.click()
    sleep(2)  # Wait for search screen to load

    # Click on the search icon/field first
    search_icon = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            SearchModule.SEARCH_ICON
        ))
    )
    search_icon.click()
    sleep(1)  # Short wait for search input to be active
    
    # Now enter text in search input
    search_input = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            SearchModule.SEARCH_INPUT_BAR
        ))
    )
    search_input.click()
    search_input.send_keys("Burlington")  # You can parameterize this search term later if needed
    
    # Press Enter on keyboard to submit search
    driver.press_keycode(66)  # 66 is the keycode for Enter/Return on Android
    sleep(2)  # Wait for search results to update

    # Verify search results are displayed
    search_results = driver.find_elements(AppiumBy.XPATH, SearchModule.EVENTS_SEARCH_RESULTS.format("Burlington"))
    assert len(search_results) > 0, "Nothing found!"

    # Take a screenshot of the search results
    take_screenshot(driver, "2_1_search_events")