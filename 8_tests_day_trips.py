import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_ui_navigation import NavDayTripsTrails


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
    7. Click Read More button
    8. Verify day trip details screen
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()
    read_more_button = nav_trips.find_day_trips_text()
    nav_trips.click_day_trips_read_more(read_more_button)

    screenshots.take_screenshot("8_1_1_day_trips_details")
