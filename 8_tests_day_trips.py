from time import sleep
import pytest
from locators import DayTrips
from utils import sign_in_and_prepare, get_screen_dimensions, calculate_swipe_coordinates
import os


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
    sign_in_and_prepare(d)

    # Scroll to center the Day Trip section
    d(scrollable=True).scroll.to(text="Day Trips")
    assert d(text="Day Trips").exists(timeout=5), "Day Trips text not found"
    sleep(2)

    # Scroll very slowly until Read More is visible
    max_small_scrolls = 3
    read_more_button = d.xpath(DayTrips.READ_MORE_HOME_SCREEN)

    # Use utility function to get screen dimensions
    width, height = get_screen_dimensions(d)

    # Calculate swipe coordinates using utility function
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    # Swipe slowly until Read More is visible
    for _ in range(max_small_scrolls):
        if read_more_button.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, 0.2)
        sleep(1)

    assert read_more_button.exists, "Read More button not found"
    read_more_button.click()
    sleep(2)
    screenshot_path = os.path.join(screenshots_dir, "8_1_1_day_trips_details.png")
    d.screenshot(screenshot_path)
