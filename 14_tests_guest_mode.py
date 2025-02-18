import pytest
import os

from utils_authentication import enter_guest_mode_and_handle_popups
from utils_scrolling import guest_mode_scroll_to_videos
from utils_ui_navigation import guest_mode_click_events_button, guest_mode_click_search, guest_mode_click_favorites
from utils_ui_verification import guest_mode_verify_events_limited_results_text, guest_mode_verify_locked_videos, \
    guest_mode_verify_plans_popup, guest_mode_home_screen_prompt


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

    enter_guest_mode_and_handle_popups(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_1_1_guest_mode_button.png")
    d.screenshot(screenshot_path)


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

    enter_guest_mode_and_handle_popups(d)

    guest_mode_click_events_button(d)

    guest_mode_verify_events_limited_results_text(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_2_1_guest_mode_events.png")
    d.screenshot(screenshot_path)


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
    enter_guest_mode_and_handle_popups(d)

    guest_mode_scroll_to_videos(d)

    guest_mode_verify_locked_videos(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_3_2_guest_mode_videos_triggered_plans_popup.png")
    d.screenshot(screenshot_path)


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
    enter_guest_mode_and_handle_popups(d)

    guest_mode_click_search(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_4_1_guest_mode_search_triggered_plans_popup.png")
    d.screenshot(screenshot_path)


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

    enter_guest_mode_and_handle_popups(d)

    guest_mode_click_favorites(d)

    guest_mode_verify_plans_popup(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_5_1_guest_mode_search_triggered_plans_popup.png")
    d.screenshot(screenshot_path)


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

    enter_guest_mode_and_handle_popups(d)

    guest_mode_home_screen_prompt(d)

    # Take a confirmation screenshot
    screenshot_path = os.path.join(screenshots_dir, "14_6_1_guest_mode_prompt_end_screen.png")
    d.screenshot(screenshot_path)
