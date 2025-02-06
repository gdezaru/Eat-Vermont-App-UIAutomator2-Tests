import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, SettingsScreen
from utils import generate_random_name, generate_random_username


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
    d.screenshot("5_1_1_settings_screen_contents.png")


def test_settings_screen_navigation(d):
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
        edit_profile = d.xpath(SettingsScreen.EDIT_PROFILE)
        assert edit_profile.exists, "Could not find Edit Profile option"
        edit_profile.click()
        sleep(2)  # Wait for Edit Profile screen to load
        
        # Take screenshot of Edit Profile screen
        d.screenshot("5_2_1_edit_profile_screen.png")
        
        # Go back to Settings
        back_button = d.xpath(SettingsScreen.BACK_BUTTON_SETTINGS)
        assert back_button.exists, "Could not find Back button"
        back_button.click()
        sleep(2)  # Wait for settings screen to reload
        
        # Click on Location Toggle
        location_toggle = d.xpath(SettingsScreen.LOCATION_TOGGLE)
        assert location_toggle.exists, "Could not find Location Toggle"
        location_toggle.click()
        sleep(1)  # Wait for toggle to change state

        # Handle location permission dialog if it appears
        location_allow = d.xpath(SettingsScreen.LOCATION_ALLOW)
        if location_allow.wait(timeout=2):  # Wait up to 2 seconds for dialog
            location_allow.click()
            sleep(1)  # Wait for permission dialog to dismiss
        
        # Take screenshot of Settings screen with toggled location
        d.screenshot("5_2_2_settings_location_toggled.png")

        # Click on Log Out
        log_out = d.xpath(SettingsScreen.LOG_OUT)
        assert log_out.exists, "Could not find Log Out button"
        log_out.click()
        sleep(2)  # Wait for logout to complete
        
        # Take screenshot of welcome screen
        d.screenshot("5_2_3_welcome_screen_after_logout.png")


def test_settings_screen_edit_profile(d):
    """Tests the edit profile section within the settings screen."""
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
        edit_profile = d.xpath(SettingsScreen.EDIT_PROFILE)
        assert edit_profile.exists, "Could not find Edit Profile option"
        edit_profile.click()
        sleep(3)

        # Clear the name field and enter a new random name
        edit_name = d.xpath(SettingsScreen.EDIT_NAME)
        assert edit_name.exists, "Could not find Name field"
        edit_name.click()
        d.clear_text()
        new_name = generate_random_name()
        d.send_keys(new_name)
        sleep(3)  # Wait for text input

        # Verify the new name was successfully inputted
        assert edit_name.get_text() == new_name, f"Name was not updated correctly. Expected: {new_name}, Got: {edit_name.get_text()}"
        
        # Verify save button is present
        save_button = d.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
        assert save_button.exists, "Save button is not present after editing name"
        
        # Take screenshot of the edited profile name
        d.screenshot("5_3_1_edited_profile_name_save_button_active.png")

        # Clear the username field and enter a new random username
        edit_username = d.xpath(SettingsScreen.EDIT_USERNAME)
        assert edit_username.exists, "Could not find Username field"
        edit_username.click()
        d.clear_text()
        new_username = generate_random_username()
        d.send_keys(new_username)
        sleep(1)  # Wait for text input

        # Verify the new username was successfully inputted
        assert edit_username.get_text() == new_username, f"Username was not updated correctly. Expected: {new_username}, Got: {edit_username.get_text()}"
        
        # Take screenshot of the edited profile username
        d.screenshot("5_3_2_edited_profile_username_save_button_active.png")

        # Click save button and verify we return to settings screen
        save_button = d.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
        save_button.click()
        sleep(2)  # Wait for navigation

        # Verify we're back at settings screen by checking for Log out text
        log_out = d.xpath(SettingsScreen.LOG_OUT)
        assert log_out.exists, "Did not return to settings screen after saving profile changes"

        # Take screenshot of settings screen after saving changes
        d.screenshot("5_3_3_settings_screen_after_save.png")
