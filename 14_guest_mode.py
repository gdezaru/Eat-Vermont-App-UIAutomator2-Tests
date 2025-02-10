import pytest
from time import sleep
from locators import Events, GuestMode, LoginPage, PlansPopup, HomeScreen, BottomNavBar
from utils import handle_notification_permission


@pytest.mark.smoke
def test_guest_mode_button(d):
    """Test the Guest Mode Home screen"""
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

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    d.screenshot("14_1_1_guest_mode_button.png")


@pytest.mark.smoke
def test_guest_mode_events(d):
    """Test the Guest Mode events screen"""
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
    d.screenshot("14_2_1_guest_mode_events.png")


@pytest.mark.smoke
def test_guest_mode_videos(d):
    """Test the Guest Mode videos screen"""
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
    d.screenshot("14_3_1_guest_mode_videos.png")

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
    d.screenshot("14_3_2_guest_mode_videos_triggered_plans_popup.png")


@pytest.mark.smoke
def test_guest_mode_search(d):
    """Test the Guest Mode videos screen"""
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
    d.screenshot("14_4_1_guest_mode_search_triggered_plans_popup.png")


@pytest.mark.smoke
def test_guest_mode_favorites(d):
    """Test the Guest Mode videos screen"""
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
    d.screenshot("14_5_1_guest_mode_search_triggered_plans_popup.png")