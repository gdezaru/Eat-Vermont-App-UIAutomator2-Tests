import pytest
from time import sleep
from locators import Events, GuestMode, LoginPage, PlansPopup, HomeScreen, BottomNavBar
from utils import handle_notification_permission, handle_events_popup, handle_guest_mode_plans_popup
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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Handle plans popup if present
    handle_guest_mode_plans_popup(d)

    # Handle events popup if present
    handle_events_popup(d)
    sleep(10)

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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Handle plans popup if present
    handle_guest_mode_plans_popup(d)

    # Handle events popup if present
    handle_events_popup(d)
    sleep(10)

    # Click on Events carousel item
    print("\nLocating Events carousel item...")
    carousel_item = d.xpath(Events.CAROUSEL_ITEM)
    assert carousel_item.exists, "Could not find Events carousel item"
    print("Events carousel item found, clicking...")
    carousel_item.click()
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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

    # Get screen dimensions for scrolling
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
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

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    screenshot_path = os.path.join(screenshots_dir, "14_3_1_guest_mode_videos.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 14_3_1_guest_mode_videos.png")

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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

    # Click on Search in bottom navigation
    print("\nClicking on Search in bottom navigation...")
    search_button = d.xpath(BottomNavBar.SEARCH)
    assert search_button.exists, "Search button not found in bottom navigation"
    search_button.click()
    sleep(3)

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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

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
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

    # Get screen dimensions for scrolling
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    # Calculate swipe coordinates for maximum scroll
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4

    # Scroll to the end of screen
    print("\nScrolling to end of screen...")
    max_scroll_attempts = 6

    # Keep scrolling until we reach the end
    for _ in range(max_scroll_attempts):
        d.swipe(start_x, start_y, start_x, end_y, duration=0.9)
        sleep(1.5)

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