from time import sleep
import pytest
from locators import DayTrips
from utils import sign_in_and_prepare, handle_events_popup
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
    print("\nScrolling to Day Trip section...")
    d(scrollable=True).scroll.to(text="Day Trip")
    assert d(text="Day Trip").exists(timeout=5), "Day Trip text not found"
    sleep(2)

    # Scroll very slowly until Read More is visible
    print("\nFine-tuning scroll to find Read More button...")
    max_small_scrolls = 3
    read_more_button = d.xpath(DayTrips.READ_MORE_HOME_SCREEN)

    # Get screen dimensions
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    # Calculate swipe coordinates (swipe in the middle of screen to avoid buttons)
    start_x = width // 2
    start_y = (height * 4) // 5
    end_y = height // 2

    for _ in range(max_small_scrolls):
        if read_more_button.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)

    assert read_more_button.exists, "Read More button not found on Day Trip tile"
    read_more_button.click()
    sleep(5)
    screenshot_path = os.path.join(screenshots_dir, "8_1_1_day_trip_details.png")
    d.screenshot(screenshot_path)
