"""
Utility functions for test automation
"""
from datetime import datetime
import os

def take_screenshot(driver, name):
    """Take a screenshot and save it with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_name)
    driver.get_screenshot_as_file(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def clear_app_state(driver):
    """Clear app data and restart the app"""
    print("Clearing app state...")
    app_id = 'com.eatvermont'
    driver.terminate_app(app_id)  # Close the app
    driver.activate_app(app_id)   # Start the app fresh
    print("App state cleared and restarted")
