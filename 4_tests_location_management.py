"""
import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, EventsScreen, HomeScreenTiles, BottomNavBar, LocationManagement
from utils import get_next_day, handle_notification_permission, sign_in_user


@pytest.mark.smoke
def test_home_screen_location_picker(d):
    "
    Test that the location picker button on the Home Screen works
    Steps:
    1. Handle notification permission if it appears
    2. Find and click Sign In button
    3. Enter email
    4. Enter password
    5. Click Log in and verify
    6. Click location picker button
    7. Take screenshot
    8. Click search input and enter location
    9. Type "Burlington" and press enter
    10. Take screenshot of search results
    11. Click on Burlington search result
    12. Take screenshot after location selection
    13. Assert that Burlington is present on screen
    14. Take final screenshot
    "
    # Handle notification permission if it appears
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)

    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")

    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    d.send_keys(TEST_USER['password'])
    sleep(1)

    # Click Log in and verify
    login_attempts = 2
    for attempt in range(login_attempts):
        # Find and click login button
        login_button = d(text="Log in")
        assert login_button.exists(timeout=5), "Log in button not found"
        login_button.click()
        sleep(5)  # Wait for login process

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
                    sleep(1)
                continue
            assert False, "Login failed - Could not verify successful login"

    # Click location picker button
    location_picker = d.xpath(HomeScreen.LOCATION_PICKER_HOME_SCREEN)
    assert location_picker.exists, "Could not find location picker button"
    location_picker.click()
    sleep(2)  # Wait for location picker to appear

    # Take screenshot
    d.screenshot("4_1_1_location_picker_home_screen.png")

    # Click search input and enter location
    search_input = d.xpath(LocationManagement.LOCATION_SEARCH_INPUT)
    assert search_input.exists, "Could not find location search input"
    search_input.click()
    sleep(1)  # Wait for keyboard to appear
    
    # Type "Burlington" and press enter
    d.send_keys("Burlington")
    sleep(2)  # Wait for text to be entered
    d.press("enter")
    sleep(5)  # Wait for search results

    # Take screenshot of search results
    d.screenshot("4_1_2_location_search_results.png")

    # Click on Burlington search result
    burlington_result = d.xpath(LocationManagement.LOCATION_SEARCH_RESULT.format("Burlington"))
    assert burlington_result.exists, "Could not find Burlington in search results"
    burlington_result.click()
    sleep(5)  # Wait for location to be selected

    # Take screenshot after location selection
    d.screenshot("4_1_3_location_selected.png")

    # Assert that Burlington is present on screen
    assert d(text="Burlington").exists, "Burlington text not found on screen after selection"

    # Take final screenshot
    d.screenshot("4_1_4_location_confirmed.png")


@pytest.mark.smoke
def test_home_screen_use_current_location(d):
    Test that the 'Use Current Location' button on the Home Screen works
    Steps:
    1. Handle notification permission if it appears
    2. Find and click Sign In button
    3. Enter email
    4. Enter password
    5. Click Log in and verify
    6. Click location picker button
    7. Take screenshot
    # Handle notification permission if it appears
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)

    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")

    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    d.send_keys(TEST_USER['password'])
    sleep(1)

    # Click Log in and verify
    login_attempts = 2
    for attempt in range(login_attempts):
        # Find and click login button
        login_button = d(text="Log in")
        assert login_button.exists(timeout=5), "Log in button not found"
        login_button.click()
        sleep(5)  # Wait for login process

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
                    sleep(1)
                continue
            assert False, "Login failed - Could not verify successful login"

        # Click location picker button
        location_picker = d.xpath(HomeScreen.LOCATION_PICKER_HOME_SCREEN)
        assert location_picker.exists, "Could not find location picker button"
        location_picker.click()
        sleep(2)  # Wait for location picker to appear

        # Take screenshot
        d.screenshot("4_2_1_location_picker_home_screen.png")
"""