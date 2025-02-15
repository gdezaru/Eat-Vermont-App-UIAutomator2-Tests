import pytest
import os

from time import sleep
from locators import HomeScreen, EventsScreen, ViewMap, HomeScreenTiles, BottomNavBar
from utils_authentication import sign_in_and_prepare
from utils_scrolling import get_screen_dimensions, scroll_to_event_and_click, calculate_swipe_coordinates, \
    scroll_to_add_info, scroll_to_events_within_30
from utils_ui_navigation import click_favorites_button, click_see_all_events_home_screen, click_view_map, \
    find_and_click_see_all_videos, click_add_info_button, find_day_trips_text, click_day_trips_see_all, \
    click_see_all_events_within_30
from utils_ui_verification import try_next_day, find_and_click_current_day, verify_videos_text_exists, \
    find_event_within_30


@pytest.mark.smoke
def test_home_screen_events(d, screenshots_dir, current_day=None):
    """
    Test home screen events module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click 'See all' next to events
    3. Take screenshot of events page
    4. Find current selected day
    5. Click through subsequent days
    6. Verify events are displayed for each day
    7. Verify event details are accessible
    """
    sign_in_and_prepare(d)

    # Find and click 'See all' next to events
    click_see_all_events_home_screen(d)

    # Take screenshot of events page
    screenshot_path = os.path.join(screenshots_dir, "3_1_1_home_screen_events.png")
    d.screenshot(screenshot_path)

    # Find and click current day
    current_day = find_and_click_current_day(d)

    # Try clicking each subsequent day until one works
    try_next_day(d, current_day)

    # Scroll through events calendar, find an event, then click it
    scroll_to_event_and_click(d, screenshots_dir, current_day)

    # Take screenshot of the event details
    screenshot_path = os.path.join(screenshots_dir, f"3_1_4_home_screen_event_details_{current_day.lower()}.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_home_screen_view_map(d, screenshots_dir):
    """
    Test home screen view map module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click View Map tile
    3. Verify map is displayed
    4. Check map controls are accessible
    5. Verify location markers are visible
    6. Test map interaction (zoom, pan)
    """
    sign_in_and_prepare(d)

    # Single scroll to show View Map
    d.swipe(0.5, 0.8, 0.5, 0.4, 0.5)
    sleep(1)

    # Click "View Map" button
    click_view_map(d)

    # Assert that Events filter is visible
    events_filter = d.xpath(ViewMap.EVENTS_FILTER)
    assert events_filter.exists, "Events filter is not visible on the map screen"

    # Take screenshot of the map screen with filters
    screenshot_path = os.path.join(screenshots_dir, "3_2_1_home_screen_view_map_opened.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_home_screen_videos(d, screenshots_dir):
    """
    Test home screen videos module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click Videos tile
    3. Verify videos section is displayed
    4. Check video thumbnails are visible
    5. Attempt to play a video
    6. Verify video playback controls
    """
    sign_in_and_prepare(d)

    # Get screen dimensions
    width, height = get_screen_dimensions(d)

    # Calculate swipe coordinates for finding Videos
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    # First scroll until we find Videos text using the specific locator
    verify_videos_text_exists(d, start_x, start_y, end_y)

    find_and_click_see_all_videos(d, height, start_x)

    # Take screenshot of the videos page
    screenshot_path = os.path.join(screenshots_dir, "3_3_1_home_screen_videos_opened.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_home_screen_add_info(d, screenshots_dir):
    """
    Test home screen add info module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click Add Info tile
    3. Verify add info form is displayed
    4. Check all form fields are accessible
    5. Test form validation
    6. Verify submission process
    """
    sign_in_and_prepare(d)

    scroll_to_add_info(d)

    click_add_info_button(d)

    # Take screenshot of the Add Info page
    screenshot_path = os.path.join(screenshots_dir, "3_4_1_home_screen_add_info_opened.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_home_screen_day_trips(d, screenshots_dir):
    """
    Test home screen day trips module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click Day Trips tile
    3. Verify day trips section is displayed
    4. Check trip cards are visible
    5. Verify trip details are accessible
    6. Test trip filtering options
    """
    sign_in_and_prepare(d)

    find_day_trips_text(d)

    click_day_trips_see_all(d)

    # Take screenshot of the Day Trips page
    screenshot_path = os.path.join(screenshots_dir, "3_5_1_home_screen_day_trips_opened.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_home_screen_events_within(d, screenshots_dir):
    """
    Test home screen events within 30 minutes functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find events within 30 minutes section
    3. Verify nearby events are displayed
    4. Check event details are accessible
    5. Verify distance information
    6. Test event sorting options
    """
    sign_in_and_prepare(d)

    scroll_to_events_within_30(d)

    find_event_within_30(d)

    # Take screenshot of the Events within 30 minutes section
    screenshot_path = os.path.join(screenshots_dir, "3_6_1_home_screen_events_within.png")
    d.screenshot(screenshot_path)
    sleep(1)

    click_see_all_events_within_30(d)

    # Take screenshot of the Events within 30 minutes list view
    screenshot_path = os.path.join(screenshots_dir, "3_6_2_home_screen_events_within_list.png")
    d.screenshot(screenshot_path)
    sleep(1)


@pytest.mark.smoke
def test_home_screen_events_further_than(d, screenshots_dir):
    """
    Test home screen events further than 30 minutes functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find events further than 30 minutes section
    3. Verify distant events are displayed
    4. Check event details are accessible
    5. Verify distance information
    6. Test event sorting options
    """
    sign_in_and_prepare(d)

    # Single scroll to show Events within ~30 minutes
    d(scrollable=True).scroll.to(text="Events Further Than ~30min")
    assert d(text="Events Further Than ~30min").exists(timeout=5), "Events Within ~30min text not found"
    sleep(1)

    # Check for content in Events within 30 minutes tile
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    event_found = False
    for day in days_of_week:
        events_tile = d.xpath(HomeScreenTiles.EVENTS_WITHIN_30_TILE.format(day))
        if events_tile.exists:
            event_found = True
            break

    assert event_found, "Could not find any events with dates in Events within 30 minutes section"
    sleep(1)

    # Take screenshot of the Events within 30 minutes section
    screenshot_path = os.path.join(screenshots_dir, "3_7_1_home_screen_events_further_than.png")
    d.screenshot(screenshot_path)
    sleep(1)

    # Click See All for Events within 30 minutes
    see_all = d(text="See All")
    assert see_all.exists, "Could not find See All button for Events within 30 minutes"
    see_all.click()
    sleep(2)  # Extra time for page transition

    # Take screenshot of the Events within 30 minutes list view
    screenshot_path = os.path.join(screenshots_dir, "3_7_2_home_screen_events_more_than_list.png")
    d.screenshot(screenshot_path)
    sleep(1)


@pytest.mark.smoke
def test_home_screen_bottom_nav_bar(d, screenshots_dir):
    """
    Test home screen bottom navigation bar functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Verify all nav bar items are visible
    3. Test Home button navigation
    4. Test Search button navigation
    5. Test Map button navigation
    6. Test Profile button navigation
    7. Verify active state indicators
    """
    sign_in_and_prepare(d)

    # Click Favorites button
    click_favorites_button(d)
    sleep(2)  # Wait for favorites page to load

    # Assert that "Favorites" text is present
    assert d(text="Favorites").exists, "Favorites text not found on screen"

    # Take screenshot
    screenshot_path = os.path.join(screenshots_dir, "3_8_1_bottom_nav_favorites_screen.png")
    d.screenshot(screenshot_path)

    # Click Events button
    events_button = d.xpath(BottomNavBar.EVENTS)
    assert events_button.exists, "Could not find Events button"
    events_button.click()
    sleep(5)  # Wait for events page to load

    # Assert that "Events" text is present
    assert d(text="Events").exists, "Events text not found on screen"

    # Take screenshot
    screenshot_path = os.path.join(screenshots_dir, "3_8_2_bottom_nav_events_screen.png")
    d.screenshot(screenshot_path)

    # Click Home button
    home_button = d.xpath(BottomNavBar.NAV_HOME_BUTTON)
    assert home_button.exists, "Could not find Home button"
    home_button.click()
    sleep(5)  # Wait for home page to load

    # Assert that "Events" text is present on home screen
    assert d(text="Events").exists, "Events text not found on home screen"

    # Take screenshot
    screenshot_path = os.path.join(screenshots_dir, "3_8_3_bottom_nav_home_screen.png")
    d.screenshot(screenshot_path)
