import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, HomeScreenTiles, Events, Videos
from utils import (
    handle_notification_permission, sign_in_user, handle_events_popup
)

@pytest.mark.smoke
def test_videos_screen(d):
    """
    Test the Videos screen
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Videos section
    5. Verify video tiles are present
    6. Take a screenshot of the Videos screen
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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


@pytest.mark.smoke
def test_video_details_card(d):
    """
    Test the video details card
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Videos section
    5. Select a video from the list
    6. Verify video details card is displayed
    7. Take a screenshot of the video details
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
