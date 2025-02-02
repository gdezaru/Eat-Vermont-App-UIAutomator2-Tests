import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def test_sign_in_user_password(driver):
    """Test sign in with valid user and password"""
    # Verify app is running
    current_activity = driver.current_activity
    current_package = driver.current_package
    print(f"\nCurrent Activity: {current_activity}")
    print(f"Current Package: {current_package}")
    
    # Print available contexts (NATIVE_APP or WEBVIEW)
    contexts = driver.contexts
    print(f"\nAvailable contexts: {contexts}")
    current_context = driver.current_context
    print(f"Current context: {current_context}")
    
    # Wait longer for React Native app to fully load
    sleep(10)
    
    print("\nTrying to find Sign In button...")
    
    # Use WebDriverWait to wait for element
    wait = WebDriverWait(driver, 10)
    
    # Find the TextView element
    sign_in_xpath = '//android.widget.TextView[@text="Sign In"]'
    print(f"\nLooking for element with xpath: {sign_in_xpath}")
    
    try:
        sign_in_button = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, sign_in_xpath))
        )
        print("Element found!")
        
        # Get element location for verification
        location = sign_in_button.location
        size = sign_in_button.size
        print(f"Element location: {location}")
        print(f"Element size: {size}")
        
        # Click the button
        sign_in_button.click()
        print("Button clicked!")
        
        # Short wait to verify the click effect
        sleep(2)
        
    except Exception as e:
        print(f"\nError finding element: {str(e)}")
        print("\nCurrent page source:")
        print(driver.page_source)
        raise
