import pytest
import os

from time import sleep
from locators import Trails
from utils_authentication import sign_in_and_prepare
from utils_scrolling import scroll_to_bottom
from utils_ui_navigation import click_trails_button, click_trails_read_more, find_trails_text, find_trail_name, \
    click_trails_see_all
from utils_ui_verification import verify_trails_percentage_progress, verify_trails_visits, verify_trail_status


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
    sign_in_and_prepare(d)

    find_trails_text(d)

    click_trails_see_all(d)

    find_trail_name(d)

    verify_trail_status(d)

    # Take screenshot of trails main screen
    screenshot_path = os.path.join(screenshots_dir, "9_1_1_trails_main_screen.png")
    d.screenshot(screenshot_path)


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
    sign_in_and_prepare(d)

    find_trails_text(d)
    sleep(2)

    click_trails_read_more(d)

    verify_trails_percentage_progress(d)

    verify_trails_visits(d)

    # Take screenshot of trail details
    screenshot_path = os.path.join(screenshots_dir, "9_2_1_trail_details.png")
    d.screenshot(screenshot_path)
    sleep(1)

    scroll_to_bottom(d)

    screenshot_path = os.path.join(screenshots_dir, "9_2_2_trail_details_visits.png")
    d.screenshot(screenshot_path)
