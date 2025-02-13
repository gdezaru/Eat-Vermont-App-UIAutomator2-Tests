import pytest
from time import sleep
from locators import Events, MyFavorites, Businesses, HomeScreen, BottomNavBar
from utils import (
    sign_in_and_prepare
)
import os


# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
def test_add_favorite_events(d, screenshots_dir):
    """
    Tests the ability to add events to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Events carousel item
    4. Find and click the favorite icon
    5. Take screenshot
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_1_1_event_favorited.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
def test_add_favorite_businesses(d, screenshots_dir):
    """
    Tests the ability to add businesses to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Find and click Search in bottom navigation
    4. Find and click search field
    5. Enter search term and submit
    6. Wait for and verify Businesses section is present
    7. Click on Big Fatty's BBQ search result under Businesses
    8. Find and click the favorite icon
    9. Take screenshot of favorited business
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_2_1_business_favorited.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
def test_add_favorite_trails(d, screenshots_dir):
    """
    Tests the ability to add trails to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Trails button
    4. Find and click the favorite icon
    5. Take screenshot of favorited trail
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_4_1_trail_favorited.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
def test_remove_favorite_events(d, screenshots_dir):
    """
    Tests the ability to remove events from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited event is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify event is no longer in favorites
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_5_1_favorited_event_before_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")

    # Click on favorite icon to remove from favorites
    print("\nRemoving event from favorites...")
    favorite_event.click()
    sleep(2)

    # Verify event is no longer in favorites
    print("\nVerifying event was removed from favorites...")
    assert not favorite_event.exists, "Event is still present in favorites"
    print("Event successfully removed from favorites")
    screenshot_path = os.path.join(screenshots_dir, "11_5_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
def test_remove_favorite_businesses(d, screenshots_dir):
    """
    Tests the ability to remove businesses from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited business is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify business is no longer in favorites
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_6_1_favorited_business_before_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")

    # Click on favorite icon to remove from favorites
    print("\nRemoving business from favorites...")
    favorite_business.click()
    sleep(2)

    # Verify business is no longer in favorites
    print("\nVerifying business was removed from favorites...")
    assert not favorite_business.exists, "Business is still present in favorites"
    print("Business successfully removed from favorites")
    sleep(3)  # Wait for UI to update
    screenshot_path = os.path.join(screenshots_dir, "11_6_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")


@pytest.mark.smoke
def test_remove_favorite_trails(d, screenshots_dir):
    """
    Tests the ability to remove trails from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited trail is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify trail is no longer in favorites
    """
    sign_in_and_prepare(d)

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
    screenshot_path = os.path.join(screenshots_dir, "11_8_1_favorited_trail_before_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")

    # Click on favorite icon to remove from favorites
    print("\nRemoving trail from favorites...")
    favorite_trail.click()
    sleep(2)

    # Verify trail is no longer in favorites
    print("\nVerifying trail was removed from favorites...")
    assert not favorite_trail.exists, "Trail is still present in favorites"
    print("Trail successfully removed from favorites")
    sleep(5)  # Wait for UI to update
    screenshot_path = os.path.join(screenshots_dir, "11_8_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)
    print(f"\nTook screenshot: {screenshot_path}")