from time import sleep
import pytest

from conftest import screenshots_dir
from utils_authentication import SignInPrepare
from utils_device_interaction import SearchAI
from utils_ui_navigation import NavEvents
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import EventsScrolling
from locators import AskAI
from utils_ui_verification import VerifyEvents


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
    nav_events = NavEvents(d)
    screenshots = ScreenshotsManagement(d)
    search_ai = SearchAI(d)
    search_result = VerifyEvents(d)
    events_scroll = EventsScrolling(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai("Vermont Events")

    search_result.verify_events_search_result()

    nav_events.click_first_event_search_result()

    events_scroll.scroll_to_bottom(scroll_times=2)

    screenshots.take_screenshot("6_2_1_events_details")

    nav_events.find_and_click_more_info_tab()

    events_scroll.scroll_to_bottom(scroll_times=2)

    screenshots.take_screenshot("6_2_2_more_info_contents")

    nav_events.events_add_to_calendar()

    screenshots.take_screenshot("6_2_3_add_to_calendar")
