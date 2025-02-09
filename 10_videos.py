import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, HomeScreenTiles, Events, Videos
from utils import (
    handle_notification_permission,
    scroll_to_find_text,
    scroll_until_element_is_visible
)


def test_videos_screen(d):
    """Test the Videos screen"""
    handle_notification_permission(d)

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
        sleep(3)  # Wait for popup to close

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
    
    # First scroll until we find Videos text using the specific locator
    print("\nScrolling to find Videos section...")
    videos_text = d.xpath(HomeScreen.VIDEOS_TEXT_HOME_SCREEN)
    max_scroll_attempts = 5
    
    # Calculate swipe coordinates for finding Videos
    start_x = width // 2
    start_y = (height * 3) // 4  # Start from 75%
    end_y = height // 4          # End at 25%
    
    for _ in range(max_scroll_attempts):
        if videos_text.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)
    
    assert videos_text.exists, "Videos section not found"
    sleep(1)

    # Now do smaller scrolls to find See All
    print("\nFine-tuning scroll to find See All button...")
    max_small_scrolls = 3
    videos_see_all = d.xpath(HomeScreen.VIDEOS_SEE_ALL)
    
    # Smaller swipes for fine-tuning
    fine_tune_start_y = (height * 3) // 5  # Start from 60%
    fine_tune_end_y = (height * 2) // 5    # End at 40%
        
    for _ in range(max_small_scrolls):
        if videos_see_all.exists:
            break
        d.swipe(start_x, fine_tune_start_y, start_x, fine_tune_end_y, duration=1.0)
        sleep(1.5)
    
    assert videos_see_all.exists, "Could not find Videos See All button"
    videos_see_all.click()
    sleep(5)

    # Verify that video tiles are present
    print("\nVerifying video tiles are present...")
    video_tiles = d.xpath(Videos.VIDEO_TILE)
    assert video_tiles.exists, "No video tiles found on the Videos screen"
    
    # Take screenshot of the videos screen
    d.screenshot("10_1_1_videos_screen.png")
    print("Found video tiles successfully")


def test_video_details_card(d):
    """Test the Videos screen"""
    handle_notification_permission(d)

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
        sleep(3)  # Wait for popup to close

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
    
    assert videos_text.exists and videos_text.bounds[1] < upper_third, \
        "Videos section not found in upper third of screen"
    sleep(1)
    
    # Now look for video tile
    video_tile_locator = HomeScreenTiles.VIDEOS_TILE_TITLE
    max_attempts = 5
    
    print("\nLooking for video tile...")
    for _ in range(max_attempts):
        video_tile = d.xpath(video_tile_locator)
        if video_tile.exists:
            print("Found video tile, clicking...")
            video_tile.click()
            sleep(2)
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)
    
        assert video_tile.exists, "Failed to find video tile"
    
    # Take a screenshot of the video details
    d.screenshot("10_2_1_video_details.png")
