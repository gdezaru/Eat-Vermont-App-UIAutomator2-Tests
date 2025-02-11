import time
from time import sleep
from config import TEST_USER
from locators import Events, DayTrips
from utils import handle_notification_permission, sign_in_user, handle_events_popup
import pytest


@pytest.mark.smoke
def test_day_trip_card(d):
    """Test the Day Trip card on the Home screen"""
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
    d.screenshot("8_1_1_day_trip_details.png")
