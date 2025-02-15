import pytest
import os
from time import sleep
from locators import ViewMap
from utils_authentication import sign_in_and_prepare
from utils_scrolling import click_and_verify_element
from utils_ui_navigation import click_view_map


@pytest.mark.smoke
def test_view_map_filters(d, screenshots_dir):
    """
    Test the View Map filters functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Handle events popup
    3. Navigate to View Map section
    4. Verify Events filter is visible
    5. Verify Food & Drinks filter is visible
    6. Verify Farms filter is visible
    7. Verify Food Pantries filter is visible
    8. Take screenshot of all filters
    9. Click Events filter and verify
    10. Click Food & Drinks filter and verify
    11. Click Farms filter and verify
    12. Click Food Pantries filter and verify
    13. Document each filter state with screenshots
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

    # Assert that Food & Drinks filter is visible
    food_drinks_filter = d.xpath(ViewMap.FOOD_AND_DRINKS_FILTER)
    assert food_drinks_filter.exists, "Food & Drinks filter is not visible on the map screen"

    # Assert that Farms filter is visible
    farms_filter = d.xpath(ViewMap.FARMS_FILTER)
    assert farms_filter.exists, "Farms filter is not visible on the map screen"

    # Assert that Food Pantries filter is visible
    food_pantries_filter = d.xpath(ViewMap.FOOD_PANTRIES_FILTER)
    assert food_pantries_filter.exists, "Food Pantries filter is not visible on the map screen"

    # Take screenshot of all filters
    screenshot_path = os.path.join(screenshots_dir, "13_1_1_map_filters_present.png")
    d.screenshot(screenshot_path)

    # Click and verify Events filter
    click_and_verify_element(d, ViewMap.EVENTS_FILTER, "Events filter")
    screenshot_path = os.path.join(screenshots_dir, "13_1_2_events_filter_active.png")
    d.screenshot(screenshot_path)

    # Click and verify Food & Drinks filter
    click_and_verify_element(d, ViewMap.FOOD_AND_DRINKS_FILTER, "Food & Drinks filter")
    screenshot_path = os.path.join(screenshots_dir, "13_1_3_food_drinks_filter_active.png")
    d.screenshot(screenshot_path)
    # Click and verify Farms filter
    click_and_verify_element(d, ViewMap.FARMS_FILTER, "Farms filter")
    screenshot_path = os.path.join(screenshots_dir, "13_1_4_farms_filter_active.png")
    d.screenshot(screenshot_path)

    # Click and verify Food Pantries filter
    click_and_verify_element(d, ViewMap.FOOD_PANTRIES_FILTER, "Food Pantries filter")
    screenshot_path = os.path.join(screenshots_dir, "13_1_5_food_pantries_filter_active.png")
    d.screenshot(screenshot_path)
