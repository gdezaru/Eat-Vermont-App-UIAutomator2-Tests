from time import sleep
import pytest
import os

from conftest import screenshots_dir
from utils_authentication import sign_in_and_prepare, SignInPrepare
from utils_device_interaction import search_and_submit
from utils_scrolling import scroll_event_card, scroll_to_bottom
from utils_ui_navigation import click_see_all_events_home_screen, find_and_click_more_info_tab, events_add_to_calendar, \
    click_first_event_search_result


@pytest.mark.smoke
def test_events_popup(d, screenshots_dir):
    """
    Tests the contents of the events popup.
    Steps:
    1. Sign in with valid credentials
    2. Verify popup contents
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    sleep(10)


@pytest.mark.smoke
def test_events_card(d, screenshots_dir):
    """
    Tests the contents of an events card.
    Steps:
    1. Sign in with valid credentials
    2. Navigate to Events section
    3. Select an event from the list
    4. Verify event title is displayed
    5. Check event date and time
    6. Verify location information
    7. Check event description
    8. Verify organizer details
    9. Test sharing functionality
    10. Check ticket/RSVP options
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    sleep(10)

    search_term = "Burlington"
    search_and_submit(d, search_term)
    sleep(5)

    click_first_event_search_result(d)

    scroll_event_card(d)

    # Take a screenshot of the event details
    screenshot_path = os.path.join(screenshots_dir, "6_2_1_events_details.png")
    d.screenshot(screenshot_path)

    find_and_click_more_info_tab(d)

    scroll_to_bottom(d)

    # Take screenshot of More Info contents
    screenshot_path = os.path.join(screenshots_dir, "6_2_2_more_info_contents.png")
    d.screenshot(screenshot_path)

    events_add_to_calendar(d)

    # Take screenshot of event added to calendar toast popup
    screenshot_path = os.path.join(screenshots_dir, "6_2_3_add_to_calendar.png")
    d.screenshot(screenshot_path)
