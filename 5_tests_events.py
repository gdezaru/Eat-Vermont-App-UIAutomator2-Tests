from time import sleep
import pytest

from conftest import screenshots_dir
from utils_authentication import SignInPrepare
from utils_device_interaction import SearchAI
from utils_ui_navigation import NavEvents, NavEventsFilters
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import EventsScrolling
from locators import AskAI
from utils_ui_verification import VerifyEvents, VerifyEventsFilters, VerifyBusinesses


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


def test_events_filters_date(d, screenshots_dir):
    """
    Tests the events filters on the home screen.
    Steps:
    1. Sign in with valid credentials
    2. Navigate to Events section
    3. Tap Filters
    4. Navigate to next month
    5. Apply Date Filter
    6. Tap Apply Filters
    7. Assert Date Visible on the home screen
    """
    sign_in = SignInPrepare(d)
    nav_home_screen = VerifyEvents(d)
    nav_filters = NavEventsFilters(d)
    nav_dates = VerifyEvents(d)
    verify_filters = VerifyEventsFilters(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_home_screen.verify_events_home_screen()

    nav_filters.click_event_filter_button()

    screenshots.take_screenshot("6_3_1_filters_screen_contents")

    nav_filters.click_next_month_filter()

    screenshots.take_screenshot("6_3_2_filters_next_month_screen_contents")

    current_day = nav_dates.find_and_click_current_day()

    nav_filters.get_next_day(current_day)

    nav_filters.click_apply_filters()

    verify_filters.verify_selected_day_displayed()

    screenshots.take_screenshot("6_3_3_filters_date_applied")


def test_events_filters_drive_time(d, screenshots_dir):
    """
    Tests the events filters on the home screen.
    Steps:
    1. Sign in with valid credentials
    2. Navigate to Events section
    3. Tap Filters
    4. Change Drive Time
    5. Apply Drive Time
    6. Tap Filters
    7. Tap Reset
    8. Assert Drive Time back to initial value (30 min)
    """
    sign_in = SignInPrepare(d)
    nav_home_screen = VerifyEvents(d)
    nav_filters = NavEventsFilters(d)
    verify_filters = VerifyEventsFilters(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_home_screen.verify_events_home_screen()

    nav_filters.click_event_filter_button()

    screenshots.take_screenshot("6_4_1_filters_screen_contents")

    nav_filters.toggle_drive_time(direction="right")

    screenshots.take_screenshot("6_4_2_drive_time_changed")

    nav_filters.click_apply_filters()

    nav_filters.click_event_filter_button()

    nav_filters.click_reset_filters()

    verify_filters.verify_events_filters_default_drive_time()

    screenshots.take_screenshot("6_4_3_drive_time_set_back_to_default")


