"""
Utility functions for test automation
"""
from datetime import datetime
import os
from time import sleep
import time
from config import TEST_USER
import random
import string
from locators import Events, PlansPopup, LoginPage, GuestMode


def get_screenshots_dir():
    """Get the screenshots directory for the current test run"""
    # Get the current test run folder from the reporter
    import pytest
    reporter = next((plugin for plugin in pytest.get_platform().pluginmanager.get_plugins() if hasattr(plugin, 'screenshots_folder')), None)
    if reporter:
        return reporter.screenshots_folder
    return None  # Return None if no reporter found


def take_screenshot(device, name):
    """Take a screenshot and save it with timestamp"""
    screenshots_dir = get_screenshots_dir()
    if screenshots_dir is None:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)
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
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=name_length - 1))
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


def sign_in_and_prepare(d):
    """Sign in and handle initial popups"""
    handle_notification_permission(d)
    sign_in_user(d)
    handle_events_popup(d)
    sleep(10)


def sign_in_user(d):
    """
    Sign in to the app using test user credentials.
    
    Args:
        d: UIAutomator2 device instance
    """
    handle_notification_permission(d)

    # Wait for initial screen to load
    print("\nWaiting for initial screen to load...")
    time.sleep(5)  # Add initial wait for app to fully load
    
    # Debug: Dump current screen hierarchy
    print("\nCurrent screen hierarchy:")
    print(d.dump_hierarchy())
    
    # First check if we're already logged in by looking for bottom navigation elements
    if d(description="Search").exists(timeout=2) or d(text="Search").exists(timeout=2):
        print("Already logged in, skipping sign in process")
        return
    
    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")

    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    time.sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    time.sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    d.send_keys(TEST_USER['password'])
    time.sleep(1)

    # Click Log in and verify
    login_attempts = 2
    for attempt in range(login_attempts):
        # Find and click login button
        login_button = d(text="Log in")
        assert login_button.exists(timeout=5), "Log in button not found"
        login_button.click()
        time.sleep(5)  # Wait for login process

        # Check for error messages
        error_messages = [
            "Invalid email or password",
            "Login failed",
            "Error",
            "Something went wrong",
            "No internet connection"
        ]

        error_found = False
        for error_msg in error_messages:
            if d(textContains=error_msg).exists(timeout=2):
                error_found = True
                break

        if error_found and attempt < login_attempts - 1:
            continue

        # Verify successful login by checking for common elements
        success_indicators = ["Events", "Home", "Profile", "Search"]
        for indicator in success_indicators:
            if d(text=indicator).exists(timeout=5):
                break
        else:
            if attempt < login_attempts - 1:
                # Try to go back if needed
                if d(text="Back").exists():
                    d(text="Back").click()
                    time.sleep(1)
                continue
            assert False, "Login failed - Could not verify successful login"


def handle_events_popup(device):
    """
    Handle events popup if it appears.
    
    Args:
        device: UIAutomator2 device instance
    """
    # Check if events popup exists
    events_popup = device.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("Events popup found, handling it...")

        # Click close button
        close_button = device.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        if close_button.exists:
            close_button.click()
            time.sleep(1)
            print("Closed events popup")
        else:
            print("No close button found on events popup")
    else:
        print("No events popup found")


def handle_guest_mode_plans_popup(d):
    """
    Handles the plans popup in guest mode.

    Args:
        d: UIAutomator2 device instance
    """
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        time.sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        time.sleep(5)


def enter_guest_mode_and_handle_popups(d):
    """Enter guest mode and handle all necessary popups."""
    handle_notification_permission(d)
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)
    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)
    handle_plans_events_popups(d)


def handle_plans_events_popups(d):
    """Handle plans popup if present."""
    handle_guest_mode_plans_popup(d)
    handle_events_popup(d)
    sleep(10)


def save_screenshot(device, filename: str, request) -> str:
    """
    Save a screenshot to the current test run's screenshots folder.
    
    Args:
        device: The UI Automator device instance
        filename: The desired filename for the screenshot
        request: The pytest request fixture
    
    Returns:
        str: The path where the screenshot was saved
    """
    # Get the current test run folder from the reporter
    reporter = request.config.pluginmanager.get_plugin('excel_reporter')
    if not reporter:
        # Fallback to saving in the current directory if reporter not found
        return device.screenshot(filename)
        
    # Save screenshot in the test run's screenshots folder
    screenshot_path = os.path.join(reporter.screenshots_folder, filename)
    return device.screenshot(screenshot_path)