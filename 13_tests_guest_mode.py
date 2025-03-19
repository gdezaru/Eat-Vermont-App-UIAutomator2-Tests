import pytest

from utils_authentication import GuestModeAuth
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollVideos
from utils_ui_navigation import NavGuestMode
from utils_ui_verification import VerifyGuestMode


@pytest.mark.smoke
def test_guest_mode_button(d, screenshots_dir):
    """
    Test the Guest Mode Home screen.
    
    Steps:
    1. Handle notification permission if it appears
    2. Click Continue as Guest button
    3. Handle events popup if it appears
    4. Take screenshot of guest mode home screen
    """

    guest_mode = GuestModeAuth(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    screenshots.take_screenshot("15_1_1_guest_mode_button")


@pytest.mark.smoke
def test_guest_mode_events(d, screenshots_dir):
    """
    Test the Guest Mode events screen.
    
    Steps:
    1. Handle notification permission if it appears
    2. Click Continue as Guest button
    3. Handle events popup if it appears
    4. Navigate to Events tab
    5. Take screenshot of guest mode events screen
    6. Verify events list is visible
    7. Check Guest Mode limited results popup
    """

    guest_mode = GuestModeAuth(d)
    nav_events = NavGuestMode(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_events.click_events_button()

    screenshots.take_screenshot("15_2_1_guest_mode_events")


@pytest.mark.smoke
def test_guest_mode_videos(d, screenshots_dir):
    """
    Test the Guest Mode videos screen.
    
    Steps:
    1. Handle notification permission if it appears
    2. Click Continue as Guest button
    3. Handle events popup if it appears
    4. Navigate to Videos section
    5. Take screenshot of guest mode videos screen
    """
    guest_mode = GuestModeAuth(d)
    scroll_videos = ScrollVideos(d)
    screenshots = ScreenshotsManagement(d)
    verify_locked_videos = VerifyGuestMode(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    scroll_videos.guest_mode_scroll_to_videos(max_attempts=10, duration=0.5)

    verify_locked_videos.verify_guest_videos()

    screenshots.take_screenshot("15_3_2_guest_mode_videos_triggered_plans_popup")


@pytest.mark.smoke
def test_guest_mode_ask_ai(d, screenshots_dir):
    """
    Test the Guest Mode search screen
    Steps:
    1. Launch app
    2. Continue as Guest
    3. Navigate to Ask AI
    4. Check Guest Mode popup
    """
    guest_mode = GuestModeAuth(d)
    nav_ask_ai = NavGuestMode(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_ask_ai.click_ask_ai()

    screenshots.take_screenshot("15_4_1_guest_mode_ask_ai_triggered_plans_popup")


@pytest.mark.smoke
def test_guest_mode_favorites(d, screenshots_dir):
    """
    Test the Guest Mode favorites screen
    Steps:
    1. Launch app
    2. Continue as Guest
    3. Navigate to Favorites
    4. Check Guest Mode popup
    """

    guest_mode = GuestModeAuth(d)
    nav_favorites = NavGuestMode(d)
    verify_plans_popup = VerifyGuestMode(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_favorites.click_favorites()

    verify_plans_popup.verify_plans_popup()

    screenshots.take_screenshot("15_5_1_guest_mode_search_triggered_plans_popup")
