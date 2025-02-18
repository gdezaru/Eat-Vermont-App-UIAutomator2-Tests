import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import GeneralScrolling
from utils_ui_navigation import NavDayTripsTrails
from utils_ui_verification import VerifyTrails


@pytest.mark.smoke
def test_trails_screen(d, screenshots_dir):
    """
    Test the Trails functionality
    Steps:
    1. Sign in and prepare
    2. Navigate to Trails section
    3. Find and verify any trail name
    4. Verify trail status
    5. Take screenshot of trails main screen
    """
    sign_in = SignInPrepare(d)
    nav_trails = NavDayTripsTrails(d)
    verify_trails = VerifyTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()
    nav_trails.find_trails_text()
    nav_trails.click_trails_see_all()

    nav_trails.find_trail_name()
    verify_trails.verify_trail_status()

    screenshots.take_screenshot("9_1_1_trails_main_screen")


@pytest.mark.smoke
def test_trails_details(d, screenshots_dir):
    """
    Test the Trails details screen
    Steps:
    1. Sign in and prepare
    2. Navigate to Trails section
    3. Click Read More button
    4. Verify percentage progress
    5. Verify visits completed text and number
    6. Take screenshot of trail details
    7. Scroll using swipe
    8. Take screenshot of trail details visits
    """
    sign_in = SignInPrepare(d)
    nav_trails = NavDayTripsTrails(d)
    verify_trails = VerifyTrails(d)
    screenshots = ScreenshotsManagement(d)
    general_scrolling = GeneralScrolling(d)

    sign_in.sign_in_and_prepare()
    nav_trails.find_trails_text()
    nav_trails.click_trails_read_more()

    verify_trails.verify_trails_percentage_progress()
    verify_trails.verify_trails_visits()

    screenshots.take_screenshot("9_2_1_trail_details")

    general_scrolling.scroll_to_bottom()
    screenshots.take_screenshot("9_2_2_trail_details_visits")
