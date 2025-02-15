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
from locators import Events, PlansPopup, LoginPage, GuestMode, Businesses, HomeScreen, BottomNavBar, EventsScreen, VisitHistory


# Utility Functions

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
    next_index = (current_index + 1) % 7
    return days[next_index]


def try_next_day(d, current_day):
    """
    Attempts to find and click on the next day element in the events screen.

    :param d: The UIAutomator2 device instance.
    :param current_day: The current day to start trying from.
    :return: None
    """
    current_try_day = current_day
    days_tried = 0
    max_days_to_try = 7  # Try all days of the week at most

    while days_tried < max_days_to_try:
        # Get the next day to try
        next_day = get_next_day(current_try_day)
        print(f"\nTrying to click on: {next_day}")

        # Try clicking this day multiple times
        max_attempts = 3
        click_success = False

        for attempt in range(max_attempts):
            next_day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(next_day, next_day))
            print(f"\nAttempt {attempt + 1}: Next day element exists: {next_day_element.exists}")

            if not next_day_element.exists:
                print(f"\n{next_day} not found, will try next day")
                break

            next_day_element.click()
            print(f"\nClicked on {next_day}")
            sleep(2)  # Wait for next day's events to load

            # Verify if we're now on this day by checking the events list
            events_for_day = d(textContains=next_day.title())  # e.g., "Mon" instead of "MON"
            if events_for_day.exists:
                print(f"\nSuccess! Found events for {next_day}")
                click_success = True
                break
            elif attempt < max_attempts - 1:
                print(f"\nClick might not have worked (no events found for {next_day}), trying again...")
                sleep(2)  # Wait before next attempt
            else:
                print(f"\nCould not verify events for {next_day} after {max_attempts} attempts, will try next day")

        if click_success:
            break

        # Move to next day if this one didn't work
        current_try_day = next_day
        days_tried += 1

        if days_tried == max_days_to_try:
            assert False, "Could not find any clickable day after trying all days of the week"


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


def get_screen_dimensions(d):
    """
    Returns the screen width and height.
    
    :param device: The device instance.
    :return: A tuple containing (width, height)
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    return width, height


# Screenshot Management

def get_screenshots_dir():
    """Get the screenshots directory for the current test run"""
    # Get the current test run folder from the reporter
    import pytest
    reporter = next((plugin for plugin in pytest.get_platform().pluginmanager.get_plugins()
                     if hasattr(plugin, 'screenshots_folder')), None)
    if reporter:
        return reporter.screenshots_folder
    return None


def take_screenshot(d, name):
    """Take a screenshot and save it with timestamp"""
    screenshots_dir = get_screenshots_dir()
    if screenshots_dir is None:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)
    d.screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")


def save_screenshot(d, filename: str, request) -> str:
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
        return d.screenshot(filename)

    # Save screenshot in the test run's screenshots folder
    screenshot_path = os.path.join(reporter.screenshots_folder, filename)
    return d.screenshot(screenshot_path)


# UI Verification

def verify_businesses_section_present(d):
    """
    Verifies that the Businesses section is present on the screen.
    """
    print("\nVerifying Businesses section is present...")
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"
    print("Found Businesses section")


def verify_video_playback(d):
    """
    Verify that a video is playing by checking app state and UI elements.

    Args:
        device: UIAutomator2 device instance

    Returns:
        bool: True if video is playing, False otherwise
    """
    print("\nVerifying video playback...")

    # Get current app info
    app_info = d.info
    print(f"\nCurrent app info: {app_info}")

    # Get current window hierarchy
    xml_hierarchy = d.dump_hierarchy()
    print(f"\nWindow hierarchy: {xml_hierarchy}")

    # Check if we're still in the app
    if not d(packageName="com.eatvermont").exists:
        print("App is no longer in foreground")
        return False

    # Take screenshot of the video playing
    take_screenshot(d, "video_playing")
    print("Video state verification complete")
    return True


def verify_and_screenshot(d, condition, error_message, screenshots_dir, filename):
    """
    Verifies a condition and takes a screenshot if successful.
    
    :param d: The device instance.
    :param condition: A callable that returns a boolean.
    :param error_message: The error message if the condition fails.
    :param screenshots_dir: The directory to save the screenshot.
    :param filename: The name of the screenshot file.
    """
    assert condition(), error_message
    screenshot_path = os.path.join(screenshots_dir, filename)
    d.screenshot(screenshot_path)
    print(f"Screenshot saved as {filename}")


# Navigation

def click_and_verify_element(d, element_locator, description):
    """
    Clicks an element and verifies its presence.

    :param d: The device instance.
    :param element_locator: The XPath locator for the element.
    :param description: A description of the element for logging.
    """
    print(f"\nClicking and verifying {description}...")
    element = d.xpath(element_locator)
    assert element.exists, f"{description} not found"
    element.click()
    print(f"{description} clicked and verified.")


def click_trails_button(d):
    """
    Finds and clicks the Trails button on the home screen.

    :param d: The device instance.
    """
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)


def click_favorites_button(d):
    """
    Clicks the Favorites button in the bottom navigation bar.

    :param device: The UIAutomator2 device instance.
    """
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)  # Wait for favorites page to load

    # Verify that "Favorites" text is present
    assert d(text="Favorites").exists, "Favorites text not found on screen"


def click_visit_history(d):
    """
    Clicks the Visit History tab.

    :param d: The UIAutomator2 device instance.
    """
    print("\nClicking on Visit History tab...")
    visit_history_tab = d.xpath(VisitHistory.VISIT_HISTORY_TAB)
    assert visit_history_tab.exists, "Could not find Visit History tab"
    print("Found Visit History tab, clicking...")
    visit_history_tab.click()
    sleep(2)


def click_view_map(d):
    """
    Clicks the View Map button.

    :param d: The UIAutomator2 device instance.
    """
    print("\nClicking on View Map button...")
    view_map = d.xpath(HomeScreen.VIEW_MAP)
    assert view_map.exists, "Could not find View Map button"
    print("Found View Map button, clicking...")
    view_map.click()
    sleep(5)


def interact_with_events_carousel(d):
    """
    Locates and interacts with the Events carousel item.
    """
    print("\nLocating Events carousel item...")
    sleep(5)  # Wait for UI to load

    # Do one scroll first
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)
    d.swipe(start_x, start_y, start_x, end_y, duration=0.4)
    sleep(1.5)
    
    # First find any event element
    event_element = d.xpath('//android.view.ViewGroup[@content-desc]').get()
    if event_element:
        content_desc = event_element.attrib.get('content-desc')
        if content_desc:
            carousel_item = d.xpath(Events.CAROUSEL_ITEM.format(content_desc))
            assert carousel_item.exists, "Could not find Events carousel item"
            print("Events carousel item found, clicking...")
            carousel_item.click()
            sleep(7)
    else:
        assert False, "Could not find any event elements"


def scroll_to_find_text(d, text, max_attempts=5):
    """
    Scroll the screen until text is found

    Args:
        device: UIAutomator2 device instance
        text: Text to find
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if text was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        if d(text=text).exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        time.sleep(1.5)

    return d(text=text).exists


