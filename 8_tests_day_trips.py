from time import sleep
import pytest
import os

from utils_authentication import sign_in_and_prepare
from utils_ui_navigation import find_day_trips_text, click_day_trips_read_more


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

    read_more_button = find_day_trips_text(d)

    click_day_trips_read_more(d, read_more_button)

    screenshot_path = os.path.join(screenshots_dir, "8_1_1_day_trips_details.png")
    d.screenshot(screenshot_path)
