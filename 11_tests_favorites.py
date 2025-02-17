import pytest
import os
from time import sleep
from locators import MyFavorites, Businesses

from utils_authentication import sign_in_and_prepare
from utils_device_interaction import search_and_submit
from utils_ui_navigation import (click_favorites_button, click_first_event_search_result, add_favorite_event,
                                 add_favorite_business, click_first_business_search_result, find_trails_text,
                                 click_trails_read_more, add_favorite_trail, verify_and_remove_favorite_event,
                                 verify_and_remove_favorite_business, verify_and_remove_favorite_trail)
from utils_ui_verification import verify_businesses_section_present

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
    3. Interact with Events carousel item
    4. Find and click the favorite icon
    5. Take screenshot
    """
    sign_in_and_prepare(d)

    search_term = "Burlington"
    search_and_submit(d, search_term)
    sleep(5)

    click_first_event_search_result(d)

    add_favorite_event(d)

    # Take screenshot
    screenshot_path = os.path.join(screenshots_dir, "11_1_1_event_favorited.png")
    d.screenshot(screenshot_path)


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

    # Use utility function to search and submit
    search_and_submit(d, menu_business_name)

    # Wait for and verify Businesses section is present
    verify_businesses_section_present(d)

    click_first_business_search_result(d, menu_business_name)

    add_favorite_business(d)

    # Take screenshot of favorited business
    screenshot_path = os.path.join(screenshots_dir, "11_2_1_business_favorited.png")
    d.screenshot(screenshot_path)


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

    find_trails_text(d)
    sleep(2)

    click_trails_read_more(d)

    add_favorite_trail(d)

    # Take screenshot of favorited trail
    screenshot_path = os.path.join(screenshots_dir, "11_4_1_trail_favorited.png")
    d.screenshot(screenshot_path)


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

    click_favorites_button(d)

    # Takes a screenshot of the favorited event
    screenshot_path = os.path.join(screenshots_dir, "11_5_1_favorited_event_before_removal.png")
    d.screenshot(screenshot_path)

    verify_and_remove_favorite_event(d)

    # Takes a screenshot of the favorites screen after removing the event from favorites
    screenshot_path = os.path.join(screenshots_dir, "11_5_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)


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
    click_favorites_button(d)

    # Takes a screenshot of the favorited business
    screenshot_path = os.path.join(screenshots_dir, "11_6_1_favorited_business_before_removal.png")
    d.screenshot(screenshot_path)

    verify_and_remove_favorite_business(d)

    # Takes a screenshot of the favorites screen after removing the business from favorites
    screenshot_path = os.path.join(screenshots_dir, "11_6_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)


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
    click_favorites_button(d)

    # Takes a screenshot of the favorited trail
    screenshot_path = os.path.join(screenshots_dir, "11_8_1_favorited_trail_before_removal.png")
    d.screenshot(screenshot_path)

    verify_and_remove_favorite_trail(d)

    # Takes a screenshot of the favorites screen after removing the trail from favorites
    screenshot_path = os.path.join(screenshots_dir, "11_8_2_favorites_after_removal.png")
    d.screenshot(screenshot_path)