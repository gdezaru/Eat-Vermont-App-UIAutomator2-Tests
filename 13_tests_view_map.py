import pytest
from time import sleep
from locators import HomeScreen, ViewMap
from utils import handle_notification_permission, handle_events_popup, sign_in_user
from retry_decorator import retry

@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_view_map_filters(d):
    """
    Test the View Map filters
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to View Map section
    5. Verify Events filter is visible
    6. Verify Food & Drinks filter is visible
    7. Verify Farms filter is visible
    8. Verify Food Pantries filter is visible
    9. Take screenshot of all filters
    10. Click Events filter and take screenshot
    11. Click Food & Drinks filter and take screenshot
    12. Click Farms filter and take screenshot
    13. Click Food Pantries filter and take screenshot
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

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
    print("\nTook screenshot: 13_1_1_map_filters_present.png")
    d.screenshot("13_1_1_map_filters_present.png")

    # Click Events filter and take screenshot
    print("\nClicking Events filter...")
    events_filter.click()
    sleep(2)
    print("\nTook screenshot: 13_1_2_events_filter_active.png")
    d.screenshot("13_1_2_events_filter_active.png")

    # Click Food & Drinks filter and take screenshot
    print("\nClicking Food & Drinks filter...")
    food_drinks_filter.click()
    sleep(2)
    print("\nTook screenshot: 13_1_3_food_drinks_filter_active.png")
    d.screenshot("13_1_3_food_drinks_filter_active.png")

    # Click Farms filter and take screenshot
    print("\nClicking Farms filter...")
    farms_filter.click()
    sleep(2)
    print("\nTook screenshot: 13_1_4_farms_filter_active.png")
    d.screenshot("13_1_4_farms_filter_active.png")

    # Click Food Pantries filter and take screenshot
    print("\nClicking Food Pantries filter...")
    food_pantries_filter.click()
    sleep(2)
    print("\nTook screenshot: 13_1_5_food_pantries_filter_active.png")
    d.screenshot("13_1_5_food_pantries_filter_active.png")
