"""
Utility functions for device interaction
"""
from time import sleep
import time
from locators import LoginPage, SettingsScreen


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
        d: UIAutomator2 device instance
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


def change_username_profile_settings(d, generate_random_username):
    """
    Changes the username in the Edit Profile screen.
    """
    edit_username = d.xpath(SettingsScreen.EDIT_USERNAME)
    assert edit_username.exists, "Could not find Username field"
    edit_username.click()
    d.clear_text()
    new_username = generate_random_username()
    d.send_keys(new_username)
    sleep(1)
    assert edit_username.get_text() == new_username, (f"Username was not updated correctly. Expected: {new_username},"
                                                      f" Got: {edit_username.get_text()}")


def change_name_profile_settings(d, generate_random_name):
    """
    Changes the name in the Edit Profile screen.
    """
    edit_name = d.xpath(SettingsScreen.EDIT_NAME)
    assert edit_name.exists, "Could not find Name field"
    edit_name.click()
    d.clear_text()
    new_name = generate_random_name()
    d.send_keys(new_name)
    sleep(3)

    # Verify the new name was successfully inputted
    assert edit_name.get_text() == new_name, f"Name was not updated correctly. Expected: {new_name}, Got: {edit_name.get_text()}"