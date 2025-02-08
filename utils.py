"""
Utility functions for test automation
"""
from datetime import datetime
import os
import random
import string

def ensure_screenshots_dir():
    """Ensure screenshots directory exists"""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

def take_screenshot(device, name):
    """Take a screenshot and save it with timestamp"""
    ensure_screenshots_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_name)
    device.screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def clear_app_state(device):
    """Clear app data and restart the app"""
    print("Clearing app state...")
    app_id = 'com.eatvermont'
    device.app_stop(app_id)  # Close the app
    device.app_clear(app_id)  # Clear app data
    device.app_start(app_id)  # Start the app fresh
    print("App state cleared and restarted")

def get_next_day(current_day):
    """
    Returns the next day of the week given the current day.
    Args:
        current_day (str): Current day in three-letter format (e.g., 'MON', 'TUE')
    Returns:
        str: Next day in three-letter format
    """
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_index = days.index(current_day)
    next_index = (current_index + 1) % 7  # Use modulo to wrap around to Sunday
    return days[next_index]

def generate_random_name():
    """Generate a random name starting with 'D'."""
    name_length = random.randint(5, 10)  # Random length between 5 and 10
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=name_length-1))
    return 'D' + random_chars

def generate_random_username():
    """Generate a random username."""
    username_length = random.randint(8, 15)  # Random length between 8 and 15
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return random_chars

def handle_notification_permission(device):
    """Handle notification permission dialogs if they appear."""
    # Handle first permission dialog
    if device(text="Allow").exists:
        device(text="Allow").click()
        device.sleep(1)

        # Handle second permission dialog if it appears
        if device(text="Allow").exists:
            device(text="Allow").click()
            device.sleep(1)