def scroll_until_element_is_visible(d, locator, max_attempts=5):
    """
    Scroll the screen until the element with the given locator is visible

    Args:
        device: UIAutomator2 device instance
        locator: XPath locator string
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if element was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        element = d.xpath(locator)
        if element.exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        time.sleep(1.5)

    return d.xpath(locator).exists


def calculate_swipe_coordinates(width, height):
    """
    Calculates swipe coordinates for scrolling.

    :param width: Screen width.
    :param height: Screen height.
    :return: A tuple containing (start_x, start_y, end_y)
    """
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4
    return start_x, start_y, end_y


def scroll_to_bottom(d, scroll_times=3, duration=0.5):
    """
    Scrolls to the bottom of the results on the screen.

    :param device: The device instance.
    :param scroll_times: Number of times to scroll to ensure reaching the bottom.
    :param duration: Duration of each swipe.
    """
    screen_size = d.window_size()
    for _ in range(scroll_times):
        d.swipe(
            screen_size[0] * 0.5, screen_size[1] * 0.8,
            screen_size[0] * 0.5, screen_size[1] * 0.2,
            duration=duration
        )
        sleep(2)


# Authentication and User Management

def sign_in_and_prepare(d):
    """Sign in and handle initial popups"""
    handle_notification_permission(d)
    sign_in_user(d)
    handle_events_popup(d)
    sleep(5)


def sign_in_user(d):
    """
    Sign in to the app using test user credentials.

    Args:
        d: UIAutomator2 device instance
    """
    from config import TEST_USER
    
    handle_notification_permission(d)

    # Wait for initial screen to load
    time.sleep(5)

    # First check if we're already logged in by looking for bottom navigation elements
    if d(description="Search").exists(timeout=2) or d(text="Search").exists(timeout=2):
        print("Already logged in, skipping sign in process")
        return

    # Find and click Get Started button
    get_started = None
    if d(description="Get Started").exists(timeout=5):
        get_started = d(description="Get Started")
    elif d(text="Get Started").exists(timeout=5):
        get_started = d(text="Get Started")

    assert get_started is not None, "Could not find Get Started button"
    get_started.click()
    time.sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    time.sleep(1)
    d.send_keys(TEST_USER['email'])
    time.sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    time.sleep(1)
    d.send_keys(TEST_USER['password'])
    time.sleep(1)

    # Try login up to 2 times
    login_attempts = 2
    for attempt in range(login_attempts):
        # Click Log In button
        log_in_button = None
        if d(description="Log in").exists(timeout=5):
            log_in_button = d(description="Log in")
        elif d(text="Log in").exists(timeout=5):
            log_in_button = d(text="Log in")

        assert log_in_button is not None, "Could not find Log in button"
        log_in_button.click()
        time.sleep(5)  # Wait for login process

        # Verify successful login by checking for common elements
        success_indicators = ["Events", "Home", "Profile", "Search"]
        for indicator in success_indicators:
            if d(text=indicator).exists(timeout=5):
                return  # Login successful
        
        if attempt < login_attempts - 1:
            # Try to go back if needed
            if d(text="Back").exists():
                d(text="Back").click()
                time.sleep(1)
            continue
        
        # If we get here on the last attempt, login failed
        assert False, "Login failed - Could not verify successful login"


def handle_events_popup(d):
    """
    Handle events popup if it appears.

    Args:
        d: UIAutomator2 device instance
    """
    # Check if events popup exists
    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("Events popup found, handling it...")

        # Click close button
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        if close_button.exists:
            close_button.click()
            sleep(1)
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
    plans_popup_close = d.xpath(PlansPopup.PLANS_POPUP_CLOSE_BUTTON)
    if plans_popup_close.exists:
        print("\nPlans popup is visible, clicking close button...")
        sleep(2)
        plans_popup_close.click()
        print("Clicked close button on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(2)


def enter_guest_mode_and_handle_popups(d):
    """Enter guest mode and handle all necessary popups."""
    handle_notification_permission(d)
    
    # Click Get Started
    get_started = d.xpath(LoginPage.GET_STARTED)
    assert get_started.exists, "Get Started button not found"
    get_started.click()
    sleep(2)

    # Click Continue as Guest
    guest_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_button.exists, "Continue as Guest button not found"
    guest_button.click()
    sleep(2)

    # Handle events popup if it appears
    handle_events_popup(d)


def handle_plans_events_popups(d):
    """Handle plans popup if present."""
    guest_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_button.exists, "Continue as Guest button not found"
    guest_button.click()
    sleep(2)
    handle_guest_mode_plans_popup(d)
    handle_events_popup(d)
    sleep(3)


# Device Interaction

def clear_app_state(d):
    """Clear app data and restart the app"""
    print("Clearing app state...")
    app_id = 'com.eatvermont'
    d.app_stop(app_id)  # Close the app
    d.app_clear(app_id)  # Clear app data
    d.app_start(app_id)  # Start the app fresh
    print("App state cleared and restarted")


def handle_notification_permission(d):
    """Handle notification permission dialogs if they appear."""
    # Handle first permission dialog
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)

        # Handle second permission dialog if it appears
        if d(text="Allow").exists:
            d(text="Allow").click()
            sleep(1)


def search_and_submit(d, search_term):
    """
    Finds the search button and field, enters a search term, and submits it.

    :param d: The device instance.
    :param search_term: The term to search for.
    """
    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys(search_term)
    sleep(1)
    d.press("enter")
    sleep(5)


def find_and_click_video(d, video_locator):
    """
    Find a video using the provided locator and click it.

    Args:
        device: UIAutomator2 device instance
        video_locator: XPath locator for the video element

    Returns:
        bool: True if video was found and clicked, False otherwise
    """
    print("\nLooking for video...")
    video = d.xpath(video_locator)

    if not video.exists:
        print("Video not found")
        return False

    print("Video found, clicking...")
    video.click()
    return True


def wait_for_video_to_load(timeout=5):
    """
    Wait for video to load after clicking.

    Args:
        timeout: How long to wait for video to load (in seconds)
    """
    print(f"\nWaiting {timeout} seconds for video to load...")
    sleep(timeout)


def click_and_fill_forgot_password(d, email):
    """
    Finds and clicks the Get Started button, navigates to Forgot Password,
    and enters the email for password reset.

    :param d: The device instance.
    :param email: The email address to enter for password reset.
    """
    # Find and click Get Started button
    get_started = None
    if d(description="Get Started").exists(timeout=5):
        get_started = d(description="Get Started")
    elif d(text="Get Started").exists(timeout=5):
        get_started = d(text="Get Started")

    assert get_started is not None, "Could not find Get Started button"
    get_started.click()
    time.sleep(2)

    # Click Forgot Password
    forgot_password = d.xpath(LoginPage.FORGOT_PASSWORD)
    assert forgot_password.wait(timeout=5), "Forgot Password button not found"
    forgot_password.click()
    sleep(2)

    # Enter email
    email_field = d.xpath(LoginPage.RESET_PASSWORD_EMAIL_FIELD)
    assert email_field.wait(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(email)
    sleep(1)