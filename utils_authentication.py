"""
Utility functions for authentication
"""
from time import sleep

from locators import Events, PlansPopup, LoginPage, GuestMode
from utils_device_interaction import handle_notification_permission


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
    sleep(5)

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
    sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    sleep(1)
    d.send_keys(TEST_USER['email'])
    sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    sleep(1)
    d.send_keys(TEST_USER['password'])
    sleep(1)

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
        sleep(5)  # Wait for login process

        # Verify successful login by checking for common elements
        success_indicators = ["Events", "Home", "Profile", "Search"]
        for indicator in success_indicators:
            if d(text=indicator).exists(timeout=5):
                return  # Login successful

        if attempt < login_attempts - 1:
            # Try to go back if needed
            if d(text="Back").exists():
                d(text="Back").click()
                sleep(1)
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