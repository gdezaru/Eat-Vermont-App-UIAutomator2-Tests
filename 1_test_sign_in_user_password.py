import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from locators import LoginPageLocators, HomeScreenLocators, PermissionDialogLocators
from utils import take_screenshot, clear_app_state
from config import TEST_USER

def test_sign_in_user_password(driver):
    """Test sign in with valid user and password"""
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
    
    # Click Log in button using the correct locator
    login_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            LoginPageLocators.LOG_IN_BUTTON
        ))
    )
    login_button.click()
    
    # Verify successful login by checking Events text is visible
    wait = WebDriverWait(driver, 10)  # Longer wait for final verification
    events_text = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            HomeScreenLocators.EVENTS_TEXT
        ))
    )
    assert events_text.is_displayed(), "Login failed - Events text not found after login"
    
    # Take screenshot after successful login
    take_screenshot(driver, "1_test_sign_in_user_password")
