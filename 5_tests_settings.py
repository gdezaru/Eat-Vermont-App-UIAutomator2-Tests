import pytest
import os

from utils_authentication import sign_in_and_prepare, SignInPrepare
from utils_device_interaction import change_username_profile_settings, change_name_profile_settings
from utils_scrolling import scroll_to_bottom
from utils_settings import generate_random_name, generate_random_username, click_settings_button, click_edit_profile, \
    click_settings_back_button, click_location_toggle, handle_allow_button, click_log_out, click_settings_save_button
from utils_ui_verification import verify_settings_options, verify_settings_changed_name, verify_save_button_exists


@pytest.mark.smoke
def test_settings_contents(d, screenshots_dir):
    """
    Tests the contents of the settings screen.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Navigate to Settings
    4. Verify all settings options are visible
    5. Take screenshot of settings screen
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    click_settings_button(d)

    verify_settings_options(d)

    # Take screenshot of settings screen
    screenshot_path = os.path.join(screenshots_dir, "5_1_1_settings_screen_contents.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_settings_screen_navigation(d, screenshots_dir):
    """
    Tests the navigation within the settings screen.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Navigate to Settings
    4. Click on Edit Profile
    5. Take screenshot of Edit Profile screen
    6. Go back to Settings
    7. Click on Location Toggle
    8. Handle location permission dialog if it appears
    9. Take screenshot of Settings screen with toggled location
    10. Click on Log Out
    11. Take screenshot of welcome screen
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    click_settings_button(d)

    click_edit_profile(d)

    # Take screenshot of Edit Profile screen
    screenshot_path = os.path.join(screenshots_dir, "5_2_1_edit_profile_screen.png")
    d.screenshot(screenshot_path)

    click_settings_back_button(d)

    click_location_toggle(d)

    handle_allow_button(d)

    # Take screenshot of Settings screen with toggled location
    screenshot_path = os.path.join(screenshots_dir, "5_2_2_settings_location_toggled.png")
    d.screenshot(screenshot_path)

    click_log_out(d)

    # Take screenshot of welcome screen
    screenshot_path = os.path.join(screenshots_dir, "5_2_3_welcome_screen_after_logout.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_settings_screen_edit_profile(d, screenshots_dir):
    """
    Tests the edit profile section within the settings screen.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Navigate to Settings
    4. Click on Edit Profile
    5. Clear the name field and enter a new random name
    6. Verify the new name was successfully inputted
    7. Clear the username field and enter a new random username
    8. Verify the new username was successfully inputted
    9. Scroll to bottom of screen to ensure save button is visible
    10. Click save button and verify we return to settings screen
    11. Verify the updated name is visible on the settings screen
    12. Take screenshot of settings screen after saving changes
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    click_settings_button(d)

    click_edit_profile(d)

    # Generate a random name and store it
    new_name = generate_random_name()
    change_name_profile_settings(d, lambda: new_name)

    verify_save_button_exists(d)

    # Take screenshot of the edited profile name
    screenshot_path = os.path.join(screenshots_dir, "5_3_1_edited_profile_name_save_button_active.png")
    d.screenshot(screenshot_path)

    change_username_profile_settings(d, generate_random_username)

    # Take screenshot of the edited profile username
    screenshot_path = os.path.join(screenshots_dir, "5_3_2_edited_profile_username_save_button_active.png")
    d.screenshot(screenshot_path)

    scroll_to_bottom(d)

    click_settings_save_button(d)

    verify_settings_changed_name(d, new_name)

    # Take screenshot of settings screen after saving changes
    screenshot_path = os.path.join(screenshots_dir, "5_3_3_settings_screen_after_save.png")
    d.screenshot(screenshot_path)
