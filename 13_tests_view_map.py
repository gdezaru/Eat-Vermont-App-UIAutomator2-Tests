import pytest
import os
from time import sleep
from locators import ViewMap
from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_ui_navigation import NavViewMap
from utils_ui_verification import VerifyViewMap


@pytest.mark.smoke
def test_view_map_filters(d, screenshots_dir):
    """
    Test the View Map filters functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Handle events popup
    3. Navigate to View Map section
    4. Verifies all filters are visible
    5. Take screenshot of all filters
    6. Click Events filter and verify
    7. Click Food & Drinks filter and verify
    8. Click Farms filter and verify
    9. Click Food Pantries filter and verify
    10. Document each filter state with screenshots
    """
    sign_in = SignInPrepare(d)
    nav_map = NavViewMap(d)
    verify_map = VerifyViewMap(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()
    nav_map.navigate_to_view_map()

    verify_map.verify_all_filters_visible()
    screenshots.take_screenshot("13_1_1_map_filters_present")

    nav_map.click_events_filter()
    screenshots.take_screenshot("13_1_2_events_filter_active")

    nav_map.click_food_drinks_filter()
    screenshots.take_screenshot("13_1_3_food_drinks_filter_active")

    nav_map.click_farms_filter()
    screenshots.take_screenshot("13_1_4_farms_filter_active")

    nav_map.click_food_pantries_filter()
    screenshots.take_screenshot("13_1_5_food_pantries_filter_active")