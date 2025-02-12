import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, SettingsScreen, Events
from utils import generate_random_name, generate_random_username, handle_notification_permission, sign_in_user, \
    handle_events_popup
from retry_decorator import retry


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_settings_contents(d):
    """
    Tests the contents of the settings screen.
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Settings
    5. Verify all settings options are visible
    6. Take screenshot of settings screen
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_settings_screen_navigation(d):
    """
    Tests the navigation within the settings screen.
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Settings
    5. Click on Edit Profile
    6. Take screenshot of Edit Profile screen
    7. Go back to Settings
    8. Click on Location Toggle
    9. Handle location permission dialog if it appears
    10. Take screenshot of Settings screen with toggled location
    11. Click on Log Out
    12. Take screenshot of welcome screen
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_settings_screen_edit_profile(d):
    """
    Tests the edit profile section within the settings screen.
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Settings
    5. Click on Edit Profile
    6. Clear the name field and enter a new random name
    7. Verify the new name was successfully inputted
    8. Clear the username field and enter a new random username
    9. Verify the new username was successfully inputted
    10. Scroll to bottom of screen to ensure save button is visible
    11. Click save button and verify we return to settings screen
    12. Verify the updated name is visible on the settings screen
    13. Take screenshot of settings screen after saving changes
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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

    # Scroll to bottom of screen to ensure save button is visible
    d.swipe_ext("up", scale=0.8)
    sleep(1)  # Wait for scroll to complete

    # Click save button and verify we return to settings screen
    save_button = d.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
    save_button.click()
    sleep(4)  # Wait for navigation

    # Verify the updated name is visible on the settings screen
    name_text = d(text=new_name)
    assert name_text.exists(timeout=5), f"Updated name '{new_name}' is not visible after saving changes"

    # Take screenshot of settings screen after saving changes
    d.screenshot("5_3_3_settings_screen_after_save.png")
