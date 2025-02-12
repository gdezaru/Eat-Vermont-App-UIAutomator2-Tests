import pytest
from time import sleep
from locators import Events, MyFavorites, Businesses, HomeScreen, BottomNavBar
from utils import (
    handle_notification_permission, sign_in_user, handle_events_popup
)
from retry_decorator import retry


# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_add_favorite_events(d):
    """
    Tests the ability to add events to My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Events carousel item
    5. Find and click the favorite icon
    6. Take screenshot
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Events carousel item
    print("\nLocating Events carousel item...")
    carousel_item = d.xpath(Events.CAROUSEL_ITEM)
    assert carousel_item.exists, "Could not find Events carousel item"
    print("Events carousel item found, clicking...")
    carousel_item.click()
    sleep(7)  # Wait for event details to load

    # Find and click the favorite icon
    print("\nLocating favorite icon...")
    favorite_icon = d.xpath(MyFavorites.FAVORITE_EVENTS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    print("Favorite icon found, clicking...")
    favorite_icon.click()
    sleep(2)  # Wait for favorite action to complete

    # Take screenshot
    screenshot_path = "11_1_1_event_favorited.png"
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_add_favorite_businesses(d):
    """
    Tests the ability to add businesses to My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Find and click Search in bottom navigation
    5. Find and click search field
    6. Enter search term and submit
    7. Wait for and verify Businesses section is present
    8. Click on Big Fatty's BBQ search result under Businesses
    9. Find and click the favorite icon
    10. Take screenshot of favorited business
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys(menu_business_name)
    sleep(1)
    d.press("enter")
    sleep(10)

    # Wait for and verify Businesses section is present
    print("\nVerifying Businesses section is present...")
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"
    print("Found Businesses section")

    # Click on Big Fatty's BBQ search result under Businesses
    print("\nLocating Big Fatty's BBQ under Businesses section...")
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
    assert search_result.exists, "Big Fatty's BBQ not found under Businesses section"
    print("Found Big Fatty's BBQ, clicking...")
    search_result.click()
    sleep(3)

    # Find and click the favorite icon
    print("\nLocating favorite icon...")
    favorite_icon = d.xpath(MyFavorites.FAVORITE_BUSINESS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    print("Favorite icon found, clicking...")
    favorite_icon.click()
    sleep(2)

    # Take screenshot of favorited business
    print("\nTook screenshot: 11_2_1_business_favorited.png")
    d.screenshot("11_2_1_business_favorited.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_add_favorite_videos(d):
    """
    Tests the ability to add videos to My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Get screen dimensions for scrolling
    5. Calculate swipe coordinates
    6. First scroll to Videos section
    7. Find and click the favorite icon
    8. Take screenshot of favorited video
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

    # Find and click the favorite icon
    print("\nLocating favorite icon...")
    favorite_icon = d.xpath(MyFavorites.FAVORITE_VIDEOS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    print("Favorite icon found, clicking...")
    favorite_icon.click()
    sleep(2)

    # Take screenshot of favorited video
    print("\nTook screenshot: 11_3_1_video_favorited.png")
    d.screenshot("11_3_1_video_favorited.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_add_favorite_trails(d):
    """
    Tests the ability to add trails to My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Trails button
    5. Find and click the favorite icon
    6. Take screenshot of favorited trail
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Trails button
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)

    # Find and click the favorite icon
    print("\nLocating favorite icon...")
    favorite_icon = d.xpath(MyFavorites.FAVORITE_TRAILS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    print("Favorite icon found, clicking...")
    favorite_icon.click()
    sleep(2)

    # Take screenshot of favorited trail
    print("\nTook screenshot: 11_4_1_trail_favorited.png")
    d.screenshot("11_4_1_trail_favorited.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_remove_favorite_events(d):
    """
    Tests the ability to remove events from My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Favorites button in bottom navigation
    5. Verify favorited event is present and take screenshot
    6. Click on favorite icon to remove from favorites
    7. Verify event is no longer in favorites
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Favorites button in bottom navigation
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)

    # Verify favorited event is present and take screenshot
    print("\nVerifying favorited event is present...")
    favorite_event = d.xpath(MyFavorites.ADDED_FAVORITE_EVENT)
    assert favorite_event.exists, "Could not find favorited event"
    print("Found favorited event")
    print("\nTook screenshot: 11_5_1_favorited_event_before_removal.png")
    d.screenshot("11_5_1_favorited_event_before_removal.png")

    # Click on favorite icon to remove from favorites
    print("\nRemoving event from favorites...")
    favorite_event.click()
    sleep(2)

    # Verify event is no longer in favorites
    print("\nVerifying event was removed from favorites...")
    assert not favorite_event.exists, "Event is still present in favorites"
    print("Event successfully removed from favorites")
    print("\nTook screenshot: 11_5_2_favorites_after_removal.png")
    d.screenshot("11_5_2_favorites_after_removal.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_remove_favorite_businesses(d):
    """
    Tests the ability to remove businesses from My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Favorites button in bottom navigation
    5. Verify favorited business is present and take screenshot
    6. Click on favorite icon to remove from favorites
    7. Verify business is no longer in favorites
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Favorites button in bottom navigation
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)

    # Verify favorited business is present and take screenshot
    print("\nVerifying favorited business is present...")
    favorite_business = d.xpath(MyFavorites.ADDED_FAVORITE_BUSINESS)
    assert favorite_business.exists, "Could not find favorited business"
    print("Found favorited business")
    print("\nTook screenshot: 11_6_1_favorited_business_before_removal.png")
    d.screenshot("11_6_1_favorited_business_before_removal.png")

    # Click on favorite icon to remove from favorites
    print("\nRemoving business from favorites...")
    favorite_business.click()
    sleep(2)

    # Verify business is no longer in favorites
    print("\nVerifying business was removed from favorites...")
    assert not favorite_business.exists, "Business is still present in favorites"
    print("Business successfully removed from favorites")
    sleep(3)  # Wait for UI to update
    print("\nTook screenshot: 11_6_2_favorites_after_removal.png")
    d.screenshot("11_6_2_favorites_after_removal.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_remove_favorite_videos(d):
    """
    Tests the ability to remove videos from My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Favorites button in bottom navigation
    5. Verify favorited video is present and take screenshot
    6. Click on favorite icon to remove from favorites
    7. Verify video is no longer in favorites
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Favorites button in bottom navigation
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)

    # Verify favorited video is present and take screenshot
    print("\nVerifying favorited video is present...")
    favorite_video = d.xpath(MyFavorites.ADDED_FAVORITE_VIDEO)
    assert favorite_video.exists, "Could not find favorited video"
    print("Found favorited video")
    print("\nTook screenshot: 11_7_1_favorited_video_before_removal.png")
    d.screenshot("11_9_1_favorited_video_before_removal.png")

    # Click on favorite icon to remove from favorites
    print("\nRemoving video from favorites...")
    favorite_video.click()
    sleep(2)

    # Verify video is no longer in favorites
    print("\nVerifying video was removed from favorites...")
    assert not favorite_video.exists, "Video is still present in favorites"
    print("Video successfully removed from favorites")
    sleep(5)  # Wait for UI to update
    print("\nTook screenshot: 11_7_2_favorites_after_removal.png")
    d.screenshot("11_9_2_favorites_after_removal.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_remove_favorite_trails(d):
    """
    Tests the ability to remove trails from My Favorites.
    Steps:
    1. Handle notification permissions
    2. Sign in using the utility method
    3. Handle events popup using the utility method
    4. Click on Favorites button in bottom navigation
    5. Verify favorited trail is present and take screenshot
    6. Click on favorite icon to remove from favorites
    7. Verify trail is no longer in favorites
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Favorites button in bottom navigation
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)

    # Verify favorited trail is present and take screenshot
    print("\nVerifying favorited trail is present...")
    favorite_trail = d.xpath(MyFavorites.ADDED_FAVORITE_TRAIL)
    assert favorite_trail.exists, "Could not find favorited trail"
    print("Found favorited trail")
    print("\nTook screenshot: 11_8_1_favorited_trail_before_removal.png")
    d.screenshot("11_7_1_favorited_trail_before_removal.png")

    # Click on favorite icon to remove from favorites
    print("\nRemoving trail from favorites...")
    favorite_trail.click()
    sleep(2)

    # Verify trail is no longer in favorites
    print("\nVerifying trail was removed from favorites...")
    assert not favorite_trail.exists, "Trail is still present in favorites"
    print("Trail successfully removed from favorites")
    sleep(5)  # Wait for UI to update
    print("\nTook screenshot: 11_8_2_favorites_after_removal.png")
    d.screenshot("11_7_2_favorites_after_removal.png")