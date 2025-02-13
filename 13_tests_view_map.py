import pytest
from time import sleep
from locators import HomeScreen, ViewMap
from utils import sign_in_and_prepare
import os


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

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Single scroll to show View Map
    d.swipe(0.5, 0.8, 0.5, 0.4, 0.5)
    sleep(1)

    # Click "View Map" button
    view_map = d.xpath(HomeScreen.VIEW_MAP)
    assert view_map.exists, "Could not find View Map button"
    view_map.click()
    sleep(5)

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
    print("\nTaking screenshot of all filters...")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 13_1_1_map_filters_present.png")

    # Click Events filter and take screenshot
    print("\nClicking Events filter...")
    events_filter.click()
    sleep(2)
    screenshot_path = os.path.join(screenshots_dir, "13_1_2_events_filter_active.png")
    print("\nTaking screenshot of Events filter...")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 13_1_2_events_filter_active.png")

    # Click Food & Drinks filter and take screenshot
    print("\nClicking Food & Drinks filter...")
    food_drinks_filter.click()
    sleep(2)
    screenshot_path = os.path.join(screenshots_dir, "13_1_3_food_drinks_filter_active.png")
    print("\nTaking screenshot of Food & Drinks filter...")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 13_1_3_food_drinks_filter_active.png")

    # Click Farms filter and take screenshot
    print("\nClicking Farms filter...")
    farms_filter.click()
    sleep(2)
    screenshot_path = os.path.join(screenshots_dir, "13_1_4_farms_filter_active.png")
    print("\nTaking screenshot of Farms filter...")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 13_1_4_farms_filter_active.png")

    # Click Food Pantries filter and take screenshot
    print("\nClicking Food Pantries filter...")
    food_pantries_filter.click()
    sleep(2)
    screenshot_path = os.path.join(screenshots_dir, "13_1_5_food_pantries_filter_active.png")
    print("\nTaking screenshot of Food Pantries filter...")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 13_1_5_food_pantries_filter_active.png")
