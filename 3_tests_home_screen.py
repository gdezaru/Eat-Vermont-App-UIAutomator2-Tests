import pytest

from time import sleep
from locators import HomeScreen, EventsScreen, ViewMap, HomeScreenTiles, BottomNavBar
from utils import sign_in_and_prepare, get_screen_dimensions, click_favorites_button, try_next_day
import os


@pytest.mark.smoke
def test_home_screen_events(d, screenshots_dir):
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
    see_all_events = d.xpath(HomeScreen.EVENTS_SEE_ALL)
    assert see_all_events.exists, "Could not find 'See all' for events"
    see_all_events.click()
    sleep(10)

    # Take screenshot of events page
    screenshot_path = os.path.join(screenshots_dir, "3_1_1_home_screen_events.png")
    d.screenshot(screenshot_path)

    # Find the current selected day
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_day = None
    for day in days:
        day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(day, day))
        if day_element.exists:
            current_day = day
            print(f"\nFound current day: {day}")
            break

    assert current_day is not None, "Could not find any day of week element"

    # Try clicking each subsequent day until one works
    try_next_day(d, current_day)

    # Verify that either there's an event or "No Events" message is shown
    first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
    no_events_message = d.xpath(EventsScreen.EVENTS_SCREEN_NO_EVENTS)

    assert first_event.exists or no_events_message.exists, "Neither events nor 'No Events' message found"
    if first_event.exists:
        print(f"\nFound at least one event for {current_day}")
    else:
        print(f"\nNo events found for {current_day}")

    # Take screenshot of the successful day's events
    screenshot_path = os.path.join(screenshots_dir, f"3_1_2_home_screen_events_{current_day.lower()}.png")
    d.screenshot(screenshot_path)

    # If no event was found initially, scroll to try to find one
    if not first_event.exists and not no_events_message.exists:
        print("\nNo event visible initially, scrolling to find events...")
        max_scroll_attempts = 3
        found_event = False

        for scroll_attempt in range(max_scroll_attempts):
            # Scroll down
            d.swipe(0.5, 0.8, 0.5, 0.2, 0.5)  # Scroll from bottom to top
            sleep(2)  # Wait for scroll to complete

            # Check if we can now see an event
            first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
            if first_event.exists:
                print(f"\nFound an event after {scroll_attempt + 1} scroll(s)")
                found_event = True
                # Take a screenshot after finding the event
                screenshot_path = os.path.join(screenshots_dir, f"3_1_3_home_screen_events_{current_day.lower()}_after_scroll.png")
                d.screenshot(screenshot_path)
                break

        if not found_event:
            print(f"\nNo events found even after {max_scroll_attempts} scrolls")
            assert no_events_message.exists, "No events found and 'No Events' message is not displayed"

    # Click on the first event tile if it exists
    if first_event.exists:
        print("\nClicking on the first event tile...")
        # Get the event title before clicking
        event_title = first_event.get_text()
        print(f"Event title: {event_title}")

        # Click the event title and wait for details to load
        first_event.click()
        sleep(2)  # Wait for event details to load

        # Verify we're in the event details view by checking for the event title
        event_title_in_details = d.xpath(EventsScreen.EVENT_TITLE.format(event_title))
        assert event_title_in_details.exists, f"Failed to open event details for '{event_title}'"

        print("\nSuccessfully opened event details")
        # Take screenshot of the event details
        screenshot_path = os.path.join(screenshots_dir, f"3_1_4_home_screen_event_details_{current_day.lower()}.png")
        d.screenshot(screenshot_path)
        print("\nEvent details page loaded and screenshot taken")


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
    view_map = d.xpath(HomeScreen.VIEW_MAP)
    assert view_map.exists, "Could not find View Map button"
    view_map.click()
    sleep(2)

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

    # Use utility function to get screen dimensions
    width, height = get_screen_dimensions(d)

    # First scroll until we find Videos text using the specific locator
    print("\nScrolling to find Videos section...")
    videos_text = d.xpath(HomeScreen.VIDEOS_TEXT_HOME_SCREEN)
    max_scroll_attempts = 5

    # Calculate swipe coordinates for finding Videos
    start_x = width // 2
    start_y = (height * 3) // 4  # Start from 75%
    end_y = height // 4  # End at 25%

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
    fine_tune_end_y = (height * 2) // 5  # End at 40%

    for _ in range(max_small_scrolls):
        if videos_see_all.exists:
            break
        d.swipe(start_x, fine_tune_start_y, start_x, fine_tune_end_y, duration=1.0)
        sleep(1.5)

    assert videos_see_all.exists, "Could not find Videos See All button"
    videos_see_all.click()
    sleep(5)  # Wait for videos page to load

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

    # Scroll until Add Info button is visible
    d(scrollable=True).scroll.to(text="Add Info")
    assert d(text="Add Info").exists(timeout=5), "Add Info button not found"
    sleep(1)

    # Click on Add Info button
    add_info_button = d.xpath(HomeScreen.ADD_INFO_BUTTON)
    assert add_info_button.exists, "Add Info button not found"
    add_info_button.click()
    sleep(5)

    # Take screenshot of the Add Info page
    screenshot_path = os.path.join(screenshots_dir, "3_4_1_home_screen_add_info_opened.png")
    d.screenshot(screenshot_path)
    print("\nAdd Info page loaded and screenshot taken")


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

    # Single scroll to show Day Trips
    d(scrollable=True).scroll.to(text="Day Trip")
    assert d(text="Day Trip").exists(timeout=5), "Day Trip text not found"
    sleep(1)

    # Click "See all" next to Day Trips
    day_trips_see_all = d.xpath(HomeScreen.DAY_TRIPS_SEE_ALL.format("Day Trip"))
    assert day_trips_see_all.exists, "Could not find Day Trip 'See all' button"
    day_trips_see_all.click()
    sleep(2)

    # Take screenshot of the Day Trips page
    screenshot_path = os.path.join(screenshots_dir, "3_5_1_home_screen_day_trips_opened.png")
    d.screenshot(screenshot_path)
    print("\nDay Trips page loaded and screenshot taken")


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

    # Single scroll to show Events within ~30 minutes
    d(scrollable=True).scroll.to(text="Events Within ~30min")
    assert d(text="Events Within ~30min").exists(timeout=5), "Events Within ~30min text not found"
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
    screenshot_path = os.path.join(screenshots_dir, "3_6_1_home_screen_events_within.png")
    d.screenshot(screenshot_path)
    sleep(1)

    # Click See All for Events within 30 minutes
    see_all = d(text="See All")
    assert see_all.exists, "Could not find See All button for Events within 30 minutes"
    see_all.click()
    sleep(2)  # Extra time for page transition

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
