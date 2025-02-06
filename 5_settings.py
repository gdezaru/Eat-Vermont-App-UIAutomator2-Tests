import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, SettingsScreen


def test_settings_contents(d):
    """Tests the contents of the settings screen."""
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

    # Click on Settings button
    settings_button = d.xpath(HomeScreen.SETTINGS_BUTTON)
    assert settings_button.exists, "Could not find Settings button"
    settings_button.click()
    sleep(2)

    # Verify all settings options are visible
    manage_account = d.xpath(SettingsScreen.MANAGE_ACCOUNT)
    assert manage_account.exists, "Manage Account option not found"

    edit_profile = d.xpath(SettingsScreen.EDIT_PROFILE)
    assert edit_profile.exists, "Edit Profile option not found"

    share_location = d.xpath(SettingsScreen.SHARE_MY_LOCATION)
    assert share_location.exists, "Share My Location option not found"

    log_out = d.xpath(SettingsScreen.LOG_OUT)
    assert log_out.exists, "Log out option not found"

    # Take screenshot of settings screen
    d.screenshot("5_1_settings_screen_contents.png")


def settings_screen_navigation(d):
    """Tests the navigation within the settings screen."""
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

        # Click on Settings button
        settings_button = d.xpath(HomeScreen.SETTINGS_BUTTON)
        assert settings_button.exists, "Could not find Settings button"
        settings_button.click()
        sleep(2)

        # Click on Edit Profile
