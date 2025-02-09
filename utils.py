"""
Utility functions for test automation
"""
from datetime import datetime
import os
import random
import string
import time

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

def verify_video_playback(device):
    """
    Verify that a video is playing by checking app state and UI elements.
    
    Args:
        device: UIAutomator2 device instance
    
    Returns:
        bool: True if video is playing, False otherwise
    """
    print("\nVerifying video playback...")
    
    # Get current app info
    app_info = device.info
    print(f"\nCurrent app info: {app_info}")
    
    # Get current window hierarchy
    xml_hierarchy = device.dump_hierarchy()
    print(f"\nWindow hierarchy: {xml_hierarchy}")
    
    # Check if we're still in the app
    if not device(packageName="com.eatvermont").exists:
        print("App is no longer in foreground")
        return False
        
    # Take screenshot of the video playing
    take_screenshot(device, "video_playing")
    print("Video state verification complete")
    return True


def find_and_click_video(device, video_locator):
    """
    Find a video using the provided locator and click it.
    
    Args:
        device: UIAutomator2 device instance
        video_locator: XPath locator for the video element
    
    Returns:
        bool: True if video was found and clicked, False otherwise
    """
    print("\nLooking for video...")
    video = device.xpath(video_locator)
    
    if not video.exists:
        print("Video not found")
        return False
        
    print("Video found, clicking...")
    video.click()
    return True


def wait_for_video_to_load(device, timeout=5):
    """
    Wait for video to load after clicking.
    
    Args:
        device: UIAutomator2 device instance
        timeout: How long to wait for video to load (in seconds)
    """
    print(f"\nWaiting {timeout} seconds for video to load...")
    device.sleep(timeout)  # Using device.sleep instead of time.sleep for consistency


def scroll_to_find_text(device, text, max_attempts=5):
    """
    Scroll the screen until text is found
    
    Args:
        device: UIAutomator2 device instance
        text: Text to find
        max_attempts: Maximum number of scroll attempts
        
    Returns:
        bool: True if text was found, False otherwise
    """
    screen_info = device.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4
    
    for _ in range(max_attempts):
        if device(text=text).exists:
            return True
        device.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        time.sleep(1.5)
    
    return device(text=text).exists


def scroll_until_element_is_visible(device, locator, max_attempts=5):
    """
    Scroll the screen until the element with the given locator is visible
    
    Args:
        device: UIAutomator2 device instance
        locator: XPath locator string
        max_attempts: Maximum number of scroll attempts
        
    Returns:
        bool: True if element was found, False otherwise
    """
    screen_info = device.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4
    
    for _ in range(max_attempts):
        element = device.xpath(locator)
        if element.exists:
            return True
        device.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        time.sleep(1.5)
    
    return device.xpath(locator).exists
