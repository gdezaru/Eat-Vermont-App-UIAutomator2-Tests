import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import EventsScrolling, ScrollVideos
from utils_ui_navigation import NavEvents, NavViewMap, NavVideos, NavDayTripsTrails, NavBottomNavBar, \
    NavFavoritesVisitHistory
from utils_ui_verification import VerifyEvents, VerifyBusinesses, VerifyViewMap


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
    sign_in = SignInPrepare(d)
    nav_events = NavEvents(d)
    verify_events = VerifyEvents(d)
    verify_next_day = VerifyBusinesses(d)
    events_scrolling = EventsScrolling(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_events.click_see_all_events_home_screen()

    screenshots.take_screenshot("3_1_1_home_screen_events")

    current_day = verify_events.find_and_click_current_day()

    verify_next_day.try_next_day(current_day)

    events_scrolling.scroll_to_event_and_click(screenshots_dir, current_day)

    screenshots.take_screenshot(f"3_1_2_home_screen_event_details_{current_day.lower()}")


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
    sign_in = SignInPrepare(d)
    nav_map = NavViewMap(d)
    verify_map = VerifyViewMap(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_map.navigate_to_view_map()

    verify_map.verify_all_filters_visible()

    screenshots.take_screenshot("3_2_1_home_screen_view_map_opened")


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
    sign_in = SignInPrepare(d)
    scroll_videos = ScrollVideos(d)
    nav_videos = NavVideos(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_videos.scroll_to_videos()

    nav_videos.find_and_click_see_all_videos()

    screenshots.take_screenshot("3_3_1_home_screen_videos_opened")


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
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trips.click_day_trips_see_all()

    screenshots.take_screenshot("3_4_1_home_screen_day_trips_opened")


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
    sign_in = SignInPrepare(d)
    nav_bar = NavBottomNavBar(d)
    nav_favorites = NavFavoritesVisitHistory(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_favorites.click_favorites_button()
    screenshots.take_screenshot("3_5_1_bottom_nav_favorites_screen")

    nav_bar.click_events_button()

    screenshots.take_screenshot("3_5_2_bottom_nav_events_screen")

    nav_bar.click_home_button()

    screenshots.take_screenshot("3_5_3_bottom_nav_home_screen")
