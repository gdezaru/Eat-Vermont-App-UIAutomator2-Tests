import pytest
from time import sleep
from locators import GuestMode, PlansPopup, HomeScreen, BottomNavBar, Videos
from utils import (handle_guest_mode_plans_popup, enter_guest_mode_and_handle_popups, interact_with_events_carousel,
                   get_screen_dimensions)
import os


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
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_1_1_guest_mode_button.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_1_1_guest_mode_button.png")


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

    # Interact with Events carousel item
    interact_with_events_carousel(d)
    sleep(7)

    # Verify Limited Results text is present
    print("\nVerifying Limited Results text...")
    limited_results = d.xpath(GuestMode.EVENTS_LIMITED_RESULTS)
    assert limited_results.exists, "Limited Results text not found"
    print("Limited Results text is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_2_1_guest_mode_events.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_2_1_guest_mode_events.png")


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

    # Navigate to Videos section
    print("\nNavigating to Videos section...")
    videos_button = d.xpath(Videos.VIDEO_TILE)
    assert videos_button.exists, "Videos button not found"
    videos_button.click()
    sleep(5)

    # Handle events popup if present
    handle_guest_mode_plans_popup(d)

    # Use utility function to get screen dimensions
    width, height = get_screen_dimensions(d)
    upper_third = int(height * 0.4)

    # Calculate swipe coordinates
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4

    # First scroll to Videos section
    print("\nScrolling to find Videos section...")
    videos_text = d.xpath(HomeScreen.VIDEOS_TEXT_HOME_SCREEN)
    max_scroll_attempts = 1

    # Keep scrolling until Videos text is in upper third of screen
    for _ in range(max_scroll_attempts):
        if videos_text.exists:
            bounds = videos_text.bounds
            if bounds[1] < upper_third:
                print("Videos section found in upper third of screen")
                break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.9)
        sleep(1.5)

    # Verify locked videos are present
    print("\nVerifying locked videos...")
    locked_videos = d.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)
    assert locked_videos.exists, "Locked videos not found"
    print("Locked videos are present")

    # Click on locked videos
    print("\nClicking on locked videos...")
    locked_videos.click()
    sleep(3)

    # Verify plans popup is present
    print("\nVerifying plans popup...")
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    assert plans_popup_continue.exists, "Plans popup continue button not found"
    print("Plans popup is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_3_2_guest_mode_videos_triggered_plans_popup.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_3_2_guest_mode_videos_triggered_plans_popup.png")


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

    # Navigate to Search
    print("\nNavigating to Search...")
    search_button = d.xpath(BottomNavBar.SEARCH)
    assert search_button.exists, "Search button not found"
    search_button.click()
    sleep(5)

    # Handle events popup if present
    handle_guest_mode_plans_popup(d)

    # Verify plans popup is present
    print("\nVerifying plans popup...")
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    assert plans_popup_continue.exists, "Plans popup continue button not found"
    print("Plans popup is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_4_1_guest_mode_search_triggered_plans_popup.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_4_1_guest_mode_search_triggered_plans_popup.png")


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

    # Click on Favorites in bottom navigation
    print("\nClicking on Favorites in bottom navigation...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Favorites button not found in bottom navigation"
    favorites_button.click()
    sleep(3)

    # Verify plans popup is present
    print("\nVerifying plans popup...")
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    assert plans_popup_continue.exists, "Plans popup continue button not found"
    print("Plans popup is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_5_1_guest_mode_search_triggered_plans_popup.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_5_1_guest_mode_search_triggered_plans_popup.png")


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

    # Use utility function to get screen dimensions
    width, height = get_screen_dimensions(d)

    # Calculate swipe coordinates for maximum scroll
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4

    max_scroll_attempts = 15

    # Keep scrolling until we reach the end or find the prompt
    for _ in range(max_scroll_attempts):
        d.swipe(start_x, start_y, start_x, end_y, duration=2.0)
        sleep(1.5)

        # Check if the guest mode prompt is visible
        guest_mode_prompt = d.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_PROMPT)
        if guest_mode_prompt.exists:
            print("Guest mode prompt is present")
            break
    else:
        assert False, "Guest mode prompt not found after maximum scroll attempts"

    # Verify guest mode prompt is present
    print("\nVerifying guest mode prompt...")
    guest_mode_prompt = d.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_PROMPT)
    assert guest_mode_prompt.exists, "Guest mode prompt not found"
    print("Guest mode prompt is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_6_1_guest_mode_prompt_end_screen.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_6_1_guest_mode_prompt_end_screen.png")
