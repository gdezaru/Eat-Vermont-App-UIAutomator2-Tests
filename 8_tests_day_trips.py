import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollToCustomDayTrips
from utils_ui_navigation import NavDayTripsTrails, NavCustomDayTrips
from utils_ui_verification import VerifyCustomDayTrips


@pytest.mark.smoke
def test_day_trip_card(d, screenshots_dir):
    """
    Test the Day Trip card on the Home screen
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Day Trip section
    4. Verify Day Trip text is displayed
    5. Scroll to find Read More button
    6. Verify Read More button is displayed
    7. Tap Read More button
    8. Verify day trip details screen
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()
    read_more_button = nav_trips.find_day_trips_text()
    nav_trips.click_day_trips_read_more(read_more_button)

    screenshots.take_screenshot("8_1_1_day_trips_details")


@pytest.mark.smoke
def test_custom_day_trip_create_trip_screem(d, screenshots_dir):
    """
    Tests if the Custom Day Trips builder can be accessed from the home screen.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Checks the contents of the "Create Trip" screen (header, Add A Location button and Quick Suggestions)
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)
    verify_custom_trips = VerifyCustomDayTrips(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    verify_custom_trips.verify_create_trip_header()

    verify_custom_trips.verify_add_location()

    verify_custom_trips.verify_quick_suggestions()

    screenshots.take_screenshot("8_2_1_custom_day_trips_create_trip_screen")


def test_auto_generated_day_trip_events(d, screenshots_dir):
    """
    Tests the auto generation of a Day Trip in Custom Day Trips module.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Searches for a location
    6. Confirms the location
    7. Selects a date from the calendar
    8. Taps Auto-Recommend
    9. Selects Events
    10. Asserts that Advanced Filter button is present
    11.
    """
