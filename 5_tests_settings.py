import pytest

from utils_authentication import SignInPrepare
from utils_settings import Settings, EditSaveProfile
from utils_device_interaction import EditProfile
from utils_ui_verification import VerifySettings
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import GeneralScrolling


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
    settings = Settings(d)
    verify_settings = VerifySettings(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    settings.click_settings_button()

    verify_settings.verify_settings_options()

    screenshots.take_screenshot("5_1_1_settings_screen_contents")


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
    settings = Settings(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    settings.click_settings_button()

    settings.click_edit_profile()

    screenshots.take_screenshot("5_2_1_edit_profile_screen")

    settings.click_settings_back_button()

    settings.click_location_toggle()
    settings.handle_allow_button()

    screenshots.take_screenshot("5_2_2_settings_location_toggled")

    settings.click_log_out()

    screenshots.take_screenshot("5_2_3_welcome_screen")


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
    settings = Settings(d)
    edit_profile = EditProfile(d)
    edit_save = EditSaveProfile(d)
    verify_settings = VerifySettings(d)
    screenshots = ScreenshotsManagement(d)
    scrolling = GeneralScrolling(d)

    sign_in.sign_in_and_prepare()
    settings.click_settings_button()
    settings.click_edit_profile()

    new_name = edit_profile.change_name_profile_settings(lambda: EditSaveProfile.generate_random_name())

    verify_settings.verify_save_button_exists()

    screenshots.take_screenshot("5_3_1_edited_profile_name_save_button_active")

    edit_profile.change_username_profile_settings(lambda: EditSaveProfile.generate_random_username())

    screenshots.take_screenshot("5_3_2_edited_profile_username_save_button_active")

    scrolling.scroll_to_bottom()

    edit_save.click_settings_save_button()

    verify_settings.verify_settings_changed_name(new_name)

    screenshots.take_screenshot("5_3_3_settings_screen_after_save")
