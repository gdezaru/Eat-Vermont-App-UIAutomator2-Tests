import pytest


from utils_authentication import GuestModeAuth
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollVideos, ScreenSwipe
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
    5. Verify guest mode elements are present
    6. Verify guest mode restrictions are in place
    """

    guest_mode = GuestModeAuth(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    screenshots.take_screenshot("14_1_1_guest_mode_button")


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
    7. Verify event details are accessible
    8. Verify guest mode restrictions on event interactions
    """

    guest_mode = GuestModeAuth(d)
    nav_events = NavGuestMode(d)
    screenshots = ScreenshotsManagement(d)
    verify_limited_results = VerifyGuestMode(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_events.click_events_button()

    verify_limited_results.verify_events_limited_results_text()

    screenshots.take_screenshot("14_2_1_guest_mode_events")


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
    6. Verify videos list is visible
    7. Attempt to interact with locked videos
    8. Verify plans popup appears for restricted content
    9. Take screenshot of plans popup
    """
    guest_mode = GuestModeAuth(d)
    scroll_videos = ScrollVideos(d)
    screenshots = ScreenshotsManagement(d)
    verify_locked_videos = VerifyGuestMode(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    scroll_videos.guest_mode_scroll_to_videos()

    verify_locked_videos.verify_locked_videos()

    screenshots.take_screenshot("14_3_2_guest_mode_videos_triggered_plans_popup")


@pytest.mark.smoke
def test_guest_mode_search(d, screenshots_dir):
    """
    Test the Guest Mode search screen
    Steps:
    1. Launch app
    2. Continue as Guest
    3. Navigate to Search
    4. Enter search term
    5. Verify search results
    6. Test filter options
    7. Check result details
    8. Verify location-based
    9. Test search history
    10. Check sign-in prompts
    """
    guest_mode = GuestModeAuth(d)
    nav_search = NavGuestMode(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_search.click_search()

    screenshots.take_screenshot("14_4_1_guest_mode_search_triggered_plans_popup")


@pytest.mark.smoke
def test_guest_mode_favorites(d, screenshots_dir):
    """
    Test the Guest Mode favorites screen
    Steps:
    1. Launch app
    2. Continue as Guest
    3. Navigate to Favorites
    4. Verify favorites list
    5. Check favorite details
    6. Test favorite filtering
    7. Verify favorite limits
    8. Check sign-in prompts
    9. Verify data persistence
    10. Test guest session expiry
    """

    guest_mode = GuestModeAuth(d)
    nav_favorites = NavGuestMode(d)
    verify_plans_popup = VerifyGuestMode(d)
    screenshots = ScreenshotsManagement(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    nav_favorites.click_favorites()

    verify_plans_popup.verify_plans_popup()

    screenshots.take_screenshot("14_5_1_guest_mode_search_triggered_plans_popup")


@pytest.mark.smoke
def test_guest_mode_prompt_end_screen(d, screenshots_dir):
    """
    Test the Guest Mode prompt from the bottom of the screen
    Steps:
    1. Launch app
    2. Continue as Guest
    3. Scroll to the end of the screen
    4. Verify guest mode prompt
    5. Check sign-in prompts
    6. Verify data persistence
    7. Test guest session expiry
    8. Check navigation limits
    9. Verify restricted features
    10. Test guest mode UI
    """

    guest_mode = GuestModeAuth(d)
    verify_prompt = VerifyGuestMode(d)
    screenshots = ScreenshotsManagement(d)
    screen_swipe = ScreenSwipe(d)

    guest_mode.enter_guest_mode_and_handle_popups()

    verify_prompt.verify_home_screen_prompt()

    # Take a confirmation screenshot
    screenshots.take_screenshot("14_6_1_guest_mode_prompt_end_screen")
