import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from locators import LoginPageLocators, HomeScreenLocators, PermissionDialogLocators
from utils import take_screenshot, clear_app_state

def test_sign_in_user_password(driver):
    """Test sign in with valid user and password"""
    # Clear app state before starting the test
    clear_app_state(driver)
    
    # Handle notification permission dialog if it appears
    print("Checking for notification permission dialog...")
    allow_buttons = driver.find_elements(AppiumBy.XPATH, PermissionDialogLocators.ALLOW_BUTTON)
    if allow_buttons:
        allow_buttons[0].click()
        print("Clicked Allow on notification permission dialog")
        sleep(2)  # Wait for dialog to dismiss
    else:
        print("No notification permission dialog found, continuing...")
    
    # Test data
    TEST_EMAIL = "evtestmail@jxpomup.com"
    TEST_PASSWORD = "evtest"
    
    # Use WebDriverWait with shorter timeout
    wait = WebDriverWait(driver, 5)
    
    # Step 1: Click Sign In button
    print("Waiting for Sign In button...")
    sign_in_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH, 
            LoginPageLocators.SIGN_IN_BUTTON
        ))
    )
    sign_in_button.click()
    print("Clicked Sign In button")
    
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
    print(f"Entered email: {TEST_EMAIL}")
    
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
    print("Entered password")
    
    # Hide keyboard
    print("Hiding keyboard...")
    try:
        driver.hide_keyboard()
        print("Keyboard hidden successfully")
    except:
        print("Keyboard was not present or could not be hidden")
    
    sleep(1)  # Short wait after hiding keyboard
    
    # Step 4: Try different strategies to find and click Log in button
    print("\n=== TRYING TO FIND LOG IN BUTTON ===")
    
    # First try: by text
    try:
        login_buttons = driver.find_elements(AppiumBy.XPATH, '//android.widget.TextView[@text="Log in"]')
        if login_buttons:
            print(">>> SUCCESS: Found Log in button by exact text match <<<")
            login_buttons[0].click()
        else:
            # Second try: by class and partial text
            login_buttons = driver.find_elements(AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Log")]')
            if login_buttons:
                print(">>> SUCCESS: Found Log in button by partial text match <<<")
                login_buttons[0].click()
            else:
                # Third try: by resource ID
                login_buttons = driver.find_elements(AppiumBy.ID, "com.eatvermont:id/login_button")
                if login_buttons:
                    print(">>> SUCCESS: Found Log in button by resource ID <<<")
                    login_buttons[0].click()
                else:
                    print(">>> FAILED: Could not find Log in button with any strategy <<<")
    except Exception as e:
        print(f">>> ERROR clicking Log in button: {str(e)} <<<")
    print("=====================================\n")
        
    # Step 5: Verify successful login by checking Events text is visible
    print("Verifying successful login...")
    wait = WebDriverWait(driver, 10)  # Longer wait for final verification
    events_text = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            HomeScreenLocators.EVENTS_TEXT
        ))
    )
    assert events_text.is_displayed(), "Login failed - Events text not found after login"
    print("Login successful - Events text found")

    # Take screenshot after successful login
    take_screenshot(driver, "1_test_sign_in_user_password")
