import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from locators import LoginPageLocators, HomeScreenLocators
from datetime import datetime
import os

def take_screenshot(driver, name):
    """Take a screenshot and save it with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_name)
    driver.get_screenshot_as_file(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def test_sign_in_user_password(driver):
    """Test sign in with valid user and password"""
    # Test data
    TEST_EMAIL = "evtestmail@jxpomup.com"
    TEST_PASSWORD = "evtest"
    
    # Use WebDriverWait with shorter timeout
    wait = WebDriverWait(driver, 5)  # Reduced to 5 seconds
    
    try:
        # Step 1: Click Sign In button
        print("Waiting for Sign In button...")
        sign_in_button = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH, 
                LoginPageLocators.SIGN_IN_BUTTON
            ))
        )
        sign_in_button.click()
        
        # Step 2: Enter email
        print("Waiting for Email field...")
        email_field = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH,
                LoginPageLocators.EMAIL_FIELD
            ))
        )
        email_field.click()
        email_field.clear()
        email_field.send_keys(TEST_EMAIL)
        
        # Step 3: Enter password
        print("Waiting for Password field...")
        password_field = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH,
                LoginPageLocators.PASSWORD_FIELD
            ))
        )
        password_field.click()
        password_field.clear()
        password_field.send_keys(TEST_PASSWORD)
        
        # Step 4: Click Log in button
        print("Waiting for Log in button...")
        login_button = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH,
                LoginPageLocators.LOG_IN_BUTTON
            ))
        )
        login_button.click()
        
        # Minimal wait for login completion
        sleep(1)
        
        # Step 5: Verify successful login by checking Events text is visible
        print("Verifying successful login...")
        events_text = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.XPATH,
                HomeScreenLocators.EVENTS_TEXT
            ))
        )
        assert events_text.is_displayed(), "Events text not visible after login"
        print("Login successful - Events text is visible")
        
        # Step 6: Take screenshot after successful login
        take_screenshot(driver, "1_sign_in_user_password")
        
    except Exception as e:
        # Take screenshot on failure
        take_screenshot(driver, "1_sign_in_user_password_failure")
        print("\nError during test execution:")
        print(str(e))
        print("\nCurrent page source:")
        print(driver.page_source)
        raise
