from unittest import result

import pytest

from utils_authentication import SignInPrepare
from utils_device_interaction import SearchAI
from utils_screenshots import ScreenshotsManagement
from utils_ui_verification import VerifyEvents, VerifyBusinesses, VerifyDayTrips, VerifyVideos


@pytest.mark.smoke
def test_ai_search_events(d, screenshots_dir):
    """
    Test searching for events functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Ask AI in bottom navigation
    5. Click search field
    6. Enter search term 'Burlington'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain events
    """

    sign_in = SignInPrepare(d)
    search_ai = SearchAI(d)
    verify_events = VerifyEvents(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai("Burlington Events")

    verify_events.verify_events_search_result()

    screenshots.take_screenshot("2_1_1_ai_search_events")


@pytest.mark.smoke
def test_ai_search_businesses(d, screenshots_dir):
    """
    Test searching for businesses functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Ask AI in bottom navigation
    5. Click search field
    6. Enter search term 'Big Fatty BBQ'
    7. Submit search
    8. Verify result contains business
    """
    sign_in = SignInPrepare(d)
    search_ai = SearchAI(d)
    verify_businesses = VerifyBusinesses(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai("Big Fatty BBQ")

    verify_businesses.verify_business_search_result()

    screenshots.take_screenshot("2_2_1_ai_search_business")


@pytest.mark.smoke
def test_ai_search_day_trips(d, screenshots_dir):
    """
    Test searching for day trips functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Ask AI in bottom navigation
    5. Click search field
    6. Enter search term 'Day Trip'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain day trips
    """
    sign_in = SignInPrepare(d)
    search_ai = SearchAI(d)
    verify_day_trips = VerifyDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai("Day Trip in Vermont")

    verify_day_trips.verify_day_trips_search_result()

    screenshots.take_screenshot("2_3_1_ai_search_day_trips")


@pytest.mark.smoke
def test_ai_search_videos(d, screenshots_dir):
    """
    Test searching for videos functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Ask AI in bottom navigation
    5. Click search field
    6. Enter search term 'Rocket'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain videos
    """
    sign_in = SignInPrepare(d)
    search_ai = SearchAI(d)
    verify_videos = VerifyVideos(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai("Vermont Videos")

    verify_videos.verify_videos_search_result()

    screenshots.take_screenshot("2_2_4_ai_search_videos")
